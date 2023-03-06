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
        self.window = mc.window(self.WINDOW_NAME)
        self.window_text = self.TEXT

        # Displaying window
        self.open_window()
        
    # Func to make sure window is singleton
    def singleton_confirm(self, window_name):
        if mc.window(self.WINDOW_NAME, ex=True, q=True):
            mc.deleteUI(self.WINDOW_NAME)

    # Func to show the window
    def open_window(self):
        if not mc.showWindow(self.WINDOW_NAME, ex=True, q=True):
            mc.warning("Cannot show window that does not exist")
            return
        mc.showWindow(self.WINDOW_NAME)

if __name__ == "__main__":
    my_window = TestUI()