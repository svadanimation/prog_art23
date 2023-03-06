# Objectives
- Reinforce concepts of classes
- Provide opportunity to study Qt/Maya widgets
- Use super to overwrite class data

# Write a UI that communicates with your file_io object
- import your file io functions
- make a block to reload the functions
```python
from importlib import reload; reload(module)
```
## Create a class and attributes
- Create a class called `Fileio_UI`
- Add the option to pass data in to your class
- Create an `__init__` function that sets up instance variables
  - `self.window = ...`
  - `self.data = ...`
  - etc
# Create a window
- Build the window
- Add single column layout into the window
- Add widgets into the window
  - Add a button that opens a `mc.fileDialog2`
  - Add a label that shows the path you selected
  - Add a text field that displays your text
  - Add a save button that writes your data to disk
- Connect a function/slot for each of these tasks
- Update the appropriate UI controls/widgets
- Create a function to tear down the window
- Create a function to show/launch the window
- Create an `if __name__ == '__main__:'` block for testing.

### Maya template
```python
import maya.cmds as mc # pylint: disable=import-error

class TestUI(object):
    WINDOW = 'submit_ui'
    
    def __init__(self):
        self.window = None
        
        self.remove()

        self.window = mc.window(self.WINDOW, widthHeight=(766, 490), sizeable=False)
        self.show()
        
    
    def show(self):
        '''Show the UI'''
        mc.window(self.window, edit=True, sizeable=False, resizeToFitChildren=True)
        mc.showWindow( self.window )

    def remove(self, *args):
        '''Remove the ui'''
        if mc.window( self.WINDOW, q = 1, ex = 1 ):
            mc.deleteUI(self.WINDOW)
            
the_window = TestUI()
```

### Qt template from Chris Zurbrigg 
**get his training if you want to learn Qt**
```python
import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.lineedit = QtWidgets.QLineEdit()
        self.checkbox1 = QtWidgets.QCheckBox()
        self.checkbox2 = QtWidgets.QCheckBox()
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")


    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Name:", self.lineedit)
        form_layout.addRow("Hidden:", self.checkbox1)
        form_layout.addRow("Locked:", self.checkbox2)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.lineedit.editingFinished.connect(self.print_hello_name)

        self.checkbox1.toggled.connect(self.print_is_hidden)

        self.cancel_btn.clicked.connect(self.close)

    def print_hello_name(self):
        name = self.lineedit.text()
        print("Hello {0}!".format(name))

    def print_is_hidden(self):
        hidden = self.checkbox1.isChecked()
        if hidden:
            print("Hidden")
        else:
            print("Visible")


if __name__ == "__main__":

    try:
        test_dialog.close() # pylint: disable=E0601
        test_dialog.deleteLater()
    except:
        pass

    test_dialog = TestDialog()
    test_dialog.show()

```
