import tkinter as tk
import interface


def dark_mode():
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
