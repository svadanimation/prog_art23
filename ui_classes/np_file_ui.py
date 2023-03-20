import sys
from importlib import reload
import maya.cmds as mc

mod_path = 'Z:/Classes/W23/Programming for Artists/VS Code Workspace/prog_art23/file_io'
if mod_path not in sys.path:
    sys.path.append(mod_path)

import np_file_io as np
reload(np)

class FileIO_ui():
    WINDOW_NAME = 'fileio_win'

    def __init__(self, text = None):
        self.text = 'Hello world!' 
        self.filepath = None
    
        self.remove()
        self.window = mc.window(self.WINDOW_NAME)
        self.layout = mc.columnLayout(columnAttach = ('both', 5),
                                      rowSpacing = 10,
                                      columnWidth = 250)
        self.text_scroll_field = mc.scrollField(editable = False,
                                                wordWrap = True, 
                                                text = 'Awaiting file path...')
        self.load_file_button = mc.button(label = "Load text file",
                                                  command = self.load_file)
        self.save_file_button = mc.button(label = "Save text file", 
                                        command = self.save_file)
        self.show()

    def load_file(self, *args):

        result = mc.fileDialog2(fileFilter = '*.txt', dialogStyle = 2)
        if not result:
            return
        self.filepath = result[0]

        mc.scrollField(self.text_scroll_field, 
                       edit = True,
                       editable = True,
                       text = self.text)
        print(f'Your file currently says: \n\n {np.rw_text(self.filepath, content = None)}')
        
    def save_file(self, *args):
        if not self.filepath:
            mc.warning('No file path given')
            return
        np.rw_text(self.filepath, content = mc.scrollField(self.text_scroll_field,
                                                           query = True,
                                                           text = True))
        print(f'Your file now says: \n\n {mc.scrollField(self.text_scroll_field, query = True, text = True)}')

    def show(self):
        if mc.window(self.WINDOW_NAME, query = True, exists = True):
            mc.showWindow(self.WINDOW_NAME)

    def remove(self):
        if mc.window( self.WINDOW_NAME, query = True, exists = True):
            mc.deleteUI(self.WINDOW_NAME)

if __name__ == '__main__':
    the_ui = FileIO_ui()