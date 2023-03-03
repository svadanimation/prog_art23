'''
Multi Submit UI
TODO incorporate data flags instead of sorting by column

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

from render_submit.ui import add_file_dialog

from render_submit import shot_data
from render_submit import render_loop

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MultiSubmitTableWindow(QtWidgets.QMainWindow):
    '''Table for displaying and editing multi submit data
    '''

    ATTR_ROLE = QtCore.Qt.UserRole
    VALUE_ROLE = QtCore.Qt.UserRole + 1


    def __init__(self, parent=maya_main_window()):
        super(MultiSubmitTableWindow, self).__init__(parent)

        self.multi_select_dialog = add_file_dialog.MultiSelectDialog(parent=self)

        self.setWindowTitle("Multi Submit")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(600)
        
        # data
        self.column_headers = list(shot_data.SHOT_TEMPLATE.keys())
        self.column_types = list(shot_data.SHOT_TEMPLATE.values())
        self.shots_data = []
        self.active_file = None
        self.allow_duplicates = False
        self.submit_in_progress = False

        # ui
        self.create_menubar()
        self.create_widgets()
        self.create_layout()
        self.create_connections()



    def create_menubar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setNativeMenuBar(False)
        self.file_menu = self.menubar.addMenu("&File")
        self.file_menu.addAction("Open", self.open_file)
        self.file_menu.addAction("Save", self.save_file)
        self.file_menu.addAction("Save As", self.save_file_as)
        self.setMenuBar(self.menubar)

        self.recent_files_menu = QtWidgets.QMenu("Recent Files", self)
        self.file_menu.addMenu(self.recent_files_menu)
        self.file_menu.addAction("Clear Recents", self.clear_recent_files)

        self.table_menu = self.menubar.addMenu("&Table")
        # create the checkbox action
        allow_duplicates_action = QtWidgets.QAction('Allow Duplicates', self, checkable=True)
        allow_duplicates_action.setChecked(self.allow_duplicates)
        allow_duplicates_action.triggered.connect(self.toggle_allow_duplicates)
        self.table_menu.addAction(allow_duplicates_action)
        self.table_menu.addAction("Clear Table", self.clear_table)
        self.table_menu.addAction("Print Table", self.print_table)

        # Create a QActionGroup to manage the recent file actions
        self.recent_files_group = QtWidgets.QActionGroup(self)
        self.recent_files_group.setExclusive(True)
        self.recent_files_group.triggered.connect(self.open_recent_file)

        # Add some recent files
        recent_files = shot_data.load_recent_data()
        if recent_files:
            for recent_file in recent_files:
                self.add_recent_file(recent_file)

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
        self.table_wdg.setHorizontalHeaderLabels(self.column_headers)
        header_view = self.table_wdg.horizontalHeader()
        header_view.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.progress_bar_label = QtWidgets.QLabel("Submit Progress")
        self.progress_bar = QtWidgets.QProgressBar()

        self.cancel_button = QtWidgets.QPushButton("Cancel Submission (Esc)")
        self.submit_btn = QtWidgets.QPushButton("Submit")
        self.update_visibility()

        self.add_btn = QtWidgets.QPushButton("Add")
        self.search_btn = QtWidgets.QPushButton("Search")
        self.delete_btn = QtWidgets.QPushButton("Delete Row")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.table_wdg, 1)
        main_layout.addStretch()

        main_layout.addWidget(self.progress_bar_label)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

    def create_connections(self):
        self.set_cell_changed_connection_enabled(True)

        self.submit_btn.clicked.connect(self.submit)
        self.refresh_btn.clicked.connect(self.refresh_table)
        self.close_btn.clicked.connect(self.close_all)
        self.search_btn.clicked.connect(self.search_add_shots)
        self.add_btn.clicked.connect(self.add_shot)
        self.delete_btn.clicked.connect(self.delete_row)

        self.cancel_button.clicked.connect(self.cancel_submit)

        # self.table_wdg.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table_wdg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_wdg.customContextMenuRequested.connect(self.on_table_widget_context_menu_requested)

    def on_table_widget_context_menu_requested(self, pos):
        menu = QtWidgets.QMenu()

        item = self.table_wdg.itemAt(pos)
        if item is not None:
            print(f'Selected item: {item.text()}')
            row = item.row()
            open_action = menu.addAction('Open')
            copy_action = menu.addAction('Copy Text')
            delete_action = menu.addAction('Delete Row')
            action = menu.exec_(self.centralWidget().mapToGlobal(pos))

            if action == open_action:
                print('Open action triggered')
                self.open_maya_file(row)
            elif action == copy_action:
                print('Copy action triggered')
                self.copy_to_clipboard(item)
            elif action == delete_action:
                print('Delete action triggered')
                self.delete_row(row)

    def copy_to_clipboard(self, item):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(item.text())

    def open_maya_file(self, row):
        maya_file = self.table_wdg.item(row, 1).text()
        print(f'Opening Maya file: {maya_file}')
        render_loop.open_scene(maya_file)
        

    def close_all(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.close()
        self.close()

    def update_visibility(self):
        self.progress_bar_label.setVisible(self.submit_in_progress)
        self.progress_bar.setVisible(self.submit_in_progress)

        self.cancel_button.setVisible(self.submit_in_progress)
        self.submit_btn.setHidden(self.submit_in_progress)    
    
    def cancel_submit(self):
        self.submit_in_progress = False

    def toggle_allow_duplicates(self, checked):
        if checked:
            self.allow_duplicates = True
        else:
            self.allow_duplicates = False

    def search_add_shots(self):
        self.multi_select_dialog.show_add_dialog()

    def add_shots(self, shots):
        # print(f'Adding shots: {shots}')
        for add_filepath in shots:
            # Check if the shot already exists in the table
            if not self.allow_duplicates:
                if shot_data.shot_exists(self.shots_data, add_filepath):
                    print(f"Shot {add_filepath} already exists in the table. Skipping...")
                    continue

            # insert the data in place    
            shot_data.insert_shot(self.shots_data, add_filepath)


        self.refresh_table()

    def add_shot(self):
        loadpath = mc.fileDialog2(fileMode=1, fileFilter="Maya Files (*.ma *.mb)", okc='Add Shot')
        if loadpath: loadpath = loadpath[0]
        if loadpath:
            # Check if the shot already exists in the table
            if not self.allow_duplicates:
                if shot_data.shot_exists(self.shots_data, loadpath):
                    mc.confirmDialog(title="Shot Already Exists",
                                     message=f"The shot {loadpath} already exists in the table.",
                                     button=["OK"])
                    return

            shot_data.insert_shot(self.shots_data, loadpath)

            self.refresh_table()
    
    def print_table(self):
        print("Shot Data:")
        pprint(self.shots_data)

    def open_file(self):
        loadpath = mc.fileDialog2(fileMode=1, fileFilter="JSON (*.json)")
        if loadpath: loadpath = loadpath[0]
        if loadpath:
            shots_data = shot_data.load_shot_data(loadpath)
            if shots_data:
                self.shots_data = shots_data
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
            
        shots_data = shot_data.load_shot_data(loadpath)
        if shots_data:
            self.shots_data = shots_data
            self.active_file = loadpath
            self.add_recent_file(loadpath)
        self.refresh_table()

    def save_file(self):
        if self.active_file is None:
            self.save_file_as()
            return
        
        if os.path.isfile(self.active_file):
            shot_data.save_shot_data(self.active_file, self.shots_data)
        else:
            self.save_file_as()

    def save_file_as(self):
        savepath = mc.fileDialog2(fileMode=0, fileFilter="JSON (*.json)")
        if savepath: savepath = savepath[0]
        if savepath:
            shot_data.save_shot_data(savepath, self.shots_data)
            self.active_file = savepath
            self.add_recent_file(savepath)

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

    def clear_table(self):
        result = mc.confirmDialog(title="Clear Table",
                        message="This will remove all data from the table and cannot be undone.",
                        button=["Yes", "No"],
                        defaultButton="No",
                        cancelButton="No",
                        dismissString="No")
        if result == "No":
            return
        
        self.shots_data = []
        self.refresh_table()


    def set_cell_changed_connection_enabled(self, enabled):
        if enabled:
            self.table_wdg.cellChanged.connect(self.on_cell_changed)
        else:
            self.table_wdg.cellChanged.disconnect(self.on_cell_changed)

    def keyPressEvent(self, event):
        super(MultiSubmitTableWindow, self).keyPressEvent(event)
        event.accept()

        if event.key() == QtCore.Qt.Key_Escape:
            self.cancel_submit()

    def showEvent(self, e):
        super(MultiSubmitTableWindow, self).showEvent(e)
        self.refresh_table()

    def refresh_table(self):
        if not self.shots_data:
            self.table_wdg.setRowCount(0)
            return

        self.set_cell_changed_connection_enabled(False)
        self.table_wdg.setRowCount(0)
        for i, shot in enumerate(self.shots_data):

            self.table_wdg.insertRow(i)

            self.insert_item(i, 0, "", "active", shot['active'], True)
            self.insert_item(i, 1, str(shot['file']), None, shot['file'], False)

            for j, key in enumerate(self.column_headers):
                if j < 2:
                    continue
                self.insert_item(i, j, str(shot[key]), key, shot[key], False)

        self.set_cell_changed_connection_enabled(True)

    def submit(self):
        self.set_cell_changed_connection_enabled(False)

        active_shots = []
        # Smarter to operate on the actual dict instead of the table
        # for i in range(self.table_wdg.rowCount()):
        #     item = self.table_wdg.item(i, 0)
        #     if item.checkState() == QtCore.Qt.Checked:
        #         active_shots.append(self.shots_data[i])
        
        for shot in self.shots_data:
            if shot['active']:
                active_shots.append(shot)

        if active_shots:
            render_loop.render_shots(active_shots, 
                                    #  label = self.progress_bar_label,
                                    #  progress=self.progress_bar,
                                    ui = self,
                                    audition=True)
        else:
            mc.confirmDialog(title="No Shots Selected",
                             message="No shots are selected to submit.",
                             button=["OK"])

        self.set_cell_changed_connection_enabled(True)

    def insert_item(self, row, column, text, attr, value, is_boolean, disable=False):
        item = QtWidgets.QTableWidgetItem(text)
        self.set_item_attr(item, attr)
        self.set_item_value(item, value)
        if disable:
            item.setFlags(QtCore.Qt.NoItemFlags)
        if is_boolean:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.set_item_checked(item, value)
        self.table_wdg.setItem(row, column, item)

    def on_cell_double_clicked(self, row, column):
        self.set_cell_changed_connection_enabled(False)
        item = self.table_wdg.item(row, column)
        print(f'Cell {row}, {column} double-clicked: {item.text()}')
        self.set_cell_changed_connection_enabled(True)

    def on_cell_changed(self, row, column):
        self.set_cell_changed_connection_enabled(False)

        item = self.table_wdg.item(row, column)
        header = self.get_column_header(column)

        if column == 1:
            self.update_shots_data(row, header, item, is_locked=True)
        elif column == 2:
            self.update_shots_data(row, header, item)
        elif column >= 3:
            self.update_shots_data(row, header, item, is_int=True)
        else:
            is_boolean = column == 0
            # self.update_attr(self.get_full_attr_name(row, item), item, is_boolean)
            
            # get the key/header from the item
            self.update_shots_data(row, header, item, is_boolean)


        self.set_cell_changed_connection_enabled(True)


    def update_shots_data(self, row, header, item,
                          is_locked=False, 
                          is_boolean=False, 
                          is_int=False ):
        if is_locked:
            self.revert_original_value(item, False)
            return
        if is_boolean:
            value = self.is_item_checked(item)
            self.set_item_text(item, "")
        elif is_int:
            text = self.get_item_text(item)
            try:
                value = int(float(text))
            except ValueError:
                self.revert_original_value(item, False)
                return
        else:
            value = self.get_item_text(item)

        self.shots_data[row][header] = value

    def delete_row(self, row=None):
        if row is None:
            row = self.table_wdg.currentRow()

        self.table_wdg.removeRow(row)

        for i, _ in enumerate(self.shots_data):
            if i == row:
                self.shots_data.pop(i)
                break

        self.refresh_table()

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
    
    def get_key_name(self,  item):
        attr_name = item.data(self.ATTR_ROLE)
        return attr_name
    
    def get_column_header(self, column):
        key = self.table_wdg.horizontalHeaderItem(column).text()
        return key

    def float_to_string(self, value):
        return "{0:.4f}".format(value)
    
    def int_to_string(self, value):
        return int(value)

    def revert_original_value(self, item, is_boolean=False, is_int=False):
        original_value = self.get_item_value(item)
        if is_boolean:
            self.set_item_checked(item, original_value)
        elif is_int:
            self.set_item_text(item, self.int_to_string(original_value))
        else:
            self.set_item_text(item, original_value)

if __name__ == "__main__":

    try:
        table_example_dialog.close() # pylint: disable=E0601
        table_example_dialog.deleteLater() # pylint: disable=E0601
    except:
        pass
    
    table_example_dialog = MultiSubmitTableWindow()
    table_example_dialog.show()
