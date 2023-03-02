import sys

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
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class MultiSelectDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(MultiSelectDialog, self).__init__(parent)

        # self.items = ["Item 01", "Item 02", "Item 03", "Item 04", "Item 05", "Item 06"]
        self.items = file_grep.get_files('Z:/work/roller_girl')

        self.setWindowTitle("Multi-Select")
        self.setFixedWidth(220)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.filter_line_edit = QtWidgets.QLineEdit()

        self.list_wdg = QtWidgets.QListWidget()
        self.list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_wdg.addItems(self.items)

        self.close_btn = QtWidgets.QPushButton("Close")
        self.add_btn = QtWidgets.QPushButton("Add")

    def create_layout(self):

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.filter_line_edit)
        main_layout.addWidget(self.list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        # connect the signal textChanged to the filter function
        self.filter_line_edit.textChanged.connect(self.filter_list)

        self.list_wdg.itemSelectionChanged.connect(self.print_selected_item)

        self.close_btn.clicked.connect(self.close)
        self.add_btn.clicked.connect(self.add_selected_item)

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

    def add_selected_item(self):
        items = self.list_wdg.selectedItems()

        selected_item_labels = []
        for item in items:
            selected_item_labels.append(item.text())

        # check if window already exists
        if mc.window('Added', exists=True):
            mc.deleteUI('Added')
              
        # create window and layout
        window = mc.window(title='Added', widthHeight=(300, 300))
        mc.columnLayout(adjustableColumn=True)

        # create text scroll list and add selected items
        list_layout = mc.textScrollList(numberOfRows=35)
        mc.textScrollList(list_layout, edit=True, append=selected_item_labels)

        mc.showWindow(window)

if __name__ == "__main__":

    try:
        multi_select_dialog.close() # pylint: disable=E0601
        multi_select_dialog.deleteLater()
    except:
        pass

    multi_select_dialog = MultiSelectDialog()
    multi_select_dialog.show()
