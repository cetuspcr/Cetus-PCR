import pickle
from time import sleep
import _thread as thread
from tkinter import simpledialog, messagebox

import serial  # Listado como pyserial em requirements.txt
from serial.tools import list_ports

import constants as std

experiments = []


class ExperimentPCR:
    """Constrói um objeto Experiment, o qual contêm todas as informações
    temperatura e tempo dos processos.

    Esses objetos são salvos na lista "experiments" e posteriormente
    carregados em um arquivo externo usando o módulo pickle.

    Os objetos salvos fornecidos a "steps" devem ser obrigatoriamente da
    classe StepPCR.
    """

    def __init__(self, name, cycles=0, final_hold=0, *steps):
        self.name = name
        self.cycles = cycles
        self.final_hold = final_hold
        self.steps = list(steps)

    def __str__(self):
        str_steps = ''
        for step in self.steps:
            str_steps += f'-{str(step)}\n'
        final_str = f'\nNome do Experimento: "{self.name}"\n' \
                    f'->Nº de ciclos: {self.cycles}\n' \
                    f'->Temperatura Final: {self.final_hold}°C\n' \
                    f'{str_steps}'
        return final_str

    def check_fields(self):
        pass

    def add_step(self, name, temp, duration):
        new_step = StepPCR(name, temp, duration)
        self.steps.append(new_step)


class StepPCR:
    def __init__(self, name, temp, duration):
        self.name = name
        self.temperature = temp
        self.duration = duration

    @classmethod
    def from_string(cls, ):
        pass

    def __add__(self, other):
        return self.duration + other.duration

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
        self.experiment = experiment

        # Conferir com o nome no Gerenciador de dispositivos do windows
        # caso esteja usando um arduino diferente.
        self.device_type = 'Arduino Uno'

        self.port_connected = None
        self.serial_device = None
        self.is_connected = False
        self.waiting_update = False

        self.reading = ''
        self.cur_cycle = None
        self.cur_temperature_pcr = None
        self.cur_temperature_lid = None
        self.cur_time = 0
        self.cur_stage = None
        self.is_running = False
        self.new_cycle = False

        self.initialize_connection()

    def run_experiment(self):
        self.cur_time = 0
        for _ in range(int(self.experiment.number_cycles)):
            for step in ('denaturation', 'annealing', 'extension'):
                if self.is_running:
                    self.cur_stage = step.capitalize()

                    temperature = self.experiment.__dict__[f'{step}_c']
                    time = self.experiment.__dict__[f'{step}_t']
                    cmd = b'setTemp:: %d' % c_to_pwm(temperature)
                    self.serial_device.write(cmd)

                    while not self.new_cycle:
                        pass
                    if self.new_cycle:
                        for t in range(time):
                            if self.is_running:
                                print('Current step time:', t + 1)
                                sleep(1)
                                self.cur_time += 1
                            else:
                                break
                        self.new_cycle = False
                else:
                    break

    def start_monitor(self):
        while self.is_connected:
            try:
                self.reading = self.serial_device.readline()
                self.reading = str(self.reading).replace(r'\r\n', '')
                if 'pcr_sensor::' in self.reading:
                    self.cur_temperature_pcr = \
                        self.reading.split('::')[1].replace("'", '')
                elif 'lid_sensor::' in self.reading:
                    self.cur_temperature_lid = \
                        self.reading.split('::')[1].replace("'", '')
                elif 'setting_peltier::' in self.reading:
                    self.new_cycle = True
                    print(f'(SM) {self.reading}')
                else:
                    print(f'(SM) {self.reading}')
            except serial.SerialException:
                messagebox.showerror('Dispositivo desconectado',
                                     'Ocorreu um erro ao se comunicar com '
                                     'o CetusPCR. Verifique a conexão e '
                                     'reinicie o aplicativo.')
                self.is_connected = False
                self.waiting_update = True
                self.is_running = False
                std.hover_text = 'Cetus PCR desconectado.'

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
            thread.start_new_thread(self.start_monitor, ())


class StringDialog(simpledialog._QueryString):
    """Modificação do ícone da StringDialog original em
    tkinter.simpledialog"""

    # Créditos ao TeamSpen210 do Reddit
    def body(self, master):
        super().body(master)
        self.iconbitmap(std.window_icon)


def ask_string(title, prompt, **kwargs):
    # Créditos ao TeamSpen210 do Reddit
    d = StringDialog(title, prompt, **kwargs)
    return d.result


def open_pickle(path: str) -> list:
    """Função para descompactar a lista do arquivo experiments.pcr
    (gerado pelo pickle).
    Caso o arquivo não seja encontrado, retorna uma lista vazia.

    :param path: O caminho do arquivo de experimentos.

    :return: Retorna uma lista com os experimentos no arquivo, ou uma
    lista vazia caso o arquivo não exista.
    """
    try:
        with open(path, 'rb') as infile:
            newlist = pickle.load(infile)
            return newlist
    except FileNotFoundError:
        return []
    except PermissionError:
        messagebox.showerror('Acesso Negado',
                             'Erro com permissões, '
                             'execute o programa como administrador '
                             'e tente novamente.')


def dump_pickle(path: str, obj: object):
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


# Ainda não Finalizada.
def c_to_pwm(celsius: int) -> int:
    pwm_signal = celsius  # TODO fórmula de conversão
    return pwm_signal
