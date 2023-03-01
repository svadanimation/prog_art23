'''
This module contains the functions to get the shot data from the json file
'''

import json
import os
import maya.cmds as mc # pylint: disable=import-error

appdata = os.getenv('APPDATA')
recents_path = os.path.join(appdata, 'render_submit', 'recents.json')

def conform_shot_data(shots_data):
    '''
    This function is called by the UI to conform the shot data
    '''
    # if the shot data doesn't have the correct keys, throw it away
    # consider other cleanup if it is close
    pass

def get_shot_data(filepath):
    '''
    This function is called by the UI to get the shot data
    '''
    # validate the file path
    if not os.path.isfile(filepath):
        mc.warning(f'File not found: {filepath}')
        return None

    with open(filepath, 'r', encoding='ascii') as f:
        shots_data = json.load(f)

    return shots_data

def save_shot_data(filepath, shots_data):
    '''
    This function is called by the UI to save the shot data
    '''
    # validate the file path
    if not os.path.isfile(filepath):
        mc.warning(f'File not found: {filepath}')
        return None
    with open(filepath, 'w', encoding='ascii') as f:
        pass
        # avoid overwriting the file for now
        # json.dump(shots_data, f, indent=4)

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
        print(f'Directory exists: {dirpath}')
        return True