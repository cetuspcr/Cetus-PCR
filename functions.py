import pickle
import tkinter as tk
import interface

experiments = []


class Experiment:
    def __init__(self, denaturation_c, denaturation_t, annealing_c, annealing_t,
                 extension_c, extension_t):
        self.name = ''
        self.denaturation_c = denaturation_c
        self.denaturation_t = denaturation_t
        self.annealing_c = annealing_c
        self.annealing_t = annealing_t
        self.extension_c = extension_c
        self.extension_t = extension_t


def open_pickle(path):
    try:
        with open(path, 'rb') as infile:
            newlist = pickle.load(infile)
            return newlist
    except FileNotFoundError:
        return []


def dump_pickle(path, obj):
    with open(path, 'wb') as outfile:
        pickle.dump(obj, outfile)


def build():
    global root, cetus
    root = tk.Tk()
    cetus = interface.ExperimentPCR(root)
    cetus._widgets()
