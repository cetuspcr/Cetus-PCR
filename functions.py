import tkinter as tk
import interface


def build():
    global root, cetus
    root = tk.Tk()
    cetus = interface.CetusPCR(root)
