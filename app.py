import tkinter as tk
import interface


class MainApp:
    def __init__(self):
        pass


def build():
    global root, application
    root = tk.Tk()
    application = interface.WidgetsPCR(root)
    root.mainloop()
