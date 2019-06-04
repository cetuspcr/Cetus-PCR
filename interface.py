"""Design para o aplicativo Cetus PCR.

"interface.py" armazena todas as informações sobre os widgets do
aplicativo.

A estrutura principal do programa é baseada principalmente nessas duas
classes:
class CetusPCR -> Seleciona/Cria um experimento;
class ExperimentPCR -> Edita/Executa o experimento selecionado;
class MonitorPCR -> Monitora o experimento ativo.

Todas as classes de janelas são herdadas da biblioteca tk.Frame.
Isso é feito apenas por propósitos de design, uma vez que facilita a
colocação das bordas e organização dos widgets dentro da janela.

Todos os métodos com prefixo "handle" remetem as funções de botões.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import constants as std
import functions


class MyButton(tk.Button):
    """Botão modificado para alternar entre 2 ícones.

    O caminho dos ícones é fornecido ao método __init__, após isso os 2
    objetos de imagens são criados e o tk.Button gera o objeto de botão
    do Tkinter.

    Por fim, on_hover e on_leave são anexadas ao botão.
    """

    def __init__(self, master, image1, image2, hover_text=None, **kw):
        self.icon1 = tk.PhotoImage(file=image1)
        self.icon2 = tk.PhotoImage(file=image2)
        super().__init__(master=master, image=self.icon1, **kw)
        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_leave)
        self.hover_text = hover_text

    def on_hover(self, event):
        """Altera o ícone do botão quando o cursor entra em sua área.

        Se o botão possuí texto de instrução, ele é exibido na barra
        inferior.
        """
        self.configure(image=self.icon2)
        if self.hover_text is not None:
            self.master.master.hover_box.configure(text=self.hover_text)

    def on_leave(self, event):
        """Altera o ícone do botão quando o cursor saí da sua área."""
        self.configure(image=self.icon1)
        self.master.master.hover_box.configure(text=std.hover_text)


cetus_device = functions.ArduinoPCR(baudrate=9600, timeout=1)


class BaseWindow(tk.Tk):
    """Janela que exibe os widgets ativos de acordo com a classe dada.

    Essa janela é preparada para receber qualquer objeto da classe
    tk.Frame e exibir o seu conteúdo.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.configure(width=1000, height=660)
        self.resizable(False, False)
        self.switch_frame(CetusPCR)
        self.connected_icon = tk.PhotoImage(file='assets/connected_icon.png')
        self.check_if_is_connected()

    def switch_frame(self, new_frame, index_exp=None):
        """Função para trocar o conteúdo exibido pela na janela.

        :param new_frame: nova classe ou subclasse da tk.Frame a ser
        exibida.
        :param index_exp: existem janelas que lidam com um experimento
        específico, nesse caso o endereço do mesmo deve ser fornecido.
        """

        if index_exp is not None:
            new_frame = new_frame(self, index_exp)
        else:
            new_frame = new_frame(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        self._frame.create_widgets()

    def check_if_is_connected(self):
        """Função para verificar alterações na porta serial.

        Essa função roda em looping infinito no background da janela
        base.
        """
        if self._frame is not None:
            if cetus_device.is_connected:
                self._frame.side_buttons['reconnect_icon']. \
                    configure(image=self.connected_icon)
        if cetus_device.waiting_update:
            self._frame.side_buttons['reconnect_icon']. \
                configure(
                image=self._frame.side_buttons['reconnect_icon'].icon1)
            cetus_device.waiting_update = False
        self.after(1, self.check_if_is_connected)


class CetusPCR(tk.Frame):
    """Primeira janela do aplicativo.

    Nessa janela o usuário pode selecionar, deletar ou criar um
    experimento.
    """

    def __init__(self, master: BaseWindow):
        # Configurações da janela master.
        super().__init__(master,
                         width=1000,
                         height=660,
                         bg=std.bg,
                         bd=0)
        self.master = master
        self.master.geometry('+200+10')
        self.master.title('Cetus PCR')
        self.master.iconbitmap(std.window_icon)
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.pack()
        self.pack_propagate(False)
        self.master.focus_force()

        self.create_widgets = self._widgets

        # Barra inferior para exibir informações sobre os botões.
        self.hover_box = tk.Label(master=self,
                                  text=std.hover_text,
                                  bg='white',
                                  font=('Arial', 11, 'italic'),
                                  anchor='w')

        self.hover_box.pack(side='bottom',
                            fill='x')

        # Barra para os botões laterais.
        self.side_bar_frame = tk.Frame(master=self,
                                       bg=std.side_bar_color)
        self.side_bar_frame.pack(side='left', fill='y')
        self.side_bar_width = 55

        # Barra superior com a logo e o nome do experimento aberto.
        self.top_bar_frame = tk.Frame(master=self,
                                      height=65,
                                      bg=std.top_bar_color)
        self.top_bar_frame.pack(side='top', fill='x')
        self.top_bar_frame.pack_propagate(False)

        self.logo = tk.PhotoImage(file=std.logo_image_path).subsample(2)

        self.logo_label = tk.Label(master=self.top_bar_frame,
                                   bg=std.top_bar_color,
                                   image=self.logo)
        self.logo_label.pack(side='right', padx=10)

        # Criar os botões da barra lateral
        self.side_buttons = {}
        for but in std.side_buttons_path:
            if '_icon' in but:
                self.path_slice = but.split('_')
                self.b_name = self.path_slice[0]
                self.path1 = std.side_buttons_path[but]
                self.path2 = std.side_buttons_path[f'{self.b_name}_highlight']
                self.new_button = MyButton(master=self.side_bar_frame,
                                           image1=self.path1,
                                           image2=self.path2,
                                           width=self.side_bar_width + 10,
                                           activebackground=std.side_bar_color,
                                           bd=0,
                                           bg=std.side_bar_color,
                                           hover_text=std.hover_texts[
                                               self.b_name])

                self.side_buttons[but] = self.new_button
                if but != 'home_icon':
                    self.new_button.pack(side='bottom', pady=3)
                else:
                    self.new_button.pack(side='top', pady=3)
        self.side_buttons['home_icon']. \
            configure(command=self.handle_home_button)
        self.side_buttons['info_icon']. \
            configure(command=self.handle_info_button)
        self.side_buttons['cooling_icon']. \
            configure(command=self.handle_cooling_button)
        self.side_buttons['reconnect_icon']. \
            configure(command=self.handle_reconnect_button)
        self.side_buttons['settings_icon']. \
            configure(command=self.handle_settings_button)

    def _widgets(self):
        """Cria os widgets específicos da janela.

        Esses widgets são colocados em outro método pois eles não podem
        herdados pelas outras janelas. O método é sobrescrito em cada
        nova sub-classe.
        """

        self.buttons_frame = tk.Frame(master=self,
                                      width=850,
                                      height=120,
                                      bg=std.bg,
                                      bd=0,
                                      highlightcolor=std.bd,
                                      highlightbackground=std.bd,
                                      highlightthickness=std.bd_width)
        self.buttons_frame.place(rely=0.50,
                                 relx=0.10,
                                 anchor='w')
        self.buttons_frame.pack_propagate(False)

        self.buttons = {}
        # Criar e posicionar os botões dentro do "options_frame"
        for but in std.cetuspcr_buttons_path:
            if '_icon' in but:
                self.path_slice = but.split('_')
                self.b_name = self.path_slice[0]
                self.path1 = std.cetuspcr_buttons_path[but]
                self.path2 = std.cetuspcr_buttons_path[
                    f'{self.path_slice[0]}_highlight']
                self.new_button = MyButton(master=self.buttons_frame,
                                           image1=self.path1,
                                           image2=self.path2,
                                           activebackground=std.bg,
                                           width=75,
                                           bd=0,
                                           bg=std.bg,
                                           highlightthickness=0,
                                           hover_text=std.hover_texts[self.b_name])

                self.buttons[but] = self.new_button
                self.buttons[but].pack(side='right', padx=8)
        self.buttons['confirm_icon']. \
            configure(command=self.handle_confirm_button)
        self.buttons['add_icon']. \
            configure(command=self.handle_new_button)
        self.buttons['delete_icon']. \
            configure(command=self.handle_delete_button)

        self.experiment_combo = ttk.Combobox(master=self.buttons_frame,
                                             width=35,
                                             font=(std.font_title, 17))
        self.experiment_combo.place(rely=0.55,
                                    relx=0.02,
                                    anchor='w',
                                    bordermode='inside')

        self.experiment_combo_title = tk.Label(master=self,
                                               font=(std.font_title, 22,
                                                     'bold'),
                                               text='Selecione o experimento:',
                                               fg=std.texts_color,
                                               bg=std.bg)

        self.experiment_combo_title.place(in_=self.experiment_combo,
                                          anchor='sw',
                                          bordermode='outside')

        self.show_experiments()

    def show_experiments(self):
        """Abre o arquivo com os experimentos salvos e os exibe na
        self.experiment_combo(ttk.Combobox).
        """
        functions.experiments = functions.open_pickle(std.exp_path)
        self.experiment_combo.configure(values=functions.experiments)

    def handle_home_button(self):
        self.master.index_exp = None
        self.master.switch_frame(CetusPCR)

    # Ainda não implementado.
    def handle_info_button(self):
        pass

    # Ainda não implementado.
    def handle_cooling_button(self):
        pass

    @staticmethod
    def handle_reconnect_button():
        if not cetus_device.is_connected:
            cetus_device.initialize_connection()
            port = cetus_device.port_connected
            if cetus_device.is_connected:
                messagebox.showinfo('Cetus PCR',
                                    'Dispositivo conectado com sucesso na '
                                    f'porta "{port}"')
            else:
                messagebox.showerror('Cetus PCR',
                                     'Conexão mal-sucedida.')
        else:
            messagebox.showinfo('Cetus PCR',
                                'O Dispositivo já está conectado '
                                f'({cetus_device.port_connected}).')

    # Ainda não implementado.
    def handle_settings_button(self):
        pass

    def handle_confirm_button(self):
        index = self.experiment_combo.current()
        if index >= 0:
            self.master.index_exp = index
            self.master.switch_frame(ExperimentPCR, index)

    def handle_new_button(self):
        new_experiment = functions.Experiment()
        name = functions.ask_string('Novo Experimento', 'Digite o nome do'
                                                        ' experimento:',
                                    parent=self.master)
        new_experiment.name = name

        if new_experiment.name != '' and new_experiment.name is not None:
            functions.experiments.append(new_experiment)
            functions.dump_pickle(std.exp_path, functions.experiments)
            self.experiment_combo.configure(values=functions.experiments)

            self.master.index_exp = functions.experiments.index(new_experiment)
            self.master.switch_frame(ExperimentPCR)

        elif name is '':
            messagebox.showerror('Novo Experimento', 'O nome não pode estar'
                                                     ' vazio')

    def handle_delete_button(self):
        index = self.experiment_combo.current()
        experiment = functions.experiments[index]
        if index >= 0:
            delete = messagebox. \
                askyesnocancel('Deletar experimento',
                               'Você tem certeza que deseja '
                               f'excluir "{experiment.name}"?\n'
                               'Essa ação não pode ser desfeita.')
            if delete:
                functions.experiments.remove(experiment)
                functions.dump_pickle(std.exp_path, functions.experiments)
                self.experiment_combo.configure(values=functions.experiments)
                self.experiment_combo.delete(0, 'end')

    def close_window(self):
        """Função para sobrescrever o protocolo padrão ao fechar a janela.

        O programa salva todos os experimentos em arquivo externo e depois
        destrói a janela principal encerrando o programa.
        """
        functions.dump_pickle(std.exp_path, functions.experiments)
        self.master.destroy()


class ExperimentPCR(CetusPCR):
    """Lida com o experimento dado pela janela CetusPCR.

    Essa janela é composto por alguns widgets da classe tk.Entry.

    Herdar do CetusPCR cria automaticamente uma janela com as mesmas
    configurações de quadro.
    Isso é util pois a janela deve ter a mesma aparência, título, ícone
    e tamanho, porém, com widgets e opções diferentes.

    As barras lateral, superior e inferior também são herdadas.
    """

    def __init__(self, master: BaseWindow, exp_index):
        super().__init__(master)
        self.exp_index = exp_index
        self.experiment = functions.experiments[exp_index]
        self.vcmd = self.master.register(functions.validate_entry)
        cetus_device.experiment = self.experiment

    def _widgets(self):
        self.title = tk.Label(master=self,
                              font=(std.font_title, 39, 'bold'),
                              fg=std.texts_color,
                              bg=std.top_bar_color,
                              text=self.experiment.name)
        self.title.place(rely=0,
                         relx=0.1)

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
                                      fg=std.texts_color,
                                      bg=std.bg,
                                      font=(std.font_title, 14, 'bold'))
                unit_label.place(in_=entry,
                                 relx=1,
                                 rely=0,
                                 x=10)
            self.gapy += 120
            label = tk.Label(master=self,
                             font=(std.font_title, 20, 'bold'),
                             text=stage + ':',
                             bg=std.bg,
                             fg=std.texts_color)
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
                             text=option + ':',
                             fg=std.texts_color,
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
                                      fg=std.texts_color)
                unit_label.place(in_=entry,
                                 relx=1,
                                 rely=0,
                                 x=10)

        self.buttons_frame = tk.Frame(master=self,
                                      width=230,
                                      height=120,
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
        self.buttons_frame.pack_propagate(False)
        self.buttons = {}
        for but in std.experimentpcr_buttons_path:
            if '_icon' in but:
                self.path_slice = but.split('_')
                self.b_name = self.path_slice[0]
                self.path1 = std.experimentpcr_buttons_path[but]
                self.path2 = std.experimentpcr_buttons_path[
                    f'{self.path_slice[0]}_highlight']
                self.new_button = MyButton(master=self.buttons_frame,
                                           image1=self.path1,
                                           image2=self.path2,
                                           activebackground=std.bg,
                                           width=75,
                                           bd=0,
                                           bg=std.bg,
                                           highlightthickness=0,
                                           hover_text=std.hover_texts[self.b_name])

                self.buttons[but] = self.new_button
                self.buttons[but].pack(side='left',
                                       padx=17)
        self.buttons['save_icon'].configure(command=self.handle_save_button)
        self.buttons['run_icon'].configure(command=self.handle_run_button)

        self.open_experiment()

    def open_experiment(self):
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
        messagebox.showinfo('Cetus PCR',
                            f'"{self.experiment.name}" salvo :]', parent=self)

    def handle_back_button(self):
        self.master.index_exp = None
        self.master.switch_frame(CetusPCR)

    def handle_run_button(self):
        if cetus_device.is_connected:
            cetus_device.run_experiment()
            self.master.switch_frame(MonitorPCR, self.exp_index)
        else:
            messagebox.showerror('Executar Experimento',
                                 'Dispositivo Cetus PCR não conectado!',
                                 parent=self)


class MonitorPCR(ExperimentPCR):

    def __init__(self, master: BaseWindow, exp_index):
        super().__init__(master, exp_index)

    def _widgets(self):
        self.title = tk.Label(master=self,
                              text=self.experiment.name,
                              fg=std.bd,
                              bg=std.bg,
                              font=(std.font_title, 35, 'bold'))
        self.title.pack()

        self.info_label = tk.Label(master=self,
                                   text=cetus_device.reading,
                                   fg='white',
                                   bg=std.bg,
                                   font=(std.font_title, 25, 'bold'))
        self.info_label.pack()
        self.update_text()

    def update_text(self):
        self.info_label.configure(text=f'Value: {cetus_device.reading}')
        self.after(1, self.update_text)
