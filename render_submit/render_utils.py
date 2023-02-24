import platform
import os
import re
import subprocess
from pprint import pprint
import maya.cmds as mc

def get_renderable_camera():
    '''Get a list of renderable cameras

    :return: list of camera names
    :rtype: list of str
    '''
    cameras = mc.listCameras(p=True)
    renderCam =  []
    for camera in cameras:
        if mc.getAttr(camera +'.renderable'):
            renderCam.append(camera)
    if len(renderCam) > 1:
        mc.warning(f'More than one render camera. Using {renderCam[0]}' )
    elif not len(renderCam):
        renderCam.append('perspShape')
        mc.warning(f'No rendearble cameras found. Using {renderCam[0]}' )
    return renderCam
 

def build_directory(filepath=''):
    '''Creates a render directory relative to the out

    :param renderPath: _description_, defaults to ''
    :type renderPath: str, optional
    :return: _description_
    :rtype: _type_
    '''
    filepath = os.path.abspath(filepath)
    if not os.path.isdir(filepath):
        os.makedirs(filepath)
        if not os.path.isdir(filepath):
            mc.error(f'Unable to create directory: {filepath} \n Check permissions.')
            return False
        else:
            print(f'Created directory: {filepath}')
            return True
    else:
        print(f'Directory exists: {filepath}')
        return True  

def plugin_check(plugins):
    '''checks the loaded state of a plugin and loads it if needed
    provide the plugin in the name.ext format to support .py and .mll
    plugin in types

    :param plugins: a list of strings formatted in name.ext
    :type plugins: string or list
    ''' 
    plugins = plugins if isinstance(plugins, list) else [plugins]

    loaded_plugins =  mc.pluginInfo( query=True, listPlugins=True )

    success = True
    for plugin in plugins:
        if plugin.split('.')[0] not in loaded_plugins:
            try:
                mc.loadPlugin( plugin )
            except:
                success = False
                mc.warning('Could not load plugin {}'.format(plugin))
    return success

def unc_drive_table(remove=''):
    '''Create a table of drive letters and their corresponding unc paths

    :param remove: optionally remove a string to allow for more consise patths , defaults to ''
    :type remove: str, optional
    :return: _description_
    :rtype: _type_
    '''

    if platform.system() == "Windows":
        drives = subprocess.getoutput('net use')
        letters = re.findall(".?:", drives)
        networks = re.findall(r"\\\\.*$", drives, re.MULTILINE)
        networks = [n.rstrip().replace(remove, '') for n in networks]
        driveMap = dict(zip(letters, networks))
            
        if driveMap:
            return driveMap    
    else:
        print("Not submitting from windows, no drive letter substitution")
    
def unc_mapper(path, remove='', drivetable = {}):
    '''Remap a path from named letters to unc paths

    :param path: path
    :type path: string
    :param remove: optionally remove a string in the path, defaults to ''
    :type remove: str, optional
    :param driveTable: a dict keyed by drive letter, generated from uncDriveTable, defaults to {}
    :type driveTable: dict, optional
    :return: a substituted path
    :rtype: string
    '''
    if not drivetable:
        drivetable = unc_drive_table()
    #get the drive letter
    drive, tail = os.path.splitdrive(path)
    print (drive, tail)
    if ':' not in drive: return path.replace(remove,'')
    
    # we may not have a mapping for the drive, like a removable disk, so skip if that's the case.
    if drive not in drivetable: return path.replace(remove,'')
    
    if drivetable[drive]: return os.path.abspath(drivetable[drive] + tail)

if __name__ == '__main__':
    print ('Drive table: ')
    pprint(unc_drive_table)