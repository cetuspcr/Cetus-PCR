"""Script para exportar o script em python para uma aplicação
de Windows independente. Um instalador pode ser gerado posteriormente
usando o Inno Setup.

A pasta "assets" contém todos os arquivos adicionais para o programa
tais como ícones e DLL necessárias.

Para a gerar os arquivos necessários, abra o prompt de comando e navegue
para a pasta raiz do projeto e execute o seguinte comando:
'python setup.py build'

Requer cx_Freeze e Python 3.7 no PATH do sistema.
"""

import os

from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Users\WILSONCAZARRESOUSA\AppData\Local\Programs\Python\Python37-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\WILSONCAZARRESOUSA\AppData\Local\Programs\Python\Python37-32\tcl\tk8.6'

executables = [Executable('Cetus PCR.py',
                          base='Win32GUI',
                          icon='assets/cetus.ico'),
               Executable('functions.py', base='Win32GUI'),
               Executable('interface.py', base='Win32GUI')]

setup(name='Cetus PCR',
      version='0.2',
      description='Interface para o Cetus PCR',
      executables=executables,
      options={'build_exe': {'includes': ['tkinter', 'serial'],
                             'include_files': ['assets/'],
                             'include_msvcr': True, }})
