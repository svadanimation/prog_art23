'''
This module contains the functions to get the shot data from the json file
'''

import json
import os
import maya.cmds as mc # pylint: disable=import-error
from pprint import pprint

appdata = os.getenv('APPDATA')
recents_path = os.path.join(appdata, 'render_submit', 'recents.json')

SHOT_TEMPLATE = {
                'active': True,
                'file': '',
                'note': '',
                'cut_in': '',
                'cut_out': '',
                'res': '',
                'step': '',
                'movie': True, 
                'osx': False 
                }

SHOT_TEMPLATE_TYPE = {
                'active': 'bool',
                'file': 'str',
                'note': 'str',
                'cut_in': 'int',
                'cut_out': 'int',
                'res': 'int',
                'step': 'int',
                'movie': 'bool',
                'osx': 'bool'
                }

def validate_shot_data(shots_data):
    '''
    This function is called by the UI to conform the shot data
    '''
    # if the shot data doesn't have the correct keys, throw it away
    # consider other cleanup if it is close
    if isinstance(shots_data, list):
        for shot in shots_data:
            if not isinstance(shot, dict):
                mc.warning('Shot is not a dictionary')
                return False
            for key in SHOT_TEMPLATE:
                if key not in shot:
                    mc.warning(f'Shot data is missing key: {key}')
                    return False
        return True
    else:
        mc.warning('Shots data is not a list')
        return False

def reorder_shots(shots_data, new_order):
    '''Reorders the shot data'''
    shot_list = {shots_data[id] for id in shots_data if id in shots_data}
    return shot_list

def replace_shot(shots_data, id, replacement):
    shots_data[id] = replacement

def insert_shot(shots_data, filepath, id=None):
    '''Inserts a shot into the shot data
    '''
    shot = SHOT_TEMPLATE.copy()
    shot['file'] = filepath
    if id is None:
        shots_data.append(shot)
    else:
        shots_data.insert(id, shot)

    return shots_data

def shot_exists(shots_data, filepath):
    '''Checks if a shot already exists in the shot data
    '''
    for shot in shots_data:
        if shot['file'] == filepath:
            return True
    return False

def remove_shot(shots_data, filepath=None, id=None):
    '''Removes a shot from the shot data
    '''
    if filepath:
        for shot in shots_data:
            if shot['file'] == filepath:
                shots_data.remove(shot)
                return shots_data
    if id:
        shots_data.pop(id)
        return shots_data
    
    mc.warning('No shot found to remove')
    return shots_data


def load_shot_data(filepath):
    '''
    This function is called by the UI to get the shot data
    '''
    # validate the file path
    if not os.path.isfile(filepath):
        mc.warning(f'File not found: {filepath}')
        return None

    with open(filepath, 'r', encoding='ascii') as f:
        try:
            shots_data = json.load(f)
        except json.JSONDecodeError as err:
            print(f'Unable to load file: {err.doc} \n'
                f'Pos: {err.pos} '
                f'Line: {err.lineno} '
                f'Column: {err.colno} ')
            mc.confirmDialog(title='Error',
                             message=f'Unable to load file: {filepath}',
                             button=['OK'], defaultButton='OK', 
                             cancelButton='OK', dismissString='OK')
            return None

    if validate_shot_data(shots_data):
        return shots_data

def save_shot_data(filepath, shots_data):
    '''
    This function is called by the UI to save the shot data
    '''
    # validate the path
    if not os.path.isdir(os.path.dirname(filepath)):
        mc.warning(f'Directory not found: {filepath}')
        return None
  
    with open(filepath, 'w', encoding='ascii') as f:
        try:
            json.dump(shots_data, f, indent=4)
        except ValueError as err:
            mc.confirmDialog(title='Error',
                             message=f'Unable to save file: {filepath} \n {err}',
                             button=['OK'], defaultButton='OK', 
                             cancelButton='OK', dismissString='OK')
            return None

def save_recent_data(recent_files):
    '''
    This function is called by the UI to save the recent files
    '''
    if build_directory(recents_path):
        with open(recents_path, 'w', encoding='ascii') as f:
            json.dump(recent_files, f, indent=4)

def load_recent_data():
    '''
    This function is called by the UI to load the recent files
    '''
    if not os.path.isfile(recents_path):
        print(f'No recent files found: {recents_path}')
        return 

    with open(recents_path, 'r', encoding='ascii') as f:
        recent_files = json.load(f)
    return recent_files if recent_files else None

def build_directory(filepath: str):
    '''Creates a folder if it doesn't exit
    '''
    filepath = os.path.abspath(filepath)
    dirpath = os.path.dirname(filepath)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
        if not os.path.isdir(dirpath):
            mc.error(f'Unable to create directory: {dirpath} \n Check permissions.')
            return False
        else:
            print(f'Created directory: {dirpath}')
            return True
    else:
        # print(f'Directory exists: {dirpath}')
        return True
    
if __name__ == '__main__':
    test_shot_path = 'Z:\\VSCODE\\prog_art23\\render_submit\\test\\test_shot_data.json'
    pprint(load_shot_data(test_shot_path))


# Class to make changes to change keys and pairs within any subdict of a given key
class FileEditor():
    def __init__(self, file_info=None, file=None):

        if file_info:
            self.shot_list = file_info
        elif file:
            with open(file) as file:
                self.shot_list = json.load(file)
        else:
            self.shot_list = []

        self.id_format = {  "note" : None,
                            "cut_in" : None,
                            "cut_out" : None,
                            "infile" : None,
                            "outfile" : None,
                            "res" : None,
                            "step" : None,
                            "active" : None     }

    def update_file(self, file):
        with open(file, 'w') as file:
            json.dump(self.shot_list, file)

    def add_shot(self, name=None, start_frame=None, end_frame=None, in_path=None, out_path=None, resolution=["720", "1280"], step=1, active=False):
        input_data = [name, start_frame, end_frame, in_path, out_path, resolution, step, active]
        edited_format = self.id_format

        if id in self.shot_list:
            # mc.warning("This shot already exists. Select a different shot or rename shot")
            return
        
        for data in edited_format:
            edited_format[data] = input_data[list(edited_format).index(data)]
        self.shot_list.append(edited_format)
        return self.shot_list

    def remove_shot(self, id=None):
        self.shot_list.pop()
        return self.shot_list

    def rearrange_shot(self, order=[]):
        if not order:
            # mc.warning('Please input the order you would like to rearrange your shots')
            return

        else:
            self.shot_list = {id:self.shot_list[id] for id in order if id in order}
        return self.shot_list

    def replace_shot(self, id, replacement_id={}):
        self.shot_list[id] = replacement_id

'''

TESTING:

test_path = get_shot_data(test_shot_path)
test_editor = FileEditor(file_info=test_path)
pprint(test_editor.shot_list, sort_dicts=False)

test_editor.add_shot(name="test_name_two", start_frame="0", end_frame="100", in_path="test_in", out_path="test_out")
pprint(test_editor.shot_list, sort_dicts=False)

test_editor.remove_shot(-1)
pprint(test_editor.shot_list, sort_dicts=False)

'''