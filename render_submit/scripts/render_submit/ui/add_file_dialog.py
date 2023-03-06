'''
TODO write a refresh function
TODO call after a dir is added.
'''

import os

from PySide2 import QtCore # pylint: disable=import-error
from PySide2 import QtWidgets # pylint: disable=import-error
from shiboken2 import wrapInstance # pylint: disable=import-error

import maya.OpenMaya as om # pylint: disable=import-error
import maya.OpenMayaUI as omui # pylint: disable=import-error
import maya.cmds as mc # pylint: disable=import-error

from render_submit import file_grep

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MultiSelectDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(MultiSelectDialog, self).__init__(parent)

        self.parent = parent
        self.items = []

        self.setWindowTitle("File Select")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.search_btn = QtWidgets.QPushButton("Search directory")
        self.filter_label = QtWidgets.QLabel("Filter:")
        self.filter_line_edit = QtWidgets.QLineEdit()

        self.list_wdg = QtWidgets.QListWidget()
        self.list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # self.list_wdg.addItems(self.items)
        self.refresh_list()

        self.add_selected_btn = QtWidgets.QPushButton("Add Selected")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_selected_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.search_btn)
        main_layout.addWidget(self.filter_label)
        main_layout.addWidget(self.filter_line_edit)
        main_layout.addWidget(self.list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        # connect the signal textChanged to the filter function
        self.filter_line_edit.textChanged.connect(self.filter_list)

        # self.list_wdg.itemSelectionChanged.connect(self.print_selected_item)

        self.close_btn.clicked.connect(self.close)
        self.add_selected_btn.clicked.connect(self.add_selected_items)
        self.close_btn.clicked.connect(self.add_selected_items)
        self.search_btn.clicked.connect(self.search_directory)

    def show_add_dialog(self):
        # This double test seems odd
        # Handles canceling the dialog
        if not self.items:
            self.search_directory()
        if self.items:
            self.show()

    def refresh_list(self):
        self.list_wdg.clear()
        self.filter_line_edit.clear()
        self.list_wdg.addItems(self.items)

    def filter_list(self, text):
        self.list_wdg.clear() # clear the list widget
        for item in self.items:
            if text in item: # only add the line if it passes the filter
                QtWidgets.QListWidgetItem(item, self.list_wdg)

    def print_selected_item(self):
        items = self.list_wdg.selectedItems()

        selected_item_labels = []
        for item in items:
            selected_item_labels.append(item.text())

        print("Selected Items: {0}".format(selected_item_labels))

    def add_selected_items(self):
        items = self.list_wdg.selectedItems()

        selected_item_labels = []
        for item in items:
            selected_item_labels.append(item.text())

        # print(f'Adding {selected_item_labels} to the list')
        if not isinstance(self.parent, omui.MQtUtil):
            self.parent.add_shots(selected_item_labels)
  
    
    def search_directory(self):
        directory = mc.fileDialog2(fileMode=3, 
                                   dialogStyle=2, 
                                   caption="Select Directory", 
                                   okc='Select')
        if directory: 
            directory = directory[0] 
        else: return []

        if not os.path.isdir(directory):
            return []
        
        self.items = file_grep.get_files(directory)
        self.refresh_list()

if __name__ == "__main__":

    try:
        multi_select_dialog.close() # pylint: disable=[E0601, E0602]
        multi_select_dialog.deleteLater() # pylint: disable=[E0601, E0602]
    except:
        pass

    multi_select_dialog = MultiSelectDialog()
    multi_select_dialog.show()
