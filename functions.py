import pickle
# import tkinter as tk

experiments = []


class Experiment:
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
