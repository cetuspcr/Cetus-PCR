# Design gráfico; Geralmente nomeados com base nas constantes do tkinter.
bg = '#434343'
bd = '#2ecc71'
bd_width = 3
relief = 'flat'
texts_color = 'white'
side_bar_color = '#383838'
# top_bar_color = '#3f9b6b'
top_bar_color = '#529E76'
header_image_path = 'assets/header_cetus.png'
logo_image_path = 'assets/logo.png'

# Fontes
font_title = 'Courier New'
font_buttons = 'Arial'
font_hover = 'Arial'
font_entry_title = 'Courier New'
font_entry = 'Courier New'

# Ícones para interface em geral
window_icon = 'assets/cetus.ico'
side_buttons_path = {'home_icon': 'assets/home_icon.png',
                     'settings_icon': 'assets/settings_icon.png',
                     'reconnect_icon': 'assets/reconnect_icon.png',
                     'cooling_icon': 'assets/cooling_icon.png',
                     'info_icon': 'assets/info_icon.png',
                     'home_highlight': 'assets/home_highlight.png',
                     'settings_highlight': 'assets/settings_highlight.png',
                     'reconnect_highlight': 'assets/reconnect_highlight.png',
                     'cooling_highlight': 'assets/cooling_highlight.png',
                     'info_highlight': 'assets/info_highlight.png'}
cetuspcr_buttons_path = {'add_icon': 'assets/add_icon.png',
                         'delete_icon': 'assets/delete_icon.png',
                         'confirm_icon': 'assets/confirm_icon.png',
                         'add_highlight': 'assets/add_highlight.png',
                         'delete_highlight': 'assets/delete_highlight.png',
                         'confirm_highlight': 'assets/confirm_highlight.png'}
experimentpcr_buttons_path = {'save_icon': 'assets/save_icon.png',
                              'run_icon': 'assets/run_icon.png',
                              'save_highlight': 'assets/save_highlight.png',
                              'run_highlight': 'assets/run_highlight.png'}

hover_texts = {
    'default': 'Feito com ♥ na ETEC PV pelo 3º Mecatrônica(2k19).',
    'home': 'Voltar a tela inicial.',
    'info': 'Exibir informações do programa.',
    'cooling': 'Iniciar processo de resfriamento.',
    'reconnect': 'Iniciar conexão com o Cetus PCR.',
    'settings': 'Exibir configurações dos processos padrões.',
    'add': 'Adicionar um novo experimento.',
    'delete': 'Remove o experimento selecionado.',
    'confirm': 'Exibir as informações do experimento selecionado.',
    'save': 'Salva as informações do experimento atual.',
    'run': 'Iniciar experimento.'
}

exp_path = 'experiments.pcr'
