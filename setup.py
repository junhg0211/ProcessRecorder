# coding=utf-8
import sys
from cx_Freeze import setup, Executable

build_exe_options = dict(
    includes=['os', 'datetime', 'time', 'pygame'],
    include_files=[
        './res/font/NotoSansCJKkr-DemiLight.otf',
        './res/font/NotoSansCJKkr-Medium.otf',
        './res/font/NotoSansCJKkr-Regular.otf',
        './res/font/NotoSansCJKkr-Thin.otf',
        './res/image/icon.ico'
    ]
)

setup(
    name='ProcessRecorder',
    version='1.0',
    description='ProcessRecorder for Deathliners or Temaca',
    author='스치',
    options={'build_exe': build_exe_options},
    executables=[Executable(
        'program_recorder.pyw',
        base='Win32GUI',
        targetName='ProcessRecorder.exe',
        icon='./res/image/icon.ico'
    )]
)