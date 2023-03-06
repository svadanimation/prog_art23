import sys
from pprint import pprint
from importlib import reload
import maya.cmds as mc

mod_path = "Z:/Classes/W23/Programming for Artists/VS Code Workspace/prog_art23/file_io"
if mod_path not in sys.path:
    sys.path.append(mod_path)

import np_file_io
reload(np_file_io)

class FileIO_ui():
    WINDOW_NAME = 'Rick_and_Morty_Copypasta'

    def __init__(self, text = None):
        self.text = text    
        self.filepath = None
    
        self.remove()
        self.window = mc.window(self.WINDOW_NAME)
        self.layout = mc.columnLayout(columnAttach = ('both', 5),
                                      rowSpacing = 10,
                                      columnWidth = 250)
        self.update_text_scroll_field = mc.button(label = "Lod text file", command = self.print_text)
        self.text_scroll_field = (editable = False,
                              wordWrap = True, 
                              text = 'Default text' )
        self.show()

    def update_scroll_field(self, *args):

        result = mc.fileDialog2(fileFilter = '*.text', dialogStyle = 2)
        if not result:
            return
        self.filepath = result[0]

        print(f'This is what you wrote: \n\n {self.text}')
        mc.scrollField(self.text_scroll_field,
                       edit = True,
                       text = self.text)

    def save_file(self):
        if not filepath:
            mc.warning('No file given')
            return

    def show(self):
        '''Show the UI'''
        if mc.window(self.WINDOW_NAME, query = True, exists = True):
            mc.showWindow(self.WINDOW_NAME)

    def remove(self):
        '''Remove the ui'''
        if mc.window( self.WINDOW_NAME, query = True, exists = True):
            mc.deleteUI(self.WINDOW_NAME)

if __name__ == '__main__':
    the_ui = FileIO_ui('''To be fair, you have to have a very high IQ to understand Rick and Morty. The humor is extremely subtle, and without a solid grasp of theoretical physics most of the jokes will go over a typical viewer's head. There's also Rick's nihilistic outlook, which is deftly woven into his characterisation - his personal philosophy draws heavily from Narodnaya Volya literature, for instance. The fans understand this stuff; they have the intellectual capacity to truly appreciate the depths of these jokes, to realize that they're not just funny- they say something deep about LIFE. As a consequence people who dislike Rick and Morty truly ARE idiots- of course they wouldn't appreciate, for instance, the humour in Rick's existencial catchphrase "Wubba Lubba Dub Dub," which itself is a cryptic reference to Turgenev's Russian epic Fathers and Sons I'm smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Dan Harmon's genius unfolds itself on their television screens. What fools... how I pity them. XD And yes by the way, I DO have a Rick and Morty tattoo. And no, you cannot see it. It's for the ladies' eyes only- And even they have to demonstrate that they're within 5 IQ points of my own (preferably lower) beforehand.''')