#
# Pyinstaller allows you to run it through python as well as terminal/cmd. This format allows
#   it to be a bit more readable and editable down the line compared to the command line.
#


import PyInstaller.__main__

PyInstaller.__main__.run([
    './webtool/main.py',
    '--onedir',
    '--windowed',
    '--clean',
    '--noconfirm',
    '--name WebTool'
])
