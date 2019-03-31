import tkinter as tk
import tkinter.messagebox
import interface


def dark_mode():
    restart = tkinter.messagebox.askokcancel('Reinicío Necessário',
                                             'É necessário reiniciar o programa para alterar o tema, o trabalho não salvo será perdido.')
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


def build():
    global root, application
    root = tk.Tk()
    application = interface.WidgetsPCR(root)
    root.mainloop()
