import sys
import maya.cmds as mc
from importlib import reload
from pprint import pprint

mod_path = 'Z:/Classes W2023/Programming/VS Code/prog_art23/file_io'

if mod_path not in sys.path:
    sys.path.append(mod_path)

import rj_file_io as rj
reload(rj)

rj.text_plcmnt('Z:/ioimport.txt', 'Impo2rt pract457ice.')
pprint(rj.text_rdr('Z:/ioimport.txt'))





class FileIO_ui():
    WINDOW_NAME = 'fileio_win'
    def __init__(self, text=None):
        self.remove()
        self.the_window = mc.window(self.WINDOW_NAME)
        self.layout = mc.columnLayout(columnAttach=('both', 5),
                                      rowSpacing=10,
                                      columnWidth=100)
        self.button = mc.button(label='oh wow what', 
                                command=self.print_text)
        self.show()
        self.text = text

    def print_text(self, _):
        pprint(f"You said, \"{self.text}\"")

    def remove(self):
        if mc.window(self.WINDOW_NAME, q=1, ex=1):
            mc.deleteUI(self.WINDOW_NAME)

    def show(self):
        if mc.window(self.WINDOW_NAME, q=1, ex=1):
            mc.showWindow(self.WINDOW_NAME)

if __name__ == '__main__':
    the_ui = FileIO_ui("Hello, how are you on this fine warm day?")