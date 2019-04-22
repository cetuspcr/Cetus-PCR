import tkinter as tk

import interface
import functions


if __name__ == '__main__':
    root = tk.Tk()
    cetus = interface.CetusPCR(root)
    cetus.widgets()

    functions.experiments = functions.open_pickle('experiments.pcr')
    cetus.show_experiments()

    root.mainloop()
