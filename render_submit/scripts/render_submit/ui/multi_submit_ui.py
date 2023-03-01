'''
Multi Submit UI

TODO: Add appdirs module to store recent file

'''

import sys
import os
from pprint import pprint

from PySide2 import QtCore # pylint: disable=import-error
from PySide2 import QtWidgets # pylint: disable=import-error
from shiboken2 import wrapInstance # pylint: disable=import-error

import maya.OpenMaya as om # pylint: disable=import-error
import maya.OpenMayaUI as omui # pylint: disable=import-error
import maya.cmds as mc # pylint: disable=import-error

from render_submit import shot_data

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MultiSubmitTableWindow(QtWidgets.QMainWindow):
    '''Table for displaying and editing multi submit data
    '''

    ATTR_ROLE = QtCore.Qt.UserRole
    VALUE_ROLE = QtCore.Qt.UserRole + 1


    def __init__(self, parent=maya_main_window()):
        super(MultiSubmitTableWindow, self).__init__(parent)

        self.setWindowTitle("Multi Submit")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(600)

        self.create_menubar()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.shots_data = {}

        # This is terrible.
        # Figure out how to pass the data in to the class
        # or load from a file menu
        # self.filepath = r"Z:/vs_code_svad/prog_art23/render_submit/test/test_shot_data.json"

    def create_menubar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setNativeMenuBar(False)
        self.file_menu = self.menubar.addMenu("&File")
        self.file_menu.addAction("Open", self.open_file)
        self.file_menu.addAction("Save", self.save_file)
        self.setMenuBar(self.menubar)

        self.recent_files_menu = QtWidgets.QMenu("Recent Files", self)
        self.file_menu.addMenu(self.recent_files_menu)
        self.file_menu.addAction("Clear Recents", self.clear_recent_files)

        # Create a QActionGroup to manage the recent file actions
        self.recent_files_group = QtWidgets.QActionGroup(self)
        self.recent_files_group.setExclusive(True)
        self.recent_files_group.triggered.connect(self.open_recent_file)

        # Add some sample recent files
        recent_files = shot_data.load_recent_data()
        if recent_files:
            for recent_file in recent_files:
                self.add_recent_file(recent_file)

        # self.add_recent_file("/path/to/recent/file1.txt")
        # self.add_recent_file("/path/to/recent/file2.txt")
        # self.add_recent_file("/path/to/recent/file3.txt")
        

    def create_widgets(self):
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.table_wdg = QtWidgets.QTableWidget()
        self.table_wdg.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)



        self.table_wdg.setColumnCount(7)
        self.table_wdg.setColumnWidth(0, 22)
        self.table_wdg.setColumnWidth(2, 200)
        self.table_wdg.setColumnWidth(3, 70)
        self.table_wdg.setColumnWidth(4, 70)
        self.table_wdg.setColumnWidth(5, 70)
        self.table_wdg.setColumnWidth(6, 70)
        self.table_wdg.setHorizontalHeaderLabels(["Active", "File", "Note", "Cut In", "Cut Out", "Res", "Step"])
        header_view = self.table_wdg.horizontalHeader()
        header_view.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.add_btn = QtWidgets.QPushButton("Add")
        self.delete_btn = QtWidgets.QPushButton("Delete")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.table_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

    def open_file(self):
        loadpath = mc.fileDialog2(fileMode=1, fileFilter="JSON (*.json)")[0]
        if loadpath:
            shots_data = shot_data.get_shot_data(loadpath)
            if shots_data:
                self.shots_data = shots_data
                self.refresh_table()
                self.add_recent_file(loadpath)

            self.refresh_table()

    def open_recent_file(self, action):
        loadpath = action.data()
        if not os.path.isfile(loadpath):
            self.recent_files_group.removeAction(action)
            mc.confirmDialog(title="File Not Found",
                             message=f"The file {loadpath} no longer exists.",
                             button=["OK"])
            return
            
        shots_data = shot_data.get_shot_data(loadpath)
        if shots_data:
            self.shots_data = shots_data
            self.add_recent_file(loadpath)
        self.refresh_table()

    def save_file(self):
        savepath = mc.fileDialog2(fileMode=0, fileFilter="JSON (*.json)")[0]
        if savepath:
            shot_data.save_shot_data(self.filepath, self.get_shot_data())
            self.refresh_table()

    def add_recent_file(self, recent_filepath):
        # Remove any existing action with the same filepath
        for action in self.recent_files_group.actions():
            if action.data() == recent_filepath:
                self.recent_files_group.removeAction(action)

        # Create a new action for the recent file
        action = QtWidgets.QAction(recent_filepath, self)
        action.setData(recent_filepath)
        action.setToolTip(recent_filepath)
        self.recent_files_group.addAction(action)

        # Add the action to the recent files menu
        self.recent_files_menu.addActions([action])

        # Save the recent files to the settings file
        shot_data.save_recent_data([action.data() for action in self.recent_files_group.actions()])

    def clear_recent_files(self):
        # Remove any existing action
        for action in self.recent_files_group.actions():
            self.recent_files_group.removeAction(action)

        # Save the recent files to the settings file
        shot_data.save_recent_data([action.data() for action in self.recent_files_group.actions()])

    def create_connections(self):
        self.set_cell_changed_connection_enabled(True)

        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close)

    def set_cell_changed_connection_enabled(self, enabled):
        if enabled:
            self.table_wdg.cellChanged.connect(self.on_cell_changed)
        else:
            self.table_wdg.cellChanged.disconnect(self.on_cell_changed)

    def keyPressEvent(self, e):
        super(MultiSubmitTableWindow, self).keyPressEvent(e)
        e.accept()

    def showEvent(self, e):
        super(MultiSubmitTableWindow, self).showEvent(e)
        self.refresh_table()

    def refresh_table(self):
        if not self.shots_data:
            return
        
        self.set_cell_changed_connection_enabled(False)
        self.table_wdg.setRowCount(0)


        for i, shot in self.shots_data.items():
            i = int(i)
            res = ':'.join(shot['res'])

            self.table_wdg.insertRow(i)
            self.insert_item(i, 0, "", "active", shot['active'], True)
            self.insert_item(i, 1, shot['file'], None, shot['file'], False)
            self.insert_item(i, 2, shot['note'], None, shot['note'], False)
            self.insert_item(i, 3, shot['cut_in'], None, shot['cut_in'], False)
            self.insert_item(i, 4, shot['cut_out'], None, shot['cut_out'], False)
            self.insert_item(i, 5, res, None, res, False)
            self.insert_item(i, 6, shot['step'], None, shot['step'], False)

        self.set_cell_changed_connection_enabled(True)

    def insert_item(self, row, column, text, attr, value, is_boolean):
        item = QtWidgets.QTableWidgetItem(text)
        self.set_item_attr(item, attr)
        self.set_item_value(item, value)
        if is_boolean:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.set_item_checked(item, value)
        self.table_wdg.setItem(row, column, item)

    def on_cell_changed(self, row, column):
        self.set_cell_changed_connection_enabled(False)

        item = self.table_wdg.item(row, column)
        if column == 1:
            self.rename(item)
        else:
            is_boolean = column == 0
            self.update_attr(self.get_full_attr_name(row, item), item, is_boolean)

        self.set_cell_changed_connection_enabled(True)

    def rename(self, item):
        old_name = self.get_item_value(item)
        new_name = self.get_item_text(item)
        if old_name != new_name:
            actual_new_name = mc.rename(old_name, new_name)
            if actual_new_name != new_name:
                self.set_item_text(item, actual_new_name)

            self.set_item_value(item, actual_new_name)

    def update_attr(self, attr_name, item, is_boolean):
        if is_boolean:
            value = self.is_item_checked(item)
            self.set_item_text(item, "")
        else:
            text = self.get_item_text(item)
            try:
                value = float(text)
            except ValueError:
                self.revert_original_value(item, False)
                return

    def set_item_text(self, item, text):
        item.setText(text)

    def get_item_text(self, item):
        return item.text()

    def set_item_checked(self, item, checked):
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def is_item_checked(self, item):
        return item.checkState() == QtCore.Qt.Checked

    def set_item_attr(self, item, attr):
        item.setData(self.ATTR_ROLE, attr)

    def get_item_attr(self, item):
        return item.data(self.ATTR_ROLE)

    def set_item_value(self, item, value):
        item.setData(self.VALUE_ROLE, value)

    def get_item_value(self, item):
        return item.data(self.VALUE_ROLE)

    def get_full_attr_name(self, row, item):
        node_name = self.table_wdg.item(row, 1).data(self.VALUE_ROLE)
        attr_name = item.data(self.ATTR_ROLE)
        return "{0}.{1}".format(node_name, attr_name)

    def float_to_string(self, value):
        return "{0:.4f}".format(value)

    def revert_original_value(self, item, is_boolean):
        original_value = self.get_item_value(item)
        if is_boolean:
            self.set_item_checked(item, original_value)
        else:
            self.set_item_text(item, self.float_to_string(original_value))


if __name__ == "__main__":

    try:
        table_example_dialog.close() # pylint: disable=E0601
        table_example_dialog.deleteLater()
    except:
        pass
    
    filepath = r'Z:/vs_code_svad/prog_art23/render_submit/test/test_shot_data.json'

    table_example_dialog = MultiSubmitTableWindow()
    table_example_dialog.show()
