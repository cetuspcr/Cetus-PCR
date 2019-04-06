import pickle
# import tkinter as tk

experiments = []


class Experiment:
    def __init__(self, denaturation_c, denaturation_t, annealing_c, annealing_t,
                 extension_c, extension_t, number_cycles, final_temp):
        self.name = ''
        self.denaturation_c = denaturation_c
        self.denaturation_t = denaturation_t
        self.annealing_c = annealing_c
        self.annealing_t = annealing_t
        self.extension_c = extension_c
        self.extension_t = extension_t
        self.number_cycles = number_cycles
        self.final_temp = final_temp


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
