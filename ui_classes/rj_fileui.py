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
    SCROLL_NAME = 'my_scroll_field'
    
    def __init__(self, text=None):
        self.remove()

        self.window = mc.window(self.WINDOW_NAME, t='File Rewriter')
        self.layout = mc.columnLayout(columnAttach=('both', 5),
                                      rowSpacing=10,
                                      columnWidth=250)
        self.load_button = mc.button(l='Load File', 
                                     c=self.load_file,
                                     w=200)
        self.data = ''
        #self.spacer = mc.separator(style='none', height=10)
        self.scroll_field = mc.scrollField(self.SCROLL_NAME,
                                            editable=True, 
                                            wordWrap=True, 
                                            text=self.data,
                                            vis=0)
        #self.spacer = mc.separator(style='none', height=10)
        self.write_button = mc.button(l='Rewrite File', 
                                      c=self.update_text_file,
                                      w=200)
        self.show()
        self.text = text
        self.selected_file = None

    def load_file(self, *args):
        result = mc.fileDialog2(ff='*.txt', ds=2, dir='Z:')
        self.selected_file = result[0]
        if not result:
            mc.warning('No available files.')
            return
        else:
            print(result)
            with open(self.selected_file, 'r') as s:
                self.data = s.read()
                mc.scrollField(self.SCROLL_NAME,
                                   edit=True,
                                   text=self.data,
                                   vis=1)

    def update_text_file(self, *args):
        content = mc.scrollField(self.SCROLL_NAME,
                                    q=True,
                                    text=True)
        if content:
            rj.text_plcmnt(self.selected_file, content)
            print('File rewritten.')
        else:
            mc.warning("Nothing to rewrite.")
            return

    def remove(self):
        if mc.window(self.WINDOW_NAME, q=1, ex=1):
            mc.deleteUI(self.WINDOW_NAME)

    def show(self):
        if mc.window(self.WINDOW_NAME, q=1, ex=1):
            mc.showWindow(self.WINDOW_NAME)

if __name__ == '__main__':
    the_ui = FileIO_ui()