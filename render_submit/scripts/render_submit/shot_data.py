'''
This module contains the functions to get the shot data from the json file
'''

import json
import os
import maya.cmds as mc # pylint: disable=import-error

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