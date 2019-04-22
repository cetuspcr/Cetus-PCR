import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable('Cetus PCR.py',
                          base=base,
                          shortcutName='Cetus PCR',
                          shortcutDir='DesktopFolder'),
               Executable('functions.py', base=base),
               Executable('interace.py', base=base)]

options = {'build_exe': {
    {'includes': ['tkinter', 'pyserial', 'matplotlib']},
    {'include_files': ['assets/cetus.ico'],
     'include_msvcr': True}}}


setup(
    name='ProjetoCetus',
    version='v0.1-alpha',
    executables=executables,
    options=options
)
