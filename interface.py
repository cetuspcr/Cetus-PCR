"""Design for Cetus PCR application.

"Interface" hold all the information about the widgets of application.

The main structure of the program is the based onto this two main classes:
class CetusPCR -> Select/Create an experiment
class ExperimentPCR -> Edit/Run the selected experiment.

All window classes is inheriting from tk.Frame.
This is just por design purposes since is easier to put a border and organize
widgets inside a frame.
"""

import tkinter as tk
from tkinter import ttk
import constants as std


class CetusPCR(tk.Frame):
    """First window of the application.

    In this window user can select, delete or create a new experiment.
    """

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.master.geometry('+200+10')
        self.master.title('Cetus PCR')
        self.pack()
        self.pack_propagate(False)
        self.configure(width=1000,
                       height=660,
                       bg=std.bg,
                       bd=0,
                       relief=std.relief,
                       highlightcolor=std.bd,
                       highlightbackground=std.bd,
                       highlightthickness=std.bd_width)

    def _widgets(self):
        """Create the widgets of window.

        The reason for the widgets been placed in another method, is because
        this class will be further inherited by ExperimentPCR window and wasn't
        supposed to copy all the widgets to another window, just the frame
        options.
        """
        self.options_frame = tk.Frame(master=self,
                                      width=250,
                                      height=200,
                                      bg=std.bg,
                                      bd=0,
                                      relief=std.relief,
                                      highlightcolor=std.bd,
                                      highlightbackground=std.bd,
                                      highlightthickness=std.bd_width)

        self.options_box_title = tk.Label(master=self,
                                          text='Opções',
                                          font=(std.font_title, 13, 'bold'),
                                          bg=std.bg,
                                          fg=std.label_color,
                                          width=7)
        self.buttons = {}
        for but in ('Abrir', 'Novo', 'Excluir'):
            self.buttons[but] = tk.Button(master=self.options_frame,
                                          font=(std.font_buttons, 13, 'bold'),
                                          text=but,
                                          relief=std.relief,
                                          width=8,
                                          height=0)
            self.buttons[but].pack(pady=14)

        self.experiment_combo = ttk.Combobox(master=self,
                                             width=25,
                                             font=(std.font_title, 20),
                                             values=['Experimento 01'])

        self.experiment_combo_title = tk.Label(master=self,
                                               font=(std.font_title, 25, 'bold'),
                                               text='Selecione o experimento:',
                                               fg=std.label_color,
                                               bg=std.bg)

        self.options_frame.place(rely=0.45,
                                 relx=0.75,
                                 anchor='center')
        self.options_frame.pack_propagate(False)

        self.options_box_title.place(in_=self.options_frame,
                                     bordermode='outside',
                                     relx=0.05,
                                     y=-10)

        self.experiment_combo.place(relx=0.35,
                                    rely=0.47,
                                    anchor='center')

        self.experiment_combo_title.place(in_=self.experiment_combo,
                                          relx=0.5,
                                          anchor='s',
                                          bordermode='outside')


class ExperimentPCR(CetusPCR):
    """Handle the experiment given by CetusPCR window.

    This window is composed by some tk.Entry widgets.
    The state of their are defined by the instruction given by the user in the
    previous window:

    Open -> Entry widgets are disabled and with experiment options inside.
    New -> Entry widgets are enabled and empty.

    If the user choice the Open option, it still be able to activate the Entry
    by pressing the Edit button.

    Inherit from Cetus PCR create automatically a window with the same frame
    configurations.
    This is useful since the windows should look the same in the title, icon
    and size. But their widgets and options are different.
    """
    def __init__(self, master: tk.Toplevel):
        super().__init__(master)


