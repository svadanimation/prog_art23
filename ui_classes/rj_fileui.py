import sys
import maya.cmds as mc
from importlib import reload
from pprint import pprint

# File_io UI
mod_path = 'Z:/Classes W2023/Programming/VS Code/prog_art23/file_io'

if mod_path not in sys.path:
    sys.path.append(mod_path)

import rj_file_io as rj
reload(rj)
    # rj.text_plcmnt('Z:/ioimport.txt', 'Impo2rt pract457ice.')
    # pprint(rj.text_rdr('Z:/ioimport.txt'))

#Class and Attributes
class FileIO_ui():
    WINDOW_NAME = 'fileio_win'
    def __init__(self, text=None):
        self.remove()
        self.window = mc.window(self.WINDOW_NAME)
        self.layout = mc.columnLayout(columnAttach=('both', 5),
                                      rowSpacing=10,
                                      columnWidth=250)
        self.button = mc.button(label='Load File', 
                                command=self.load_file)
        self.show()
        self.text = text

    def load_file(self, *args):
        file_filters = 'Text files (*txt);; JSON files (*.json)'
        result = mc.fileDialog2(ff=file_filters, ds=2, dir='Z:')
        selected_file = result[0]
        if not result:
            mc.warning('No available files.')
            return
        else:
            print(result)
            with open(selected_file, 'r') as s:
                data = s.read()
                if not data:
                    mc.warning('Selected file is empty.')
                else:
                    mc.scrollField(editable=True, 
                        wordWrap=True, 
                        text=data) 

    def update_scroll_field(self, *args):
        pass

    def remove(self):
        if mc.window(self.WINDOW_NAME, q=1, ex=1):
            mc.deleteUI(self.WINDOW_NAME)

    def show(self):
        if mc.window(self.WINDOW_NAME, q=1, ex=1):
            mc.showWindow(self.WINDOW_NAME)

if __name__ == '__main__':
    the_ui = FileIO_ui()