# Imports and setup
import sys
from importlib import reload
from pprint import pprint
import maya.cmds as mc

MOD_PATH = "Z:\\VSCODE\\prog_art23\\file_io"
if MOD_PATH not in sys.path:
    sys.path.append(MOD_PATH)
import rr_file_io as rr
reload(rr)

class TestUI():
    WINDOW_NAME = "ui_window"
    TITLE = "UI Window"
    DIMENSION = (500,500)
    TEXT = "Hello window!"

    def __init__(self):
        # Make sure window is singleton
        self.singleton_confirm()
        
        # Initializing characteristics of window
        self.window_name = self.WINDOW_NAME
        self.window_title = self.TITLE
        self.window_dimensions = self.DIMENSION
        self.window = mc.window(self.WINDOW_NAME, rtf=True, s=False)
        self.window_text = self.TEXT

        # Initializing characteristics of scrollfield
        self.text_scrollfield = "Text/JSON Scroll Field"
        self.scrollfield_width = 250
        self.scrollfield_height = 250
        self.filepath = None
        self.text_from_file = None

        # Window layout
        mc.columnLayout()
        mc.button("Select file to display", command=self.print_text_from_file)
        self.text_scrollfield = mc.scrollField(w=self.scrollfield_width, 
                                               h=self.scrollfield_height,
                                               tx="Nothing here...")
        
        mc.button("Save current text to file", command=self.save_text_to_file)

        # Displaying window
        mc.window(self.WINDOW_NAME, e=True, s=False)
        self.open_window()
    
    # Print text
    def print_text_from_file(self, *args):
        file_filter = 'Text Files (*.txt);;JSON Files (*.json)'
        start_dir = 'Z:\\'
        selected_file = mc.fileDialog2(ff=file_filter, ds=2, dir=start_dir)
        if not selected_file:
            mc.warning("Please select a file that can be displayed")
            return
        self.filepath = selected_file[0]
        self.text_from_file = rr.read_text(self.filepath)
        print(self.text_from_file)

        mc.scrollField(self.text_scrollfield, edit=True, tx=self.text_from_file)

    # Save text
    def save_text_to_file(self, *args):
        rr.write_text(self.filepath, mc.scrollField(self.text_scrollfield, tx=True, q=True))
        print("Text in the field has now been saved into the file")


    # Func to make sure window is singleton
    def singleton_confirm(self):
        if mc.window(self.WINDOW_NAME, ex=True, q=True):
            mc.deleteUI(self.WINDOW_NAME)

    # Func to show the window
    def open_window(self):
        if not mc.window(self.WINDOW_NAME, ex=True, q=True):
            mc.warning("Cannot show window that does not exist")
            return
        mc.showWindow(self.WINDOW_NAME)

if __name__ == "__main__":
    my_window = TestUI()

