import os
import pickle
import tkinter as tk
import tkinter.messagebox

# import serial

import interface

serialport = 'COM4'
path_experiments = 'experiments'


class Experiment:
    def __init__(self):
        self.name = None


    def _generate(self):
        """Internal function.

        Define the attributes of experiment by reading the entry boxes in
        main window.
        """
        self.number_of_cycles = appcetus.entry_cycles.get()
        self.denaturing_temperature = appcetus.entry_stageC1.get()
        self.denaturing_time = appcetus.entry_stageT1.get()
        self.annealing_temperature = appcetus.entry_stageC2.get()
        self.annealing_time = appcetus.entry_stageT2.get()
        self.extension_temperature = appcetus.entry_stageC3.get()
        self.extension_time = appcetus.entry_stageT3.get()
        self.final_temperature = appcetus.entry_ftemp.get()

    def save(self):
        self._generate()



def dark_mode():
    restart = tkinter.messagebox.askokcancel('Reinicío Necessário',
                                             'É necessário reiniciar o '
                                             'programa para alterar o tema, '
                                             'o trabalho não salvo será perdido.')
    if restart:
        if interface.std_label == 'white':
            interface.std_label = 'black'
            interface.std_bd = 'SpringGreen4'
            interface.std_bg = 'Cornsilk2'
        else:
            interface.std_bg = '#434343'
            interface.std_bd = '#2ECC71'
            interface.std_label = 'white'
        root.destroy()
        build()


# def experiment():
#     """Write a string to Serial port containing all the experiment information.
#     The structure of string is the following:
#
#     'number_of_cycles&
#     denaturing_temperature&
#     denaturing_time&
#     annealing_temperature&
#     annealing_time&
#     extension_temperature&
#     extension_time&
#     final_temperature'
#
#     Example: '4&90&30&45&30&60&45&30&20'
#     """
#
#     number_of_cycles = appcetus.entry_cycles.get()
#     denaturing_temperature = appcetus.entry_stageC1.get()
#     denaturing_time = appcetus.entry_stageT1.get()
#     anneling_temperature = appcetus.entry_stageC2.get()
#     anneling_time = appcetus.entry_stageT2.get()
#     extension_temperature = appcetus.entry_stageC3.get()
#     extension_time = appcetus.entry_stageT3.get()
#     final_temperature = appcetus.entry_ftemp.get()
#
#     str_experiment = f'<{number_of_cycles}&' \
#                      f'{denaturing_temperature}&{denaturing_time}&' \
#                      f'{anneling_temperature}&{anneling_time}&' \
#                      f'{extension_temperature}&{extension_time}&' \
#                      f'{final_temperature}>'
#
#     s_port.write(b"%b" % str_experiment.encode())
#
#     print(s_port.readlines())

def open_experiments():
    global experiments, list_experiments
    list_experiments = []
    experiments = os.listdir(path_experiments)
    for exp in experiments:
        if exp.endswith('.exp'):
            list_experiments.append(exp)
            exp = exp[:-4]
            appcetus.tree.insert(0, exp)


def build():
    global root, appcetus, s_port
    # s_port = serial.Serial(serialport, 9600, timeout=1)
    root = tk.Tk()
    appcetus = interface.WidgetsPCR(root)
