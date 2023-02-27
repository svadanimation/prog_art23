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

EMPTY_UNDO = "Nothing to undo"
EMPTY_REDO = "Nothing to redo"

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
        
        # Creating undo/redo widgets
        self.master_layout= mc.columnLayout(adj=True)
        mc.separator(h=20)
        undo_queue = get_queue()
        redo_queue = get_queue(redo=True)
        if undo_queue:
            self.undo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=undo_queue,
                                                w=400, 
                                                fn='fixedWidthFont',
                                                hlc=[0.1, 0.1, 0.1],
                                                dcc=self.undo_amount    )
   
        else:
            self.undo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=EMPTY_UNDO,
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

        if redo_queue:
            self.redo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=reversed(get_queue(redo=True)), 
                                                w=400,
                                                fn='fixedWidthFont',
                                                hlc=[0.1, 0.1, 0.1],
                                                dcc=self.redo_amount    )
        else:
            self.redo_list = mc.textScrollList(
                                                nr=20, 
                                                ams=False, 
                                                a=EMPTY_REDO, 
                                                w=400,
                                                fn='fixedWidthFont',
                                                hlc=[0.1, 0.1, 0.1]    )
        mc.setParent('..')     

        # Making window visible
        mc.window(self.window_name, e=True, wh=(400,620))
        mc.showWindow(self.window_name)

    def update_lists(self, *args):
        undo_queue = get_queue()
        redo_queue = reversed(get_queue(redo=True))

        if undo_queue:
            mc.textScrollList(  
                    self.undo_list,
                    dcc=self.undo_amount,
                    a=undo_queue,
                    ra=True,
                    e=True      )
        else:
            mc.textScrollList(  
                    self.undo_list,
                    a=EMPTY_UNDO,
                    ra=True,
                    e=True      )
            
        if redo_queue:
            mc.textScrollList(  
                    self.redo_list,
                    dcc=self.redo_amount,
                    a=redo_queue,
                    ra=True,
                    e=True      )
        else:
            mc.textScrollList(  
                    self.redo_list,
                    a=EMPTY_REDO,
                    ra=True,
                    e=True      )

    def undo_redo(self, amount, redo=False):
        for i in range(amount):
            if redo:
                mc.redo()
            else:
                mc.undo()

        self.update_lists()

    # Undo/redo
    def undo_amount(self):
        undo_queue = get_queue()
        selected_item = mc.textScrollList(self.undo_list, si=True, q=True)[0]
        reverse_undo_list = list(reversed(undo_queue))
        undo_amount = reverse_undo_list.index(selected_item) + 1
        self.undo_redo(amount=undo_amount)

    def redo_amount(self):
        redo_queue = get_queue(redo=True)
        selected_item = mc.textScrollList(self.redo_list, si=True, q=True)[0]
        reverse_redo_list = list(reversed(redo_queue))
        redo_amount = reverse_redo_list.index(selected_item) + 1
        self.undo_redo(amount=redo_amount, redo=True)

if __name__ == '__main__':
    Undo_Redo_Window()