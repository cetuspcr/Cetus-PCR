import tkinter as tk
import tkinter.messagebox
# import serial
import interface


def dark_mode():
    restart = tkinter.messagebox.askokcancel('Reinicío Necessário',
                                             'É necessário reiniciar o '
                                             'programa para alterar o tema, '
                                             'o trabalho não salvo será perdido.')
    if restart:
        if interface.std_label == 'white':
            interface.std_label = 'black'
            interface.std_bd = 'RoyalBlue2'
            interface.std_bg = 'Cornsilk2'
        else:
            interface.std_bg = '#434343'
            interface.std_bd = '#2ECC71'
            interface.std_label = 'white'
        root.destroy()
        build()


def experiment():
    pass
    # """Write a string to Serial port containing all the experiment information.
    # The structure of string is the following:
    #
    # 'number_of_cycles&
    # denaturing_temperature&
    # denaturing_time&
    # annealing_temperature&
    # annealing_time&
    # extension_temperature&
    # extension_time&
    # final_temperature'
    #
    # Example: '4&90&30&45&30&60&45&30&20'
    # """
    #
    # number_of_cycles = appcetus.entry_cycles.get()
    # denaturing_temperature = appcetus.entry_stageC1.get()
    # denaturing_time = appcetus.entry_stageT1.get()
    # anneling_temperature = appcetus.entry_stageC2.get()
    # anneling_time = appcetus.entry_stageT2.get()
    # extension_temperature = appcetus.entry_stageC3.get()
    # extension_time = appcetus.entry_stageT3.get()
    # final_temperature = appcetus.entry_ftemp.get()
    #
    # str_experiment = f'{number_of_cycles}&' \
    #                  f'{denaturing_temperature}&{denaturing_time}&' \
    #                  f'{anneling_temperature}&{anneling_time}&' \
    #                  f'{extension_temperature}&{extension_time}&' \
    #                  f'{final_temperature}'
    #
    # s_port.write(b"%b" % str_experiment.encode())
    #
    # print(s_port.read(30))


def build():
    global root, appcetus, s_port
    # s_port = serial.Serial('COM1', 9600, timeout=1)
    root = tk.Tk()
    appcetus = interface.WidgetsPCR(root)
    root.mainloop()
