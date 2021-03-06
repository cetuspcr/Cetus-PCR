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
from threading import Thread
from tkinter import ttk, messagebox
from time import sleep

import functions as fc
import constants as std


class AnimatedButton(tk.Button):
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
        self.master = master
        self.hover_text = hover_text

    def on_hover(self, event):
        """Altera o ícone do botão quando o cursor entra em sua área.

        Se o botão possuí texto de instrução, ele é exibido na barra
        inferior.
        """

        if self['state'] == 'normal':
            self.configure(image=self.icon2)
            if self.hover_text is not None:
                cetus.hover_box.configure(
                    text=self.hover_text)

    def on_leave(self, event):
        """Altera o ícone do botão quando o cursor saí da sua área."""
        if self['state'] == 'normal':
            self.configure(image=self.icon1)
            cetus.hover_box.configure(
                text=std.hover_texts['default'])


class ScrollFrame(tk.Frame):
    """Um frame customizado com uma barra de rolagem vertical.

    Créditos ao mp035 no GitHub Gist.
    """

    def __init__(self, master, **kw):
        super().__init__(master, **kw)  # create a frame (self)

        self.canvas = tk.Canvas(self,
                                borderwidth=0,
                                height=450,
                                width=350,
                                **kw)
        self.viewPort = tk.Frame(self.canvas, **kw)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right",
                      fill="y")
        self.canvas.pack(side="left", fill="both",
                         expand=True)
        self.canvas.create_window((10, 4), window=self.viewPort, anchor="nw",
                                  # add view port frame to canvas
                                  tags="self.viewPort")

        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self.on_frame_configure)
        self.update_scroll_bar()

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        # whenever the size of the frame changes, alter the scroll region.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_scroll_bar(self):
        if StepWidget.n_steps < 5:
            self.vsb.forget()
        else:
            self.vsb.pack(side="right",
                          fill="y")


class StepWidget(tk.Frame):
    """Um frame padrão para adicionar informações aos experimentos. """

    n_steps = 0

    def __init__(self, master, step_name, **kw):
        tk.Frame.__init__(self, master=master, **kw)
        self.configure(width=250, height=100, bg=std.BG)
        self.vcmd = self.master.register(fc.validate_entry)
        self.master = master

        self.step_name = step_name
        self.label_name = tk.Label(master=self,
                                   font=(std.FONT_ENTRY_TITLE, 20, 'bold'),
                                   text=f'{self.step_name}:',
                                   bg=std.BG,
                                   fg=std.TEXTS_COLOR)
        self.label_name.pack(side='top', anchor='nw')
        self.entry_temp = tk.Entry(master=self,
                                   font=(std.FONT_ENTRY, 30),
                                   width=3,
                                   bd=1,
                                   highlightcolor=std.BD,
                                   highlightthickness=std.BD_WIDTH,
                                   validate='key',
                                   validatecommand=(self.vcmd, '%P'))
        self.entry_temp.pack(side='left',
                             pady=10)
        tk.Label(master=self,
                 font=(std.FONT_ENTRY_TITLE, 14, 'bold'),
                 text='°C',
                 bg=std.BG,
                 fg=std.TEXTS_COLOR).place(in_=self.entry_temp,
                                           relx=1,
                                           rely=0,
                                           x=10)

        self.entry_time = tk.Entry(master=self,
                                   font=(std.FONT_ENTRY, 30),
                                   width=3,
                                   bd=1,
                                   highlightcolor=std.BD,
                                   highlightthickness=std.BD_WIDTH,
                                   validate='key',
                                   validatecommand=(self.vcmd, '%P'))
        self.entry_time.pack(side='left',
                             padx=50,
                             pady=10)
        tk.Label(master=self,
                 font=(std.FONT_ENTRY_TITLE, 14, 'bold'),
                 text='Seg',
                 bg=std.BG,
                 fg=std.TEXTS_COLOR).place(in_=self.entry_time,
                                           relx=1,
                                           rely=0,
                                           x=10)

        self.remove_image = tk.PhotoImage(file='assets/remove_icon.png')
        self.remove_button = tk.Button(master=self,
                                       image=self.remove_image,
                                       command=self.remove_widget_step,
                                       bg=std.BG,
                                       relief=std.RELIEF,
                                       bd=0,
                                       highlightthickness=0,
                                       activebackground=std.BG)
        self.remove_button.pack(side='left', padx=15)
        StepWidget.n_steps += 1

    @classmethod
    def create_from_step_class(cls, master, step: fc.StepPCR):
        new_widget = cls(master=master, step_name=step.name)
        new_widget.entry_temp.insert(0, step.temperature)
        new_widget.entry_time.insert(0, step.duration)
        return new_widget

    def get_step(self):
        return fc.StepPCR(self.step_name, self.entry_temp.get(),
                          self.entry_time.get())

    def remove_widget_step(self):
        self.master.master.master.master.step_widgets_data.remove(self)
        StepWidget.n_steps -= 1
        self.forget()
        self.master.master.master.update_scroll_bar()


