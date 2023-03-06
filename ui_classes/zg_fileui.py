
# built ins
import sys
from pprint import pprint
from importlib import reload

# env
import maya.cmds as mc

# pprint (sys.path)
# pprint (sys.modules)

mod_path = 'Z:/vs_code_svad/prog_art23/file_io'
if mod_path not in sys.path:
    sys.path.append(mod_path)

import np_file_io
reload(np_file_io)


class FileIO_ui():
    WINDOW_NAME = 'fileio_win'

    def __init__(self, text=None):
        self.text = text
        self.filepath = None

        self.remove()
        self.window = mc.window(self.WINDOW_NAME)
        self.layout = mc.columnLayout(columnAttach=('both', 5), 
                                      rowSpacing=10, 
                                      columnWidth=250)
        self.update_text_scroll_field = mc.button(label='Load text file', 
                                                  command=self.update_scroll_field)
        self.text_scroll_field = mc.scrollField(editable=True, 
                                                wordWrap=True, 
                                                text='Default text' )


        self.show()
    # alternate synatx to absorb extra arguments
    # def print_text(self, *args):
    
    def update_scroll_field(self, _):
        '''
        Print a message when you click the button
        '''
        result = mc.fileDialog2(fileFilter='*.txt', dialogStyle=2)
        if not result:
            return
        self.filepath = result[0]

        

        # put your file load here, give it the file path, capture the result text
        # stuff the result text into your scroll field

        print(f'This is what you wrote: \n\n {self.filepath} ')
        mc.scrollField(self.text_scroll_field,
                       edit=True,
                       text=self.filepath)

    def save_file(self):
        if not self.filepath:
            mc.warning('No file given')
            return
        # get the text from your scroll field
        # write the file using your module

    def show(self):
        '''show the ui'''
        if mc.window( self.WINDOW_NAME, query = True, exists = True ):
            mc.showWindow(self.WINDOW_NAME)

    def remove(self):
        '''Remove the ui'''
        if mc.window( self.WINDOW_NAME, query = True, exists = True ):
            mc.deleteUI(self.WINDOW_NAME)



if __name__ == '__main__':
    the_ui = FileIO_ui('Good dog, spot')
    print(the_ui.text)

    # TEXT = 'Hello World'
    # text_path = 'Z:/text.txt'
    # np_file_io.rw_text(text_path, content = TEXT)
