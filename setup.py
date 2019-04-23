
import os
import tkinter
from cx_Freeze import setup, Executable

os.environ[
    'TCL_LIBRARY'] = r'C:\Users\Wilson Cazarré\AppData\Local\Programs\Python\Python37-32\tcl\tcl8.6'
os.environ[
    'TK_LIBRARY'] = r'C:\Users\Wilson Cazarré\AppData\Local\Programs\Python\Python37-32\tcl\tk8.6'

executables = [Executable('Cetus PCR.py',
                          base='Win32GUI',
                          shortcutName='Cetus PCR',
                          shortcutDir='DesktopFolder',
                          icon='assets/cetus.ico'),
               Executable('functions.py', base='Win32GUI'),
               Executable('interface.py', base='Win32GUI')]

setup(
    name='ProjetoCetus',
    version='0.1',
    executables=executables,
    options={'build_exe':
                 {'includes': ['tkinter', 'serial', 'matplotlib'],
                  'include_files': ['assets/cetus.ico', 'assets/tcl86t.dll',
                                    'assets/tk86t.dll'],
                  'include_msvcr': True, }}
)
