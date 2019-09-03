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

import _thread as thread
import tkinter as tk
from tkinter import ttk, messagebox

# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.animation import FuncAnimation

import constants as std
import functions as fc

cetus_device = fc.ArduinoPCR(baudrate=9600, timeout=0.1)


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
                self.master.master.hover_box.configure(
                    text=self.hover_text)

    def on_leave(self, event):
        """Altera o ícone do botão quando o cursor saí da sua área."""
        if self['state'] == 'normal':
            self.configure(image=self.icon1)
            self.master.master.hover_box.configure(
                text=std.hover_texts['default'])


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

        self.switch_frame(CetusWindow)
        self.connected_icon = tk.PhotoImage(file='assets/connected_icon.png')
        self.check_if_is_connected()
        self.experiment_thread = None

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
        self.after(250, self.check_if_is_connected)


class CetusWindow(tk.Frame):
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
        self.master.title('Cetus PCR')
        self.master.iconbitmap(std.WINDOW_ICON)
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.pack(expand=1, fill='both')
        self.pack_propagate(False)
        self.master.focus_force()

        self.create_widgets = self._widgets

        self.logo = tk.PhotoImage(file=std.LOGO_IMAGE_PATH)
        self.logo_bg = tk.Label(master=self,
                                image=self.logo,
                                bg=std.BG)
        self.logo_bg.place(x=550, y=200)

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
                                           activebackground=std.SIDE_BAR_COLOR,
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

    def _widgets(self):
        """Cria os widgets específicos da janela.

        Esses widgets são colocados em outro método pois eles não podem
        herdados pelas outras janelas. O método é sobrescrito em cada
        nova sub-classe.
        """

        self.buttons_frame = tk.Frame(master=self,
                                      width=850,
                                      height=120,
                                      bg=std.BG,
                                      bd=0,
                                      highlightcolor=std.BD,
                                      highlightbackground=std.BD,
                                      highlightthickness=std.BD_WIDTH)
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

    def handle_home_button(self):
        self.master.index_exp = None
        self.master.switch_frame(CetusWindow)

    @staticmethod
    def handle_info_button():
        if not InfoWindow.is_open:
            InfoWindow(tk.Tk())

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
            self.master.switch_frame(ExperimentWindow, index)

    def handle_new_button(self):
        name = fc.ask_string('Novo Experimento', 'Digite o nome do'
                                                 ' experimento:',
                             parent=self.master)
        new_experiment = fc.ExperimentPCR(name)

        if new_experiment.name != '' and new_experiment.name is not None:
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

    def close_window(self):
        """Função para sobrescrever o protocolo padrão ao fechar a janela.

        O programa salva todos os experimentos em arquivo externo e depois
        destrói a janela principal encerrando o programa.
        """
        fc.save_pickle_file(std.EXP_PATH, fc.experiments)
        if cetus_device.is_connected:
            cetus_device.is_connected = False
            cetus_device.serial_device.close()
            print('Closing serial port.')
        self.master.destroy()


