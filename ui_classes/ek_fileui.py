import sys
from pprint import pprint
from importlib import reload
import os

import maya.cmds as mc

mod_path = (r'Z:\Documents\Winter 2023\programing for artists\vs code ek\git-and-github-fundamentals-EllaAKim\prog_art23')
mod_path = os.path.normpath(mod_path)
if mod_path not in sys.path:
    sys.path.append(mod_path)

import ek_file_io
reload(ek_file_io) 

class EkFile_ui():
    WINDOW_NAME = 'ekfile_io_window'
    def __init__(self, text=None):
        self.window = None
        self.remove()
        self.text = text
        self.remove()
        self.window = mc.window(self.WINDOW_NAME, 
                                widthheight = (766, 490), 
                                sizeable=False)
        self.show()
        self.layout = mc.columnLayout(columnAttach=('both', 5), 
                                      rowSpacing=10, 
                                      columnWidth=250)
        self.button = mc.button(label="Ella!", command=self.print_text)
        self.update_text_scroll_field = mc.button(label='Load text file', 
                                                  command=self.update_scroll_field)
        self.save_file_button = mc.button(label='Save file', 
                                                  command=self.save_file)
        self.text_scroll_field = mc.scrollField(editable=True, 
                                                wordWrap=True, 
                                                text='Default text' )


    def update_scroll_field(self, _):
        result = mc.fileDialog2(fileFilter='*.txt', dialogStyle=2)
        if not result:
            return
        self.filepath = result[0]
        print(f'this is what you typed: \n\n {self.text}')
        mc.scrollField(self.text_scroll_field,
                       edit=True,
                       text=self.filepath)
        
    def save_file(self, _):
        if not self.filepath:
            mc.warning('No file given')
            return
        
    def show(self):
        mc.window( self.WINDOW_NAME,
                  edit=True,
                  sizeable=False,
                  resizeToFitChildren=True) 
        mc.showWindow(self.WINDOW_NAME)

    def remove(self, _):
        if mc.window( self.WINDOW_NAME, query=True, exists=True):
            mc.deleteUI(self.WINDOW_NAME)


if __name__ == "__main__":
    #ek_class = EkFile_ui("test run: class text")
    
    #TEXT = 'test run.'
    #file_path_t = 'Z:/text_file.txt'
    # ek_file_io.open_text(file_path_t, TEXT)