class BaseWindow(tk.Tk):
    """Janela que exibe os widgets ativos de acordo com a classe dada.

    Essa janela é preparada para receber qualquer objeto da classe
    tk.Frame e exibir o seu conteúdo.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry('1050x660+200+10')
        self.resizable(False, False)
        self.title('Cetus PCR')
        self.iconbitmap(std.WINDOW_ICON)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.configure(bg=std.BG)
        self.focus_force()

        # Barra inferior para exibir informações sobre os botões.
        self.hover_box = tk.Label(master=self,
                                  text=std.hover_texts['default'],
                                  bg='white',
                                  font=(std.FONT_HOVER, 11),
                                  anchor='w')

        self.hover_box.pack(side='bottom',
                            fill='x')

        # Barra para os botões laterais.
        self.side_bar_frame = tk.Frame(master=self,
                                       bg=std.SIDE_BAR_COLOR)
        self.side_bar_frame.pack(side='left', fill='y')
        self.side_bar_width = 55

        # Barra superior com a logo e o nome do experimento aberto.
        self.top_bar_frame = tk.Frame(master=self,
                                      height=78,
                                      bg=std.TOP_BAR_COLOR)
        self.top_bar_frame.pack(side='top', fill='x')
        self.top_bar_frame.pack_propagate(False)

        self.header = tk.PhotoImage(file=std.HEADER_IMAGE_PATH).subsample(2)

        self.header_label = tk.Label(master=self.top_bar_frame,
                                     bg=std.TOP_BAR_COLOR,
                                     image=self.header)
        self.header_label.pack(side='right', padx=10)

        self.title_experiment = tk.Label(master=self.top_bar_frame,
                                         font=(std.FONT_TITLE, 39, 'bold'),
                                         fg=std.TEXTS_COLOR,
                                         bg=std.TOP_BAR_COLOR)
        self.title_experiment.place(rely=0,
                                    x=5,
                                    y=7)

        # Criar os botões da barra lateral
        self.side_buttons = {}
        for but in std.side_buttons_path:
            if '_icon' in but:
                self.path_slice = but.split('_')
                self.b_name = self.path_slice[0]
                self.path1 = std.side_buttons_path[but]
                self.path2 = std.side_buttons_path[f'{self.b_name}_highlight']
                self.new_button = AnimatedButton(master=self.side_bar_frame,
                                                 image1=self.path1,
                                                 image2=self.path2,
                                                 width=
                                                 self.side_bar_width + 10,
                                                 activebackground=
                                                 std.SIDE_BAR_COLOR,
                                                 bd=0,
                                                 bg=std.SIDE_BAR_COLOR,
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

        self.switch_frame(HomeWindow)
        self.connected_icon = tk.PhotoImage(file='assets/connected_icon.png')
        self.check_if_is_connected()
        self.experiment_thread = None

    def check_if_is_connected(self):
        """Função para verificar alterações na porta serial.

        Essa função roda em looping infinito no background da janela
        base.
        """
        bt_connected = self.side_buttons['reconnect_icon']
        if self._frame is not None and arduino.is_connected:
            bt_connected.icon1 = self.connected_icon
            bt_connected.icon2 = self.connected_icon
            bt_connected.configure(image=self.connected_icon)
        elif arduino.waiting_update:
            bt_connected.icon1 = tk.PhotoImage(
                file=std.side_buttons_path['reconnect_icon'])
            bt_connected.icon2 = tk.PhotoImage(
                file=std.side_buttons_path['reconnect_highlight'])
            bt_connected.configure(image=bt_connected.icon1)
            arduino.waiting_update = False

        self.after(1000, self.check_if_is_connected)

    def close_window(self):
        """Função para sobrescrever o protocolo padrão ao fechar a janela.

        O programa salva todos os experimentos em arquivo externo e depois
        destrói a janela principal encerrando o programa.
        """
        fc.save_pickle_file(std.EXP_PATH, fc.experiments)
        if arduino.is_connected:
            arduino.is_running = False
            arduino.is_connected = False
            arduino.serial_device.close()
            print('Closing serial port.')
        self.destroy()

    def switch_frame(self, new_frame, *args, **kwargs):
        """Função para trocar o conteúdo exibido pela na janela.

        :param new_frame: nova classe ou subclasse da tk.Frame a ser
        exibida.
        """

        new_frame = new_frame(self, *args, **kwargs)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        self._frame.create_widgets()

    # ---------------------------------- Métodos para funções de botão
    def handle_cooling_button(self):
        if not arduino.is_cooling:
            print('cooling')
            arduino.serial_device.write(b'<peltier 0 0>')
            sleep(1)
            if arduino.current_sample_temperature >= std.COOLING_TEMP_C:
                arduino.experiment = arduino.cooling_experiment
                arduino.is_cooling = True
                arduino.is_running = True
                self.experiment_thread = Thread(
                    target=arduino.run_experiment)
                self.experiment_thread.start()
                messagebox.showinfo('Cetus PCR', 'Processo de resfriamento '
                                                 'iniciado.')
            else:
                messagebox.showinfo('Cetus PCR', 'O Dispositivo já está resfriado.')
        else:
            arduino.serial_device.write(b'<printTemps>')
            messagebox.showinfo('Cetus PCR',
                                'Dispositivo resfriando.\n'
                                f'Temperatura atual: {arduino.current_sample_temperature}')

    def handle_home_button(self):
        self.title_experiment.configure(text='')
        self.switch_frame(HomeWindow)

    @staticmethod
    def handle_info_button():
        if not InfoWindow.is_open:
            InfoWindow(tk.Tk())

    @staticmethod
    def handle_reconnect_button():
        if not arduino.is_connected:
            arduino.initialize_connection()
            port = arduino.port_connected
            if arduino.is_connected:
                messagebox.showinfo('Cetus PCR',
                                    'Dispositivo conectado com sucesso na '
                                    f'porta "{port}"')
            else:
                messagebox.showerror('Cetus PCR',
                                     'Conexão mal-sucedida.')
        else:
            messagebox.showinfo('Cetus PCR',
                                'O Dispositivo já está conectado '
                                f'({arduino.port_connected}).')

    def handle_settings_button(self):
        pass


class HomeWindow(tk.Frame):
    """Primeira janela do aplicativo.

    Nessa janela o usuário pode selecionar, deletar ou criar um
    experimento.
    """

    def __init__(self, master: BaseWindow):
        # Configurações da janela master.
        super().__init__(master,
                         bg=std.BG,
                         bd=0)
        self.master = master
        self.pack(expand=1, fill='both')
        self.pack_propagate(False)

        self.create_widgets = self._widgets

    def _widgets(self):
        """Cria os widgets específicos da janela.

        Esses widgets são colocados em outro método pois eles não podem
        herdados pelas outras janelas. O método é sobrescrito em cada
        nova sub-classe.
        """
        self.logo = tk.PhotoImage(file=std.LOGO_IMAGE_PATH)
        self.logo_bg = tk.Label(master=self,
                                image=self.logo,
                                bg=std.BG)
        self.logo_bg.place(x=550, y=200)

        self.buttons_frame = tk.Frame(master=self,
                                      width=850,
                                      height=120,
                                      bg=std.BG,
                                      bd=0,
                                      highlightcolor=std.BD,
                                      highlightbackground=std.BD,
                                      highlightthickness=std.BD_WIDTH)
        self.buttons_frame.place(anchor='n',
                                 rely=0.30,
                                 relx=0.5,
                                 y=35)
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
                self.new_button = AnimatedButton(master=self.buttons_frame,
                                                 image1=self.path1,
                                                 image2=self.path2,
                                                 activebackground=std.BG,
                                                 width=75,
                                                 bd=0,
                                                 bg=std.BG,
                                                 highlightthickness=0,
                                                 hover_text=std.hover_texts[
                                                     self.b_name])

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
                                             font=(std.FONT_TITLE, 17))
        self.experiment_combo.place(rely=0.55,
                                    relx=0.02,
                                    anchor='w',
                                    bordermode='inside')

        self.experiment_combo_title = tk.Label(master=self,
                                               font=(std.FONT_TITLE, 22,
                                                     'bold'),
                                               text='Selecione o experimento:',
                                               fg=std.TEXTS_COLOR,
                                               bg=std.BG)

        self.experiment_combo_title.place(in_=self.experiment_combo,
                                          anchor='sw',
                                          bordermode='outside')

        self.show_experiments()

    def show_experiments(self):
        """Abre o arquivo com os experimentos salvos e os exibe na
        self.experiment_combo(ttk.Combobox).
        """
        fc.experiments = fc.open_pickle_file(std.EXP_PATH)
        values = []
        for exp in fc.experiments:
            values.append(exp.name)
        self.experiment_combo.configure(values=values)

    # ---------------------------------- Métodos para funções de botão
    def handle_confirm_button(self):
        index = self.experiment_combo.current()
        if index >= 0:
            self.master.index_exp = index
            self.master.switch_frame(ExperimentWindow, index)

    def handle_new_button(self):
        name = fc.ask_string('Novo Experimento', 'Digite o nome do'
                                                 ' experimento:',
                             parent=self.master)

        if name != '' and name is not None:
            new_experiment = fc.ExperimentPCR(name)
            fc.experiments.append(new_experiment)
            fc.save_pickle_file(std.EXP_PATH, fc.experiments)
            index_exp = fc.experiments.index(new_experiment)
            self.show_experiments()
            self.master.switch_frame(ExperimentWindow, index_exp)

        elif name is '':
            messagebox.showerror('Novo Experimento', 'O nome não pode estar'
                                                     ' vazio')

    def handle_delete_button(self):
        index = self.experiment_combo.current()
        experiment = fc.experiments[index]
        if index >= 0:
            delete = messagebox. \
                askyesnocancel('Deletar experimento',
                               'Você tem certeza que deseja '
                               f'excluir "{experiment.name}"?\n'
                               'Essa ação não pode ser desfeita.')
            if delete:
                fc.experiments.remove(experiment)
                fc.save_pickle_file(std.EXP_PATH, fc.experiments)
                self.show_experiments()
                self.experiment_combo.delete(0, 'end')


class ExperimentWindow(HomeWindow):
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
        self.master = master
        self.vcmd = self.master.register(fc.validate_entry)
        self.experiment: fc.ExperimentPCR = fc.experiments[exp_index]
        arduino.experiment = self.experiment
        self.step_widgets_data = []
        cetus.title_experiment.configure(text=self.experiment.name)

    def _widgets(self):
        self.entry_of_options = {}
        self.gapy = 50

        for option in ('Nº de ciclos', 'Temperatura Final'):
            key = option
            entry = tk.Entry(master=self,
                             font=(std.FONT_ENTRY, 30),
                             width=3,
                             bd=1,
                             highlightcolor=std.BD,
                             highlightthickness=std.BD_WIDTH,
                             validate='key',
                             validatecommand=(self.vcmd, '%P'))
            entry.place(relx=0.7,
                        rely=0.1,
                        y=self.gapy)
            self.gapy += 120
            self.entry_of_options[key] = entry

            label = tk.Label(master=self,
                             font=(std.FONT_ENTRY_TITLE, 20, 'bold'),
                             text=option + ':',
                             fg=std.TEXTS_COLOR,
                             bg=std.BG)
            label.place(in_=entry,
                        anchor='s',
                        relx=0.5,
                        y=-10)

            if option == 'Temperatura Final':
                unit_label = tk.Label(master=self,
                                      font=(std.FONT_ENTRY_TITLE, 14, 'bold'),
                                      text='°C',
                                      bg=std.BG,
                                      fg=std.TEXTS_COLOR)
                unit_label.place(in_=entry,
                                 relx=1,
                                 rely=0,
                                 x=10)
        self.frame_steps = ScrollFrame(master=self,
                                       bg=std.BG,
                                       bd=0,
                                       highlightthickness=0)
        self.frame_steps.place(relx=0.1,
                               rely=0.1)
        for step in ('Desnaturação', 'Anelamento', 'Extensão'):
            self.new_step = StepWidget(master=self.frame_steps.viewPort,
                                       step_name=step)
            self.new_step.pack(side='top')
            self.step_widgets_data.append(self.new_step)

        self.buttons_frame = tk.Frame(master=self,
                                      width=340,
                                      height=120,
                                      bg=std.BG,
                                      bd=0,
                                      relief=std.RELIEF,
                                      highlightcolor=std.BD,
                                      highlightbackground=std.BD,
                                      highlightthickness=std.BD_WIDTH)
        self.buttons_frame.place(in_=self.entry_of_options['Temperatura '
                                                           'Final'],
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
                self.new_button = AnimatedButton(master=self.buttons_frame,
                                                 image1=self.path1,
                                                 image2=self.path2,
                                                 activebackground=std.BG,
                                                 width=75,
                                                 bd=0,
                                                 bg=std.BG,
                                                 highlightthickness=0,
                                                 hover_text=std.hover_texts[
                                                     self.b_name])

                self.buttons[but] = self.new_button
                self.buttons[but].pack(side='left',
                                       padx=17)

        self.buttons['save_icon'].configure(command=self.handle_save_button)
        self.buttons['run_icon'].configure(command=self.handle_run_button)
        self.buttons['add_icon'].configure(command=self.handle_add_button)
        if len(self.experiment.steps) > 0:
            self.open_experiment()

    def open_experiment(self):
        self.entry_of_options['Nº de ciclos']. \
            insert(0, self.experiment.n_cycles)
        self.entry_of_options['Temperatura Final']. \
            insert(0, self.experiment.final_hold)
        for widget in self.step_widgets_data:
            widget.forget()
        self.step_widgets_data.clear()
        for step in self.experiment.steps:
            new = StepWidget.create_from_step_class(master=self.frame_steps.
                                                    viewPort,
                                                    step=step)
            new.pack(side='top')
            self.step_widgets_data.append(new)
        StepWidget.n_steps = len(self.step_widgets_data)
        self.frame_steps.update_scroll_bar()

    def save_experiment(self):
        self.experiment.n_cycles = self.entry_of_options['Nº de ciclos'].get()
        self.experiment.final_hold = \
            self.entry_of_options['Temperatura Final'].get()
        self.experiment.steps.clear()
        for widget in self.step_widgets_data:
            self.experiment.steps.append(widget.get_step())
        fc.save_pickle_file(std.EXP_PATH, fc.experiments)
        print(self.experiment)

    # ---------------------------------- Métodos para funções de botão
    def handle_add_button(self):
        step_name = fc.ask_string('Nova Etapa', 'Digite o nome do novo '
                                                'passo:')
        if step_name == '':
            messagebox.showerror('Nova Etapa', 'O nome da etapa não pode '
                                               'estar vazio')
        elif step_name is not None:
            new_step = StepWidget(master=self.frame_steps.viewPort,
                                  step_name=step_name)
            self.step_widgets_data.append(new_step)
            self.frame_steps.update_scroll_bar()
            new_step.label_name.configure(text=step_name + ':')
            new_step.pack()

    def handle_save_button(self):
        self.save_experiment()
        messagebox.showinfo('Cetus PCR', 'Experimento salvo :)', parent=self)

    def handle_back_button(self):
        self.master.index_exp = None
        self.master.switch_frame(HomeWindow)

    def handle_run_button(self):
        if arduino.is_connected:
            self.save_experiment()
            arduino.is_running = True
            self.master.experiment_thread = Thread(
                target=arduino.run_experiment)
            self.master.experiment_thread.start()
            self.master.switch_frame(MonitorWindow, self.exp_index)

        else:
            messagebox.showerror('Executar Experimento',
                                 'Dispositivo Cetus PCR não conectado!',
                                 parent=self)


class MonitorWindow(ExperimentWindow):

    def __init__(self, master: BaseWindow, exp_index):
        fc.experiments = fc.open_pickle_file(std.EXP_PATH)
        super().__init__(master, exp_index)
        self.master = master
        self.current_estimated_time = 0
        arduino.elapsed_time = 0

    def _widgets(self):
        self.data = {}
        gapx, gapy = 20, 0
        line1 = ['Temperatura Amostra', 'Temperatura Alvo', 'Ciclo Atual']
        line2 = ['Tempo Decorrido', 'Passo Atual']
        for label1 in line1:
            new_label1 = tk.Label(master=self,
                                  text=label1,
                                  bg=std.BG,
                                  fg=std.TEXTS_COLOR,
                                  font=(std.FONT_TITLE, 20, 'bold'))
            new_label1.place(relx=0.0,
                             rely=0.1,
                             x=gapx)
            new_value1 = tk.Label(master=self,
                                  font=(std.FONT_TITLE, 30, 'bold'),
                                  bg=std.BG,
                                  fg=std.TEXTS_COLOR)
            new_value1.place(in_=new_label1,
                             anchor='n',
                             rely=1,
                             y=30,
                             relx=0.5)
            self.data[label1.lower()] = new_value1

            gapx += 360

        gapx = 20
        for label2 in line2:
            new_label2 = tk.Label(master=self,
                                  text=label2,
                                  bg=std.BG,
                                  fg=std.TEXTS_COLOR,
                                  font=(std.FONT_TITLE, 20, 'bold'))
            new_label2.place(rely=0.5,
                             anchor='n',
                             relx=0.3,
                             x=gapx)
            new_value2 = tk.Label(master=self.master,
                                  font=(std.FONT_TITLE, 30, 'bold'),
                                  bg=std.BG,
                                  fg=std.TEXTS_COLOR)
            new_value2.place(in_=new_label2,
                             anchor='n',
                             rely=1,
                             y=30,
                             relx=0.5)
            self.data[label2.lower()] = new_value2
            gapx += 360

        # self.frame1 = tk.Frame(master=self)
        # self.frame1.place(relx=0.9,
        #                   rely=0.8,
        #                   x=-30,
        #                   y=15,
        #                   anchor='center')

        self.cancel_button = AnimatedButton(master=self,
                                            relief=std.RELIEF,
                                            command=self.handle_cancel_button,
                                            image1=std.cetuspcr_buttons_path[
                                                'delete_icon'],
                                            image2=std.cetuspcr_buttons_path[
                                                'delete_highlight'],
                                            hover_text=std.hover_texts[
                                                'cancel'],
                                            activebackground=std.BG,
                                            width=75,
                                            bd=0,
                                            bg=std.BG,
                                            highlightthickness=0)

        self.cancel_button.place(relx=0.8,
                                 rely=0.8,
                                 x=45,
                                 y=-10,
                                 anchor='center')
        self.update_labels()

    def update_labels(self):
        cur_cycle = f'{arduino.current_cycle}/{self.experiment.n_cycles}'
        self.data['temperatura amostra']. \
            configure(text=f'{arduino.current_sample_temperature} °C')
        # self.data['temperatura tampa']. \
        #     configure(text=f'{arduino.current_lid_temperature} °C')
        self.data['temperatura alvo']. \
            configure(text=f'{arduino.current_step_temp} °C')
        self.data['tempo decorrido']. \
            configure(text=fc.seconds_to_string(arduino.elapsed_time))
        self.data['passo atual']. \
            configure(text=arduino.current_step,
                      font=(std.FONT_TITLE, 21, 'bold'))
        self.data['ciclo atual']. \
            configure(text=cur_cycle)
        self.after(50, self.update_labels)

    # ---------------------------------- Métodos para funções de botão
    def handle_cancel_button(self):
        arduino.is_running = False
        arduino.elapsed_time = 0
        self.current_estimated_time = 0
        self.master.switch_frame(ExperimentWindow, self.exp_index)


class InfoWindow(tk.Frame):
    is_open = False

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.master.title('Cetus PCR')
        self.master.iconbitmap(std.WINDOW_ICON)
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        InfoWindow.is_open = True

        # Os dois primeiro valores ajustam o tamanho da janela, os dois
        # últimos ajustam a posição
        self.master.geometry('400x250+500+200')

        self.master.resizable(False, False)

        self.configure(bg=std.BG,
                       bd=0,
                       highlightcolor=std.BD,
                       highlightbackground=std.BD,
                       highlightthickness=std.BD_WIDTH)
        self.pack(expand=1,
                  fill='both')

    def close_window(self):
        InfoWindow.is_open = False
        self.master.destroy()


arduino = fc.ArduinoPCR(baudrate=9600, timeout=1)
fc.experiments = fc.open_pickle_file(std.EXP_PATH)
cetus = BaseWindow()
cetus.mainloop()
