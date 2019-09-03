import pickle
from time import sleep, time
import _thread as thread
from tkinter import simpledialog, messagebox

import serial  # Listado como pyserial em requirements.txt
from serial.tools import list_ports
from simple_pid import PID

import constants as std

experiments = []


class ExperimentPCR:
    """Um objeto que contêm todas as informações de temperatura e tempo dos
    processos.
    Esses objetos são salvos na lista "experiments" e posteriormente
    carregados em um arquivo externo usando o módulo pickle.

    Os objetos salvos fornecidos a "steps" devem ser obrigatoriamente da
    classe StepPCR.
    """

    def __init__(self, name, n_cycles=0, final_hold=0, *steps):
        self.name = name
        self.n_cycles = n_cycles
        self.final_hold = final_hold
        self.steps = list(steps)
        self._update_estimated_time()

    def __str__(self):
        str_steps = ''
        for step in self.steps:
            str_steps += f'-{str(step)}\n'
        final_str = f'\nNome do Experimento: "{self.name}"\n' \
            f'->Nº de ciclos: {self.n_cycles}\n' \
            f'->Temperatura Final: {self.final_hold}°C\n' \
            f'{str_steps}'
        return final_str

    def add_step(self, name, temp, duration):
        new_step = StepPCR(name, temp, duration)
        self.steps.append(new_step)
        self._update_estimated_time()

    def _update_estimated_time(self):
        self.estimated_time = 0
        for step in self.steps:
            self.estimated_time += int(step.duration)
        self.estimated_time *= int(self.n_cycles)


class StepPCR:
    def __init__(self, name, temp, duration):
        self.name = name
        self.temperature = temp
        self.duration = duration

    def __repr__(self):
        return f'StepPCR({self.name}, {self.temperature}, {self.duration})'

    def __str__(self):
        return f'Passo de PCR "{self.name}": ' \
            f'{self.temperature}°C, {self.duration}s'


class ArduinoPCR:
    """Classe com protocolos para comunicação serial."""

    def __init__(self, baudrate, timeout,
                 experiment: ExperimentPCR = None):
        self.timeout = timeout
        self.baudrate = baudrate
        self.experiment: ExperimentPCR = experiment
        self.pid = PID(Kp=3, Ki=0, Kd=0,
                       output_limits=(-255, 255), sample_time=0)

        # Conferir com o nome no Gerenciador de dispositivos do windows
        # caso esteja usando um arduino diferente.
        self.device_type = ''

        self.port_connected = None
        self.serial_device: serial.Serial = None
        self.is_connected = False
        self.waiting_update = False
        self.monitor_thread = None

        self.is_running = False
        self.is_waiting = True
        self.current_sample_temperature = 0
        self.current_lid_temperature = 0
        self.current_step = ''
        self.current_cycle = 0
        self.elapsed_time = 0

        self.reading = ''

        self.initialize_connection()

    def run_experiment(self):
        sleep(1)
        started_time = time()
        for step in self.experiment.steps:
            self.elapsed_time += int(step.duration)
        self.elapsed_time *= self.experiment.n_cycles
        for i in range(int(self.experiment.n_cycles)):
            self.current_cycle = i + 1
            for step in self.experiment.steps:
                self.current_step = step.name
                set_point = int(step.temperature)
                duration = int(step.duration)
                started_step_time = time()
                self.pid.setpoint = set_point
                while time() - started_step_time <= duration:
                    if not self.is_running:
                        print('Experiment Cancelled')
                        messagebox.showinfo('Cetus PCR', 'O experimento foi '
                                                         'cancelado.')
                        self.serial_device.write(b'<printTemps 0>')
                        return
                    elif self.is_waiting:
                        output = self.pid(self.current_sample_temperature)
                        if output > 0:
                            rv = f'<peltier 0 {int(output):03}>'
                        elif output < 0:
                            rv = f'<peltier 1 {int(abs(output)):03}>'
                        self.serial_device.write(b'%a\r\n' % rv)
                        self.is_waiting = False
                        self.elapsed_time = int(time() - started_time)
        print(f'Finish time: {time() - started_time}')
        self.serial_device.write(b'<printTemps 0>')

    def serial_monitor(self):
        """Função para monitoramento da porta serial do Arduino.

        Todas as informações provenientes da porta serial são exibidas
        no prompt padrão do Python.
        Determinadas informações também são guardadas em variáveis para
        serem posteriormente exibidas para o usuário.

        Esse processo deve ser rodado em outra thread para evitar a parada
        do mainloop da janela principal.
        """

        while self.is_connected:
            try:
                self.reading = self.serial_device.readline().decode()
                self.reading = self.reading.strip('\r\n')
                if 'tempSample' in self.reading:
                    self.current_sample_temperature = \
                        float(self.reading.split()[1])
                elif 'tempLid' in self.reading:
                    self.current_lid_temperature = \
                        float(self.reading.split()[1])
                elif self.reading == 'nextpls':
                    self.is_waiting = True
                # if self.reading != '':
                #     print(repr(f'(SM) {self.reading}'))

            except serial.SerialException:
                messagebox.showerror('Dispositivo desconectado',
                                     'Ocorreu um erro ao se comunicar com '
                                     'o CetusPCR. Verifique a conexão e '
                                     'reinicie o aplicativo.')
                self.is_connected = False
                self.waiting_update = True
                std.hover_text = 'Cetus PCR desconectado.'
        return  # Return para encerrar a thread

    def initialize_connection(self):
        try:
            ports = list_ports.comports()
            if not list_ports.comports():  # Se não há nada conectado
                raise serial.SerialException
            for port in ports:
                if self.device_type in port.description:
                    self.serial_device = serial.Serial(port.device,
                                                       self.baudrate,
                                                       timeout=self.timeout)

                    sleep(2)  # Delay para esperar o sinal do arduino
                    self.reading = self.serial_device.readline()
                    if self.reading == b'Cetus is ready.\r\n':
                        self.is_connected = True
                        self.port_connected = port.device
                        print('Connection Successfully. '
                              'Initializing Serial Monitor (SM)')
                        break
                else:
                    raise serial.SerialException
        except serial.SerialException:
            self.serial_device = None
            self.is_connected = False
            print('Connection Failed')

        if self.is_connected:
            self.monitor_thread = thread.start_new_thread(self.serial_monitor,
                                                          ())


