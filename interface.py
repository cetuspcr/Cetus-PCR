"""Design para o aplicativo Cetus PCR.

"Interface" armazena todas as informações sobre os widgets do aplicativo.

A estrutura principal do programa é baseada principalmente nessas duas classes:
class CetusPCR -> Seleciona/Cria um experimento;
class ExperimentPCR -> Edita/Executa o experimento selecionado;

Todas as classes de janelas herdadas da biblioteca tk.Frame.
Isso é feito apenas por propósitos de design,
uma vez que facilita a colocação das bordas e organização dos widgets dentro da
janela.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import constants as std

import functions


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
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.pack()
        self.pack_propagate(False)
        self.master.focus_force()
        self.configure(width=1000,
                       height=660,
                       bg=std.bg,
                       bd=0,
                       relief=std.relief,
                       highlightcolor=std.bd,
                       highlightbackground=std.bd,
                       highlightthickness=std.bd_width)
        self.widgets = self._widgets

    def _widgets(self):
        """Cria os widgets da janela.

        A razão para qual os widgets são colocador em outro método é que essa
        classe será futuramente herdada pela janela ExperimentPCR e não é
        suposta para copiar todos os widgets para outra janela, apenas as
        opções de quadro.
        """
        # Criar os widgets
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
        # Criar e posicionar 3 botões dentro do "options_frame"
        for but in ('Abrir', 'Novo', 'Excluir'):
            self.buttons[but] = tk.Button(master=self.options_frame,
                                          font=(std.font_buttons, 13, 'bold'),
                                          text=but,
                                          relief=std.relief,
                                          width=8,
                                          height=0)
            self.buttons[but].pack(pady=14)
        self.buttons['Abrir'].configure(command=self.handle_openbutton)
        self.buttons['Novo'].configure(command=self.handle_newbutton)
        self.buttons['Excluir'].configure(command=self.handle_deletebutton)

        self.experiment_combo = ttk.Combobox(master=self,
                                             width=30,
                                             font=(std.font_title, 15),
                                             values=['Experimento 01'])

        self.experiment_combo_title = tk.Label(master=self,
                                               font=(std.font_title, 25,
                                                     'bold'),
                                               text='Selecione o experimento:',
                                               fg=std.label_color,
                                               bg=std.bg)

        # Posicionar os widgets(botões não incluídos)
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

        self.show_experiments()

    def show_experiments(self):
        functions.experiments = functions.open_pickle(std.exp_path)
        self.experiment_combo.configure(values=functions.experiments)

    def handle_openbutton(self):
        index = self.experiment_combo.current()
        if index >= 0:
            newroot = tk.Tk()
            new = ExperimentPCR(newroot, index)
            new.widgets()
            self.master.destroy()

    def handle_newbutton(self):
        new_experiment = functions.Experiment()
        name = functions.ask_string('Novo Experimento', 'Digite o nome do'
                                                        ' experimento:',
                                    parent=self.master)
        new_experiment.name = name
        if new_experiment.name is not None:
            functions.experiments.append(new_experiment)
            functions.dump_pickle(std.exp_path, functions.experiments)
            self.experiment_combo.configure(values=functions.experiments)

            newroot = tk.Tk()
            new = ExperimentPCR(newroot,
                                functions.experiments.index(new_experiment))
            new.widgets()
            self.master.destroy()
        elif name is None:
            messagebox.showerror('Novo Experimento', 'O nome não pode estar'
                                                     ' vazio')

    def handle_deletebutton(self):
        delete = messagebox.askyesnocancel('Deletar experimento',
                                           'Você tem certeza?')
        if delete:
            functions.experiments.pop(self.experiment_combo.current())
            functions.dump_pickle(std.exp_path, functions.experiments)
            print(functions.experiments)
            self.experiment_combo.configure(values=functions.experiments)
            self.experiment_combo.delete(0, 'end')

    def close_window(self):
        functions.dump_pickle(std.exp_path, functions.experiments)
        self.master.destroy()


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
    Isso é util pois a janela deve ter a mesma aparência, título, ícone e
    tamanho, porém, com widgets e opções diferentes.
    """
    def __init__(self, master: tk.Tk, exp_index):
        super().__init__(master)
        self.experiment = functions.experiments[exp_index]
        self.vcmd = self.master.register(functions.validate_entry)

    def _widgets(self):
        self.entry_of_options = {}
        self.gapy = 20
        for stage in ('Desnaturação', 'Anelamento', 'Extensão'):
            self.gapx = 20
            for option in ('Temperatura', 'Tempo'):
                entry = tk.Entry(master=self,
                                 font=(std.font_title, 30),
                                 width=3,
                                 bd=1,
                                 highlightcolor=std.bd,
                                 highlightthickness=std.bd_width,
                                 validate='key',
                                 validatecommand=(self.vcmd, '%P')
                                 )
                key = f'{stage} {option}'
                self.entry_of_options[key] = entry
                entry.place(relx=0.2,
                            rely=0.2,
                            x=self.gapx,
                            y=self.gapy,
                            anchor='ne')
                self.gapx += 150
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
            self.gapy += 120
            label = tk.Label(master=self,
                             font=(std.font_title, 20, 'bold'),
                             text=stage+':',
                             bg=std.bg,
                             fg=std.label_color)
            label.place(in_=self.entry_of_options[f'{stage} Temperatura'],
                        anchor='sw',
                        y=-10,
                        bordermode='outside')

        self.gapy = 20
        for option in ('Nº de ciclos', 'Temperatura Final'):
            key = option
            entry = tk.Entry(master=self,
                             font=(std.font_title, 30),
                             width=3,
                             bd=1,
                             highlightcolor=std.bd,
                             highlightthickness=std.bd_width,
                             validate='key',
                             validatecommand=(self.vcmd, '%P'))
            entry.place(relx=0.7,
                        rely=0.2,
                        y=self.gapy)
            self.gapy += 120
            self.entry_of_options[key] = entry

            label = tk.Label(master=self,
                             font=(std.font_title, 20, 'bold'),
                             text=option+':',
                             fg=std.label_color,
                             bg=std.bg)
            label.place(in_=entry,
                        anchor='s',
                        relx=0.5,
                        y=-10)

            if option == 'Temperatura Final':
                unit_label = tk.Label(master=self,
                                      font=(std.font_title, 14, 'bold'),
                                      text='°C',
                                      bg=std.bg,
                                      fg=std.label_color)
                unit_label.place(in_=entry,
                                 relx=1,
                                 rely=0,
                                 x=10)

        self.buttons_frame = tk.Frame(master=self,
                                      width=250,
                                      height=100,
                                      bg=std.bg,
                                      bd=0,
                                      relief=std.relief,
                                      highlightcolor=std.bd,
                                      highlightbackground=std.bd,
                                      highlightthickness=std.bd_width)
        self.buttons_frame.place(in_=self.
                                 entry_of_options['Temperatura Final'],
                                 anchor='n',
                                 relx=0.5,
                                 rely=1,
                                 y=50)
        self.buttons_frame_title = tk.Label(master=self,
                                            text='Opções',
                                            font=(std.font_title, 13, 'bold'),
                                            bg=std.bg,
                                            fg=std.label_color,
                                            width=7)
        self.buttons_frame_title.place(in_=self.buttons_frame,
                                       bordermode='outside',
                                       relx=0.05,
                                       y=-10)
        self.buttons_frame.pack_propagate(False)

        self.buttons = {}
        for but in ('Salvar', 'Executar'):
            self.buttons[but] = tk.Button(master=self.buttons_frame,
                                          text=but,
                                          width=7,
                                          font=(std.font_buttons, 15, 'bold'))
            self.buttons[but].pack(side='left',
                                   padx=15)
        self.buttons['Salvar'].configure(command=self.handle_save_button)

        self.button_back = tk.Button(master=self,
                                     text='◄',
                                     font=(std.font_title, 20, 'bold'),
                                     bg=std.bg,
                                     bd=0,
                                     fg=std.label_color,
                                     command=self.handle_back_button,
                                     activebackground='#555A5C')
        self.button_back.bind('<Enter>', self.on_hover)
        self.button_back.bind('<Leave>', self.on_leave)
        self.button_back.place(x=0, y=0)

        self.open_experiment()

    def open_experiment(self):
        print(self.experiment)
        self.entry_of_options['Desnaturação Temperatura'] \
            .insert(0, self.experiment.denaturation_c)
        self.entry_of_options['Desnaturação Tempo'] \
            .insert(0, self.experiment.denaturation_t)
        self.entry_of_options['Anelamento Temperatura'] \
            .insert(0, self.experiment.annealing_c)
        self.entry_of_options['Anelamento Tempo'] \
            .insert(0, self.experiment.annealing_t)
        self.entry_of_options['Extensão Temperatura'] \
            .insert(0, self.experiment.extension_c)
        self.entry_of_options['Extensão Tempo'] \
            .insert(0, self.experiment.extension_t)
        self.entry_of_options['Nº de ciclos'] \
            .insert(0, self.experiment.number_cycles)
        self.entry_of_options['Temperatura Final'] \
            .insert(0, self.experiment.final_temp)

    def on_hover(self, event=None):
        self.button_back['bg'] = std.bd

    def on_leave(self, event=None):
        self.button_back['bg'] = std.bg

    def handle_save_button(self):
        self.experiment.denaturation_c = \
            self.entry_of_options['Desnaturação Temperatura'].get()
        self.experiment.denaturation_t = \
            self.entry_of_options['Desnaturação Tempo'].get()
        self.experiment.annealing_c = \
            self.entry_of_options['Anelamento Temperatura'].get()
        self.experiment.annealing_t = \
            self.entry_of_options['Anelamento Tempo'].get()
        self.experiment.extension_c = \
            self.entry_of_options['Extensão Temperatura'].get()
        self.experiment.extension_t = \
            self.entry_of_options['Extensão Tempo'].get()
        self.experiment.number_cycles = \
            self.entry_of_options['Nº de ciclos'].get()
        self.experiment.final_temp = \
            self.entry_of_options['Temperatura Final'].get()
        functions.dump_pickle(std.exp_path, functions.experiments)
        messagebox.showinfo('Cetus PCR', 'Experimento salvo!', parent=self)

    def handle_back_button(self):
        newroot = tk.Tk()
        new = CetusPCR(newroot)
        new.widgets()
        self.close_window()
