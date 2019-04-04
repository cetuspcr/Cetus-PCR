import tkinter as tk
from tkinter import ttk
import constants as std


class CetusPCR(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master=master)
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

        self.fr_title = tk.Frame(master=self,
                                 height=100)

        self.experiment_box = ttk.Combobox(master=self,
                                           width=25,
                                           font=(std.font_title, 20))
        self.experiment_box_title = tk.Label(master=self,
                                             font=(std.font_title, 25, 'bold'),
                                             text='Selecione o experimento:',
                                             fg=std.label_color,
                                             bg=std.bg)
        self.button_confirm = tk.Button(master=self,
                                        font=(std.font_buttons, 15, 'bold'),
                                        text='CORRER',
                                        relief=std.relief)

        self.button_confirm.place(relx=0.5,
                                  rely=0.5,
                                  anchor='center')

        self.experiment_box.place(in_=self.button_confirm,
                                  anchor='s',
                                  relx=0.5,
                                  y=-1,
                                  bordermode='outside')

        self.experiment_box_title.place(in_=self.experiment_box,
                                        relx=0.5,
                                        anchor='s',
                                        bordermode='outside')
