import pickle
import _thread as thread
from tkinter import simpledialog, messagebox

import serial

import constants as std

experiments = []


class Experiment:
    """Constrói um objeto Experiment, o qual contêm todas as informações
    temperatura e tempo dos processos.

    Esses objetos são salvos na lista "experiments" e posteriormente
    carregados em um arquivo externo usando o módulo pickle.
    """

    def __init__(self):
        self.name = ''
        self.denaturation_c = ''
        self.denaturation_t = ''
        self.annealing_c = ''
        self.annealing_t = ''
        self.extension_c = ''
        self.extension_t = ''
        self.number_cycles = ''
        self.final_temp = ''

    def __str__(self):
        return self.name


class StringDialog(simpledialog._QueryString):
    """Modificação do ícone da StringDialog original em
    tkinter.simpledialog"""

    # Créditos ao TeamSpen210 do Reddit
    def body(self, master):
        super().body(master)
        self.iconbitmap(std.icon)


def ask_string(title, prompt, **kwargs):
    # Créditos ao TeamSpen210 do Reddit
    d = StringDialog(title, prompt, **kwargs)
    return d.result


def open_pickle(path):
    """Função para descompactar a lista do arquivo experiments.pcr
    (gerado pelo pickle).
    Caso o arquivo não seja encontrado, retorna uma lista vazia.
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


def dump_pickle(path, obj):
    """Salva um objeto no formato binário, utilizando serialização do
    módulo pickle.

    :param path: O caminho para salvar o objeto.
    :param obj: O objeto a ser salvo.
    """
    try:
        with open(path, 'wb') as outfile:
            pickle.dump(obj, outfile)
    except PermissionError:
        messagebox.showerror('Acesso Negado',
                             'Erro com permissões, '
                             'execute o programa como administrador '
                             'e tente novamente.')


def validate_entry(new_text):
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
            return True
        else:
            return False
    except ValueError:
        return False


class ArduinoPCR:
    def __init__(self, port, baudrate, timeout,
                 experiment: Experiment = None):
        self.experiment = experiment
        self.reading = ''

        try:
            self.port_pcr = serial.Serial(port, baudrate, timeout=timeout)
            self.is_connected = True
            std.hover_text = 'Cetus PCR Conectado.'
            print('Connection Successfully. Initializing Serial Monitor (SM)')
        except serial.SerialException:
            self.port_pcr = None
            self.is_connected = False
            std.hover_text = 'Cetus PCR desconectado.'
            print('Connection Failed')

    def run_experiment(self):
        message: str = f'<running: {self.experiment.name}>'
        self.port_pcr.write(b'%a' % message)


class SerialMonitor:
    def __init__(self, device: ArduinoPCR):
        self.device = device
        if self.device.is_connected:
            self.thread = thread.start_new_thread(self.start_monitor, ())

    def start_monitor(self):
        while self.device.is_connected:
            # if self.device.port_pcr.in_waiting:
            try:
                self.device.reading = self.device.port_pcr.readline()
                print(f'(SM) {self.device.reading}')
            except serial.SerialException:
                messagebox.showerror('Dispositivo desconectado',
                                     'Ocorreu um erro ao se comunicar com '
                                     'o CetusPCR. Verifique a conexão e '
                                     'reinicie o aplicativo.')
                self.device.is_connected = False
                std.hover_text = 'Cetus PCR desconectado.'
