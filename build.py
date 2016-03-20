import sys
import os,shutil
from cx_Freeze import setup, Executable

build_exe_options = {"optimize": 2}
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
executables = [Executable(script='misaka.pyw',
               base=base,
               targetName="Misaka.exe",
               compress=True)]
setup(name='Misaka',
      version='1.0',
      description='Mathematica Input Sequence Analyzer and Keystroke Assistant by xmcp',
      options = {"build_exe": build_exe_options},
      executables=executables)

print('===== CLEANING UP =====')

os.remove('build/exe.win32-2.7/unicodedata.pyd')
os.remove('build/exe.win32-2.7/_hashlib.pyd')
shutil.rmtree('build/exe.win32-2.7/tcl/encoding')
shutil.rmtree('build/exe.win32-2.7/tcl/tzdata')
shutil.rmtree('build/exe.win32-2.7/tcl/msgs')
shutil.rmtree('build/exe.win32-2.7/tk/demos')
shutil.rmtree('build/exe.win32-2.7/tk/images')
shutil.rmtree('build/exe.win32-2.7/tk/msgs')

os.rename('build/exe.win32-2.7','build/misaka-exe.win32-2.7')

print('===== DONE =====')
