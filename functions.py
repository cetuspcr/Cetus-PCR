import pickle
from tkinter import simpledialog

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


def ask_string(title, prompt, **kargs):
    # Créditos ao TeamSpen210 do Reddit
    d = StringDialog(title, prompt, **kargs)
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


def dump_pickle(path, obj):
    """Salva um objeto no formato binário, utilizando serialização do
    módulo pickle.

    :param path: O caminho para salvar o objeto.
    :param obj: O objeto a ser salvo.
    """
    with open(path, 'wb') as outfile:
        pickle.dump(obj, outfile)


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