class ExperimentWindow(CetusWindow):
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
        self.experiment: fc.ExperimentPCR = fc.experiments[exp_index]
        self.vcmd = self.master.register(fc.validate_entry)
        cetus_device.experiment = self.experiment
        self.logo_bg.place_forget()

        self.title = tk.Label(master=self,
                              font=(std.FONT_TITLE, 39, 'bold'),
                              fg=std.TEXTS_COLOR,
                              bg=std.TOP_BAR_COLOR,
                              text=self.experiment.name)
        self.title.place(rely=0,
                         x=80,
                         y=10)

    def _widgets(self):
        self.entry_of_options = {}
        self.gapy = 20
        for stage in ('Desnaturação', 'Anelamento', 'Extensão'):
            self.gapx = 20
            for option in ('Temperatura', 'Tempo'):
                entry = tk.Entry(master=self,
                                 font=(std.FONT_ENTRY, 30),
                                 width=3,
                                 bd=1,
                                 highlightcolor=std.BD,
                                 highlightthickness=std.BD_WIDTH,
                                 validate='key',
                                 validatecommand=(self.vcmd, '%P'))
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
                                      fg=std.TEXTS_COLOR,
                                      bg=std.BG,
                                      font=(std.FONT_ENTRY_TITLE, 14, 'bold'))
                unit_label.place(in_=entry,
                                 relx=1,
                                 rely=0,
                                 x=10)
            self.gapy += 120
            label = tk.Label(master=self,
                             font=(std.FONT_ENTRY_TITLE, 20, 'bold'),
                             text=f'{stage}:',
                             bg=std.BG,
                             fg=std.TEXTS_COLOR)
            label.place(in_=self.entry_of_options[f'{stage} Temperatura'],
                        anchor='sw',
                        y=-10,
                        bordermode='outside')

        self.gapy = 20

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
                        rely=0.2,
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

        self.buttons_frame = tk.Frame(master=self,
                                      width=230,
                                      height=120,
                                      bg=std.BG,
                                      bd=0,
                                      relief=std.RELIEF,
                                      highlightcolor=std.BD,
                                      highlightbackground=std.BD,
                                      highlightthickness=std.BD_WIDTH)
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
        if len(self.experiment.steps) > 0:
            self.open_experiment()

    def open_experiment(self):
        self.entry_of_options['Nº de ciclos']. \
            insert(0, self.experiment.n_cycles)
        self.entry_of_options['Temperatura Final']. \
            insert(0, self.experiment.final_hold)

        for step in self.experiment.steps:
            self.entry_of_options[f'{step.name} Temperatura']. \
                insert(0, step.temperature)
            self.entry_of_options[f'{step.name} Tempo']. \
                insert(0, step.duration)
        print(self.experiment)

    def save_experiment(self):
        self.experiment.n_cycles = self.entry_of_options['Nº de ciclos'].get()
        self.experiment.final_hold = \
            self.entry_of_options['Temperatura Final'].get()
        self.experiment.steps = []
        for step in ('Desnaturação', 'Anelamento', 'Extensão'):
            self.experiment.add_step(step,
                                     self.entry_of_options[
                                         f'{step} Temperatura'].get(),
                                     self.entry_of_options[
                                         f'{step} Tempo'].get())

        fc.save_pickle_file(std.EXP_PATH, fc.experiments)

    def handle_save_button(self):
        self.save_experiment()
        messagebox.showinfo('Cetus PCR', 'Experimento salvo :)', parent=self)

    def handle_back_button(self):
        self.master.index_exp = None
        self.master.switch_frame(CetusWindow)

    def handle_run_button(self):
        if cetus_device.is_connected:
            self.save_experiment()
            cetus_device.is_running = True
            self.master.experiment_thread = \
                thread.start_new_thread(cetus_device.run_experiment, ())
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
        cetus_device.elapsed_time = 0

    def _widgets(self):
        self.data = {}
        gapx, gapy = 0, 0
        line1 = ['Temperatura Amostra', 'Tempo Est. Restante', 'Ciclo Atual']
        line2 = ['Temperatura Tampa', 'Tempo Decorrido', 'Passo Atual']
        for label1, label2 in zip(line1, line2):
            new_label1 = tk.Label(master=self,
                                  text=label1,
                                  bg=std.BG,
                                  fg=std.TEXTS_COLOR,
                                  font=(std.FONT_TITLE, 20, 'bold'))
            new_label1.place(relx=0.1,
                             rely=0.2,
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

            gapy += 200
            new_label2 = tk.Label(master=self,
                                  text=label2,
                                  bg=std.BG,
                                  fg=std.TEXTS_COLOR,
                                  font=(std.FONT_TITLE, 20, 'bold'))
            new_label2.place(in_=new_label1,
                             relx=0.5,
                             anchor='n',
                             y=gapy)
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
            gapy = 0

        self.frame1 = tk.Frame(master=self)
        self.frame1.place(relx=0.9,
                          rely=0.8,
                          x=-30,
                          y=15,
                          anchor='center')

        self.cancel_button = MyButton(master=self.frame1,
                                      relief=std.RELIEF,
                                      command=self.handle_cancel_button,
                                      image1=std.cetuspcr_buttons_path[
                                          'delete_icon'],
                                      image2=std.cetuspcr_buttons_path[
                                          'delete_highlight'],
                                      hover_text=std.hover_texts['cancel'],
                                      activebackground=std.BG,
                                      width=75,
                                      bd=0,
                                      bg=std.BG,
                                      highlightthickness=0)

        self.cancel_button.pack()
        self.update_labels()

    def update_labels(self):
        cur_cycle = f'{cetus_device.current_cycle}/{self.experiment.n_cycles}'
        self.current_estimated_time = self.experiment.estimated_time - \
                                      cetus_device.elapsed_time
        self.data['temperatura amostra']. \
            configure(text=f'{cetus_device.current_sample_temperature}°C')
        self.data['temperatura tampa']. \
            configure(text=f'{cetus_device.current_lid_temperature}°C')
        self.data['tempo est. restante']. \
            configure(text=fc.seconds_to_string(self.current_estimated_time))
        self.data['tempo decorrido']. \
            configure(text=fc.seconds_to_string(cetus_device.elapsed_time))
        self.data['passo atual']. \
            configure(text=cetus_device.current_step,
                      font=(std.FONT_TITLE, 21, 'bold'))
        self.data['ciclo atual']. \
            configure(text=cur_cycle)
        self.after(50, self.update_labels)

    def handle_cancel_button(self):
        cetus_device.is_running = False
        cetus_device.elapsed_time = 0
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

        # O mestre de todos os outros widgets deve ser o self.main_frame

    def close_window(self):
        InfoWindow.is_open = False
        self.master.destroy()
