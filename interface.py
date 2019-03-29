import tkinter as tk
import app

std_bg = 'cornsilk2'
std_bd = 'dark green'
std_hover = 'Feito com ♥ pelo 3º Mecatrônica (2k19).'
std_fonttitle = 'Courier New'


class MyButton(tk.Button):
    def __init__(self, master=None, hovertext=None, cnf={}, **kw):
        tk.Button.__init__(self, master=master, cnf=cnf, **kw)
        self.configure(relief='groove',
                       highlightcolor=std_bd,
                       highlightbackground=std_bd,
                       highlightthickness=2)

        if hovertext is not None:
            self.bind('<Enter>', lambda x: self.hover(hovertext))
            self.bind('<Leave>', lambda x: self.hover(std_hover))

    @staticmethod
    def hover(new_text):
        app.application.hover_bar.configure(text=new_text)


class WidgetsPCR:
    def __init__(self, master: tk.Tk):
        # Setup Master
        self.master = master
        self.master.title('Cetus PCR')
        self.master.geometry('1000x660+200+10')
        self.master.config(bg=std_bg)

        # Setup Widgets
        self.frame_titles = tk.Frame(master=self.master,
                                     bg=std_bg,
                                     bd=0,
                                     relief='groove',
                                     highlightcolor=std_bd,
                                     highlightbackground=std_bd,
                                     highlightthickness=2)
        self.frame_titles.pack(side='top',
                               fill='x')

        self.frame_experimenttree = tk.Frame(master=self.master,
                                             width=300,
                                             height=610,
                                             bg='white',
                                             bd=0,
                                             relief='groove',
                                             highlightcolor=std_bd,
                                             highlightbackground=std_bd,
                                             highlightthickness=2)
        self.frame_experimenttree.pack(side='left',
                                       anchor='sw')

        self.frame_experimentoptions = tk.Frame(master=self.master,
                                                width=700,
                                                height=610,
                                                bg=std_bg,
                                                bd=0,
                                                relief='groove',
                                                highlightcolor=std_bd,
                                                highlightbackground=std_bd,
                                                highlightthickness=2)

        self.frame_experimentoptions.pack(fill='both',
                                          expand=True)
        self.frame_experimentoptions.pack_propagate(False)

        self.label_title = tk.Label(master=self.frame_titles,
                                    text='Cetus PCR ',
                                    font=('Courier New', '30', 'bold'),
                                    bg=std_bg,
                                    fg=std_bd,
                                    anchor='e')
        self.label_title.pack(side='right',
                              anchor='w',
                              fill='x')
        self.label_tree = tk.Label(master=self.frame_titles,
                                   text='Experimentos',
                                   font=('Courier New', '20', 'bold'),
                                   bg=std_bg,
                                   fg=std_bd,
                                   anchor='se')
        self.label_tree.pack(side='left',
                             anchor='se',
                             fill='x')

        self.tree = tk.Listbox(master=self.frame_experimenttree)
        self.tree.pack(fill='both')

        self.hover_bar = tk.Label(master=self.frame_experimentoptions,
                                  text=std_hover,
                                  bg='white',
                                  font='Arial 10 italic',
                                  anchor='w')
        self.hover_bar.pack(fill='x',
                            side='bottom')

        self.stages_labels = []
        for i in ['Desnaturação:', 'Anelamento:', 'Extensão:',
                  'Nº de Ciclos:', '°C Inicial:']:
            newlabel = tk.Label(master=self.frame_experimentoptions,
                                text=i,
                                font=(std_fonttitle, '25', 'bold'),
                                bg=std_bg,
                                anchor='e')
            self.stages_labels.append(newlabel)

        self.entry_stageC1 = tk.Entry(master=self.frame_experimentoptions,
                                      font=('Courier New', '30'),
                                      width=3)
        self.entry_stageC2 = tk.Entry(master=self.frame_experimentoptions,
                                      font=('Courier New', '30'),
                                      width=3)
        self.entry_stageC3 = tk.Entry(master=self.frame_experimentoptions,
                                      font=('Courier New', '30'),
                                      width=3)
        self.entry_stageT1 = tk.Entry(master=self.frame_experimentoptions,
                                      font=('Courier New', '30'),
                                      width=3)
        self.entry_stageT2 = tk.Entry(master=self.frame_experimentoptions,
                                      font=('Courier New', '30'),
                                      width=3)
        self.entry_stageT3 = tk.Entry(master=self.frame_experimentoptions,
                                      font=('Courier New', '30'),
                                      width=3)
        self.entry_cycles = tk.Entry(master=self.frame_experimentoptions,
                                     font=('Courier New', '30'),
                                     width=3)
        self.entry_temp = tk.Entry(master=self.frame_experimentoptions,
                                   font=('Courier New', '30'),
                                   width=3)
        self.labelsC = []

        for i in range(4):
            positons = [80, 200, 320, 200]
            newlabel = tk.Label(master=self.frame_experimentoptions,
                                text='°C',
                                font=(std_fonttitle, '15', 'bold'),
                                bg=std_bg,
                                anchor='e')
            self.labelsC.append(newlabel)
            newlabel.place(x=130, y=positons[i])
            newlabel = tk.Label(master=self.frame_experimentoptions,
                                text='Seg',
                                font=(std_fonttitle, '15', 'bold'),
                                bg=std_bg,
                                anchor='e')
            newlabel.place(x=280, y=positons[i])
            self.labelsC.append(newlabel)

        for widget in self.frame_experimentoptions.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.configure(relief='groove',
                                 highlightcolor=std_bd,
                                 highlightthickness=2)

        self.stages_labels[0].place(x=20, y=20)
        self.entry_stageC1.place(x=50, y=80)
        self.entry_stageT1.place(x=200, y=80)

        self.stages_labels[1].place(x=20, y=140)
        self.entry_stageC2.place(x=50, y=200)
        self.entry_stageT2.place(x=200, y=200)

        self.stages_labels[2].place(x=20, y=260)
        self.entry_stageC3.place(x=50, y=320)
        self.entry_stageT3.place(x=200, y=320)

        self.stages_labels[3].place(x=400, y=20)
        self.entry_cycles.place(x=470, y=80)

        self.stages_labels[4].place(x=400, y=140)
        self.entry_temp.place(x=470, y=200)
        self.labelsC[6].place(x=550, y=200)
