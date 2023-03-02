'''
TODO write a refresh function
TODO call after a dir is added.
'''

import sys
import os

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as mc

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

        # TODO pass data as input to function with *args
        if not isinstance(self.parent, omui.MQtUtil):
            self.parent.add_shots_data = selected_item_labels
            self.parent.add_shots(selected_item_labels)
  
    
    def search_directory(self):
        directory = mc.fileDialog2(fileMode=3, 
                                   dialogStyle=2, 
                                   caption="Select Directory", 
                                   okc='Select')[0]
        if not os.path.isdir(directory):
            return []
        
        self.items = file_grep.get_files(directory)
        self.refresh_list()

if __name__ == "__main__":

    try:
        multi_select_dialog.close() # pylint: disable=E0601
        multi_select_dialog.deleteLater()
    except:
        pass

    multi_select_dialog = MultiSelectDialog()
    multi_select_dialog.show()
