import tkinter as tk
import functions

std_bg = '#434343'
std_bd = '#2ECC71'
std_label = 'white'
std_hover = 'Feito com ♥ pelo 3º Mecatrônica (2k19).'
std_fonttitle = 'Courier New'
icon = 'assets/cetusico.ico'


class StdButton(tk.Button):
    def __init__(self, master=None, hovertext=None, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.configure(relief='groove',
                       highlightcolor=std_bd,
                       highlightbackground=std_bd,
                       highlightthickness=2)

        if hovertext is not None:
            self.bind('<Enter>', lambda x: self.hover(hovertext))
            self.bind('<Leave>', lambda x: self.hover(std_hover))

    @staticmethod
    def hover(new_text):
        functions.appcetus.hover_bar.configure(text=new_text)


class WidgetsPCR:
    def __init__(self, master: tk.Tk):
        # Setup Master
        self.master = master
        self.master.title('Cetus PCR')
        self.master.geometry('1000x660+200+10')
        self.master.config(bg=std_bg)
        self.master.iconbitmap(icon)

        # Top Widgets Title
        self.frame_titles = tk.Frame(master=self.master,
                                     bg=std_bg,
                                     bd=0,
                                     relief='groove',
                                     highlightcolor=std_bd,
                                     highlightbackground=std_bd,
                                     highlightthickness=2)
        self.frame_titles.pack(side='top',
                               fill='x')

        self.label_title = tk.Label(master=self.frame_titles,
                                    text='Cetus PCR ',
                                    font=('Courier New', '30', 'bold'),
                                    bg=std_bg,
                                    fg=std_bd,
                                    anchor='e')
        self.label_title.pack(side='right',
                              anchor='w',
                              fill='x')

        # Experiments tree widgets
        self.frame_experimenttree = tk.Frame(master=self.master,
                                             width=300,
                                             height=610,
                                             bg=std_label,
                                             bd=0,
                                             relief='groove',
                                             highlightcolor=std_bd,
                                             highlightbackground=std_bd,
                                             highlightthickness=2)
        self.frame_experimenttree.pack(side='left',
                                       anchor='sw')
        self.frame_experimenttree.pack_propagate(False)
        self.label_tree = tk.Label(master=self.frame_titles,
                                   text='Experimentos',
                                   font=('Courier New', '20', 'bold'),
                                   bg=std_bg,
                                   fg=std_bd,
                                   anchor='se')

        self.label_tree.pack(side='left',
                             anchor='se',
                             fill='x')

        self.tree = tk.Listbox(master=self.frame_experimenttree,
                               height=24,
                               width=50,
                               font='Consolas 14',
                               bd=0,
                               relief='groove',
                               highlightcolor=std_bd,
                               highlightbackground=std_bd,
                               highlightthickness=2,
                               bg=std_bg,
                               fg=std_label)

        self.tree.pack()

        self.frame_treebottom = tk.Frame(master=self.frame_experimenttree,
                                         height=30,
                                         bg='white',
                                         bd=2,
                                         relief='groove')
        self.frame_treebottom.pack(side='bottom', fill='x')

        self.button_add = StdButton(master=self.frame_treebottom,
                                    hovertext='Adicionar um novo experimento',
                                    text='+',
                                    fg='green',
                                    font='Arial 14 bold')
        self.button_add.pack(side='left')

        self.button_sub = StdButton(master=self.frame_treebottom,
                                    hovertext='Excluí o experimento selecionado',
                                    text='-',
                                    fg='red',
                                    font='Arial 14 bold')
        self.button_sub.pack(side='left')
        self.img = tk.PhotoImage(file='assets/moon.png').subsample(20, 20)
        self.button_darkmode = StdButton(master=self.frame_treebottom,
                                         hovertext='Alterna entre os modos '
                                                  'noturno e padrão',
                                         image=self.img,
                                         text='a',
                                         font='Arial 14 bold',
                                         width=30,
                                         height=35,
                                         command=functions.dark_mode)

        self.button_darkmode.pack(side='left')

        # Experiment options widgets
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
        self.stages_labels = []

        for i in ['Desnaturação:', 'Anelamento:', 'Extensão:',
                  'Nº de Ciclos:', '°C Final:']:
            newlabel = tk.Label(master=self.frame_experimentoptions,
                                text=i,
                                font=(std_fonttitle, '25', 'bold'),
                                bg=std_bg,
                                fg=std_label,
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
        self.entry_ftemp = tk.Entry(master=self.frame_experimentoptions,
                                    font=('Courier New', '30'),
                                    width=3)
        self.labelsC = []

        for i in range(4):
            positons = [80, 200, 320, 200]
            newlabel = tk.Label(master=self.frame_experimentoptions,
                                text='°C',
                                font=(std_fonttitle, '15', 'bold'),
                                fg=std_label,
                                bg=std_bg,
                                anchor='e')
            self.labelsC.append(newlabel)
            newlabel.place(x=130, y=positons[i])
            newlabel = tk.Label(master=self.frame_experimentoptions,
                                text='Seg',
                                font=(std_fonttitle, '15', 'bold'),
                                fg=std_label,
                                bg=std_bg,
                                anchor='e')
            newlabel.place(x=280, y=positons[i])
            self.labelsC.append(newlabel)

        for widget in self.frame_experimentoptions.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.configure(relief='groove',
                                 highlightcolor=std_bd,
                                 highlightthickness=2)

        self.button_run = StdButton(master=self.frame_experimentoptions,
                                    hovertext='Iniciar o experimento selecionado',
                                    text='INICIAR',
                                    # command=functions.experiment,
                                    font='Arial 15 bold'
                                    )
        self.button_run.place(x=470, y=325)

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
        self.entry_ftemp.place(x=470, y=200)
        self.labelsC[6].place(x=550, y=200)

        # Hover bar
        self.hover_bar = tk.Label(master=self.frame_experimentoptions,
                                  text=std_hover,
                                  bg='white',
                                  font='Arial 10 italic',
                                  anchor='w')
        self.hover_bar.pack(fill='x',
                            side='bottom')
