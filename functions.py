import tkinter as tk
import interface


def build():
    global root, application
    root = tk.Tk()
    application = interface.WidgetsPCR(root)
    root.mainloop()
