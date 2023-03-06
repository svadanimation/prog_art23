import sys
from pprint import pprint
from importlib import reload
import maya.cmds as mc

mod_path = 'Z:/Kaleb-Animation_23\winter_23/programming_4_artists/prog_art23/prog_art23/file_io'
if mod_path not in sys.path:
    sys.path.append(mod_path)

import kr_file_io
reload (kr_file_io)

class FileIo_UI():

    MY_WINDOW = 'fileUI_window'

    def __init__(self, text=None):
        self.text = text
        
        self.remove()
        self.window = mc.window(self.MY_WINDOW, title = 'File Writer')
        self.layout = mc.columnLayout(columnAttach=('both', 5), 
                                      rowSpacing=10, 
                                      columnWidth=250)

        self.spacer = mc.separator(height = 10)
        self.button = mc.button(label='Load Text File', command = self.update_scroll_field)
        self.spacer = mc.separator(height = 10)
        self.text_scroll_field = mc.scrollField( editable=True, 
                                             wordWrap=True, 
                                             text='Editable with word wrap' )

        self.show()
    
    def update_scroll_field(self, *args):
        print(f'this is what you wrote: \n\n {self.text}')

    def show(self):
        if mc.window(self.MY_WINDOW, q = True, exists = True):
            mc.showWindow(self.MY_WINDOW)

    def remove(self):
        if mc.window(self.MY_WINDOW, q = True, exists = True):
            mc.deleteUI(self.MY_WINDOW)

if __name__ == '__main__':
    my_ui = FileIo_UI('evans cathphrase')
    #print(my_ui.text)
    # TEXT = 'my world'
    # text_path = 'Z:/text_file.txt'
    # kr_file_io.write_txt(text_path, TEXT)

# pprint(sys.path)