class StringDialog(simpledialog._QueryString):
    """Modificação do ícone da StringDialog original em
    tkinter.simpledialog"""

    # Créditos ao TeamSpen210 do Reddit
    def body(self, master):
        super().body(master)
        self.iconbitmap(std.WINDOW_ICON)


def ask_string(title, prompt, **kwargs):
    # Créditos ao TeamSpen210 do Reddit
    d = StringDialog(title, prompt, **kwargs)
    return d.result


def open_pickle_file(path: str) -> list:
    """Função para descompactar a lista do arquivo experiments.pcr
    (gerado pelo pickle).
    Caso o arquivo não seja encontrado, retorna uma lista vazia.

    :param path: O caminho do arquivo de experimentos.

    :return: Uma lista com os experimentos no arquivo, ou uma
    lista vazia caso o arquivo não exista.
    """
    try:
        with open(path, 'rb') as infile:
            new_list = pickle.load(infile)
            return new_list
    except FileNotFoundError:
        return []
    except PermissionError:
        messagebox.showerror('Acesso Negado',
                             'Erro com permissões, '
                             'execute o programa como administrador '
                             'e tente novamente.')


def save_pickle_file(path: str, obj: object):
    """Salva um objeto no formato binário, utilizando serialização do
    módulo pickle.

    :param path: O caminho para salvar o objeto.
    :param obj: O objeto a ser salvo.
    """
    try:
        with open(path, 'wb') as outfile:
            pickle.dump(obj, outfile, protocol=pickle.HIGHEST_PROTOCOL)
    except PermissionError:
        messagebox.showerror('Acesso Negado',
                             'Erro com permissões, '
                             'execute o programa como administrador '
                             'e tente novamente.')


def validate_entry(new_text) -> bool:
    """Função callback para validação de entrada dos campos na janela
    ExperimentPCR.

    É chamada toda vez que o usuário tenta inserir um valor no campo de
    entrada.

    Uma entrada válida deve atender os seguintes requisitos:
        -Ser composto apenas de números inteiros.
        -Ter um número de caracteres menor que 3.

    :param new_text: Passada pelo próprio widget de entrada.
    :return: boolean - Retorna pro widget se a entrada é ou não válida.
    """
    if new_text == '':  # Se "backspace"
        return True
    try:
        int(new_text)
        if len(new_text) <= 3:
            return len(new_text) <= 3
    except ValueError:
        return False


def seconds_to_string(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f'{h}h {m}m {s}s'
    elif m > 0:
        return f'{m}m {s}s'
    else:
        return f'{s}s'
