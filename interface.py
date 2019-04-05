"""Design para o aplicativo Cetus PCR.

"Interface" armazena todas as informações sobre os widgets do aplicativo.

A estrutura principal do programa é baseada principalmente nessas duas classes:
class CetusPCR -> Seleciona/Cria um experimento;
class ExperimentPCR -> Edita/Executa o experimento selecionado;

Todas as classes de janelas herdadas da biblioteca tk.Frame.
Isso é feito apenas por propósitos de design,
uma vez que facilita a colocação das bordas e organização dos widgets dentro da janela.
"""

import tkinter as tk
from tkinter import ttk
import constants as std


class CetusPCR(tk.Frame):
    """Primeira janela do aplicativo.

    Nessa janela o usuário pode selecionar, deletar ou criar um experimento.
    """

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.master.geometry('+200+10')
        self.master.title('Cetus PCR')
        self.master.iconbitmap(std.icon)
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
        """Cria os widgets da janela.

        A razão para qual os widgets são colocador em outro método é que essa classe
        será futuramente herdada pela janela ExperimentPCR e não é suposta  para
        copiar todos os widgets para outra janela, apenas as opções de quadro.
        """
        # Create widgets
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
        # Create and place 3 buttons on the options_frame
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

        # Place widgets (buttons not included)
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
    """Lida com o experimento dado pela janela CetusPCR.

    Essa janela é composto por alguns widgets da classe tk.Entry.
    Seu estado é definido pelas instruções dadas pelo usuário
    na janela anterior.

    Abrir -> Widgets de entrada são desabilitados com as opções do experimento
    dentro deles.
    Novo -> Widgets de entrada são habilitados e esvaziados.

    Se o usuário escolher a opção Abrir, ainda é possível
    ativar os widgets de entrada pressionando o botão Editar.

    Herdar do CetusPCR cria automaticamente uma janela
    com as mesmas configurações de quadro.
    Isso é util pois a janela deve ter a mesma aparência, título, ícone e tamanho,
    porém, com widgets e opções diferentes.
    """
    def __init__(self, master: tk.Toplevel):
        super().__init__(master)

    def _widgets(self):
        self.entry_of_options = {}
        self.entry_labels = {}
        gapy = 20
        for stage in ('Desnaturação', 'Anelamento', 'Extensão'):
            gapx = 20
            for option in ('Temperatura', 'Tempo'):
                entry = tk.Entry(master=self,
                                 font=(std.font_title, 30),
                                 width=3,
                                 bd=1,
                                 highlightcolor=std.bd,
                                 highlightthickness=std.bd_width)
                key = 'Entry-' + stage + ' ' + option
                self.entry_of_options[key] = entry
                entry.place(relx=0.2,
                            rely=0.2,
                            x=gapx,
                            y=gapy,
                            anchor='ne')
                gapx += 150
                if option == 'Temperatura':
                    text = '°C'
                else:
                    text = 'Seg'
                unit_label = tk.Label(master=self,
                                      text=text,
                                      fg=std.label_color,
                                      bg=std.bg,
                                      font=(std.font_title, 14, 'bold'))
                unit_label.place(in_=entry,
                                 relx=1,

                                 rely=0,
                                 x=10)
            gapy += 120
            label = tk.Label(master=self,
                             font=(std.font_title, 20, 'bold'),
                             text=stage+':',
                             bg=std.bg,
                             fg=std.label_color)
            self.entry_of_options['Label-'+stage] = label
            label.place(in_=self.entry_of_options['Entry-'+stage+' Temperatura'],
                        anchor='sw',
                        y=-10,
                        bordermode='outside')

        gapy = 20
        for option in ('Nº de ciclos', 'Temperatura Final'):
            key = 'Entry- ' + option
            entry = tk.Entry(master=self,
                             font=(std.font_title, 30),
                             width=3,
                             bd=1,
                             highlightcolor=std.bd,
                             highlightthickness=std.bd_width)
            entry.place(relx=0.7,
                        rely=0.2,
                        y=gapy)
            gapy += 120
            self.entry_of_options[key] = entry

            key = 'Label- ' + option
            label = tk.Label(master=self,
                             font=(std.font_title, 20, 'bold'),
                             text=option+':',
                             fg=std.label_color,
                             bg=std.bg)
            label.place(in_=entry,
                        anchor='s',
                        relx=0.5,
                        y=-10)
            self.entry_of_options[key] = label

        self.button_run = tk.Button(master=self,
                                    text='Iniciar',
                                    font=(std.font_buttons, 20))
        for i in self.entry_of_options:
            print(i)
