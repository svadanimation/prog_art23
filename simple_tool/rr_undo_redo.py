'''

This tool allows for interactive selection of the commands
available to undo and/or redo. With a list of widgets, a user
can go to a specific place in the history of commands.

Example:
    With a set of commands having been done and/or undone:
    A user will be able to interactively select/double-click
    on one of the commands in the list and jump to that place
    in the history of commands that have been done and/or undone

TODO:
    With the upper list being undoable commands and lower list
    being the redoable commands:

    Simple double-click an item/commands
    You will then jump to that location in the history of commands
    The list will update, and you may jump to another item/command

    Note: Click the update button in the center if you happen to
    undo/redo/do any other command, so you will have updated lists

Author(s):
    - Raphael Roman

Contributors(s):
    - Zach Gray

Editors(s):
    - Zach Gray
    
'''

# Imports
import maya.cmds as mc
import maya.api.OpenMaya as om
from contextlib import contextmanager

# Build a simple data class and initialize a simple list
class CustomData:
    def __init__(self):
        self.value = []

# Create a custom callback, this will be passed three arguments from MCommand message
def customCommandOutputCallback(message, filter, customData):
    if isinstance(customData, CustomData):
        customData.value.append(message)

# Setup a decorator for the context manager
@contextmanager
def capture_output():

    # setup the custom data
    data = CustomData()
    try:
        id = om.MCommandMessage.addCommandOutputCallback(customCommandOutputCallback, data)
        yield data

    finally:
        om.MCommandMessage.removeCallback(id)
        
    return data

# wrap functionality and error checking into a single function
def get_queue(redo=False, strip=False):
    
    # always return an empty list
    queue = []
    if redo:
         with capture_output() as output:
            mc.undoInfo(q=True, prq=True)
            
    # call our context manager
    else:
        with capture_output() as output:
            mc.undoInfo(q=True, pq=True)

    
    if output.value is not None:
        queue = output.value
        
        # optionally remove the queue id
        if strip:
            queue = [v.split(':')[-1].lstrip() for v in output.value]
    
    return queue

empty_undo_list = "Nothing to undo"
empty_redo_list = "Nothing to redo"

class Undo_Redo_Window():
    
    def __init__(self):
        
        # Simplifies naming and labelling
        self.window_name = "Undo_Redo_Window"
        self.title = "Undo/Redo Tool"
        self.introduction = "Welcome to the Undo/Redo Tool!"
        self.size = (350, 300)
            
        # If opening new window, close old
        if mc.window(self.window_name, ex = True):
            mc.deleteUI(self.window_name)
            
        # Creates window
        self.window = mc.window(    self.window_name, t=self.title, 
                                    wh=self.size, 
                                    s=False, 
                                    mnb=False, 
                                    mxb=False   )
                                    
        mc.window(self.window_name, e=True, wh=(200,320))
        
        # Creating undo/redo widgets
        self.master_layout= mc.columnLayout(adj=True)
        mc.separator(h=20)
        if get_queue():
            self.undo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=get_queue(),
                                                w=400, 
                                                fn='fixedWidthFont',
                                                hlc=[0.1, 0.1, 0.1],
                                                dcc=self.undo_action    )
   
        elif not get_queue():
            self.undo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=empty_undo_list,
                                                w=400, 
                                                fn='fixedWidthFont',
                                                hlc=[0.1, 0.1, 0.1]    )
                                                
                                                
        mc.separator(h=15)
        mc.button(    
                    l="YOU ARE HERE - CLICK TO UPDATE LISTS", 
                    p=self.master_layout, 
                    align="center", 
                    c=self.update_lists    )
        mc.separator(h=15)

        if get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=reversed(get_queue(redo=True)), 
                                                w=400,
                                                fn='fixedWidthFont',
                                                hlc=[0.1, 0.1, 0.1],
                                                dcc=self.redo_action    )
        elif not get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=empty_redo_list, 
                                                w=400,
                                                fn='fixedWidthFont',
                                                hlc=[0.1, 0.1, 0.1]    )
        mc.setParent('..')
        
        # Making window visible
        mc.showWindow(self.window_name)
        
    # Allow user to update lists if changes have been made since
    def update_lists(self, *args):
        if get_queue():
            self.undo_list = mc.textScrollList(
                                                self.undo_list,
                                                dcc=self.undo_action, 
                                                a=get_queue(), 
                                                ra=True, 
                                                e=True    )
        elif not get_queue():
            self.undo_list = mc.textScrollList(
                                                self.undo_list, 
                                                a=empty_undo_list,
                                                ra=True, 
                                                e=True    )                   
        if get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                self.redo_list,
                                                dcc=self.redo_action, 
                                                a=reversed(get_queue(redo=True)), 
                                                ra=True, 
                                                e=True    )
        elif not get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                self.redo_list, 
                                                a=empty_redo_list, 
                                                ra=True, 
                                                e=True    )

    # Allow user to undo/redo when an item on the list is double-clicked
    def undo_action(self):
        selected_item = ''.join(mc.textScrollList(self.undo_list, si=True, q=True))
        reverse_undo_list = list(reversed(get_queue()))
        undo_amount = reverse_undo_list.index(selected_item) + 1

        for i in range(undo_amount):
            print("Undoing!")
            mc.undo()

        if get_queue():
            self.undo_list = mc.textScrollList(
                                                self.undo_list,
                                                dcc=self.undo_action, 
                                                a=get_queue(), 
                                                ra=True, 
                                                e=True    )
        elif not get_queue():
            self.undo_list = mc.textScrollList(
                                                self.undo_list, 
                                                a=empty_undo_list,
                                                ra=True, 
                                                e=True    )                   
        if get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                self.redo_list,
                                                dcc=self.redo_action, 
                                                a=reversed(get_queue(redo=True)), 
                                                ra=True, 
                                                e=True    )
        elif not get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                self.redo_list, 
                                                a=empty_redo_list, 
                                                ra=True, 
                                                e=True    )

    def redo_action(self):
        selected_item = ''.join(mc.textScrollList(self.redo_list, si=True, q=True))
        reverse_redo_list = list(reversed(get_queue(redo=True)))
        redo_amount = reverse_redo_list.index(selected_item) + 1

        for i in range(redo_amount):
            print("Redoing!")
            mc.redo()

        if get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                self.redo_list,
                                                dcc=self.redo_action, 
                                                a=reversed(get_queue(redo=True)), 
                                                ra=True, 
                                                e=True    )
        elif not get_queue(redo=True):
            self.redo_list = mc.textScrollList(
                                                self.redo_list, 
                                                a=empty_redo_list, 
                                                ra=True, 
                                                e=True    )
        
        if get_queue():
            self.undo_list = mc.textScrollList(
                                                self.undo_list,
                                                dcc=self.undo_action, 
                                                a=get_queue(), 
                                                ra=True, 
                                                e=True    )
        elif not get_queue():
            self.undo_list = mc.textScrollList(
                                                self.undo_list, 
                                                a=empty_undo_list,
                                                ra=True, 
                                                e=True    )   
                                                             
user_window = Undo_Redo_Window()