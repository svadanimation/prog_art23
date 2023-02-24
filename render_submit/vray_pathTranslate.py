'''
Post translate paths in vray scenes
'''

# built-ins
import os
import vray.utils as vu

# internal
from render_submit import constants
from render_submit import render_utils


GEOMETRY = 'GeomMeshFile'
BITMAP = 'BitmapBuffer'
SCENE = 'VRayScene'

def find_and_process_paths(debug=True):
    '''post translate python script to replace all drive mapped paths with unc paths

    :param debug: verbose printing, defaults to True
    :type debug: bool, optional
    '''
    local_drive_table = render_utils.uncDriveTable(remove = constants.NETWORK_SUFFIX)

    if debug: print ('Vray post translate paths: Finding meshes and bitmaps')

    nodes = []
    nodes.extend( vu.findByType(GEOMETRY) )
    nodes.extend( vu.findByType(BITMAP) )


    for node in nodes:
        if debug: print (f'Node: {node}')
        path = node.get('file')
        path = render_utils.uncMapper(path,
                                     remove = constants.NETWORK_SUFFIX,
                                     drivetable=local_drive_table)
        path = path.replace(os.sep, '/')
        if debug: print (f'Path: {path}')
        node.set('file', str(path))

    if debug: print ('Finding scenes')

    scenes=[]
    scenes.extend( vu.findByType(SCENE) )

    for scene in scenes:
        if debug: print (f'Scene {scene}')

        path = scene.get('filepath')
        path = render_utils.uncMapper(path,
                                     remove = constants.NETWORK_SUFFIX,
                                     drivetable=local_drive_table)
        path = path.replace(os.sep, '/')
        if debug: print ('Path: {path}')
        scene.set('filepath', str(path))

if __name__ == "__main__":
    find_and_process_paths()
