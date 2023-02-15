'''
This exports current animation as an Atom export 
and creates new file with new jack_rig 
Imports animation to fix glitches.
Does not inport any other objects.

Example: 
    Given a file using the jack rig
    Select the TSM2Controls set

    Execute this file.

TODO:
    - Put loose code in function
    - Create a if __name__ == 'main fn
    - Fix namespaces
    - Find shelf button pic
    - Try to keep same perspective in new file

Author:
    Eleanor Kim
'''
import maya.cmds as mc
import os

#constants
TEMP_FILE_PATH = os.path.abspath('z:/temp.atom')
JACK_FILE_PATH = os.path.abspath(r"K:\Animation\Library\rigs\BodyMech_MegaPack\scenes\jack_rig.ma")
CONTROL_SET_NAME = 'TSM2Controls'
ATOM_PLUGIN = 'atomImportExport.mll'
min_key= mc.playbackOptions(min=True, q=True)
max_key= mc.playbackOptions(max=True, q=True)
NAMESPACE = 'jack_rig'
NODE = 'Character'
CONTROL_LIST = ['.TRUNK', 
                '.Hips', 
                '.Torso', 
                '.Neck', 
                '.Head', 
                '.ARMS', 
                '.Arm_L', 
                '.Arm_R', 
                '.HandL', 
                '.HandR', 
                '.LEGS', 
                '.LegL', 
                '.LegR', 
                '.FootL', 
                '.FootR', 
                '.ToeToggle', 
                '.VIS_TRACKERS']

def plugin_check(plugin):
    try:
        mc.loadPlugin(plugin, quiet=True)
    except:
        mc.error(f'unable to load {plugin}')
        
def get_namespace_from_file(filename):
    base_file = os.path.basename(filename)    
    namespace = os.path.splitext(base_file)[0]
    return namespace
     
def load_atom(filename, import_file=False):
    '''
    Loads an atom file.
    Requires an active selection in maya
    for both import and export
    '''
    
    # make sure atom is loaded
    plugin_check(ATOM_PLUGIN)
    
    # make sure the directory is there beofre continuing
    if not os.path.isdir(os.path.dirname(filename)):
        mc.warning(f'{filename} is not a valid directory')
        return

    # get the base filename to use as a namespace
    namespace = get_namespace_from_file(filename)    
    # construct options strings using () to improve readability
    export_options = ( 
                'precision=8;'
                'statics=1;'
                'baked=1;'
                'sdk=0;'
                'constraint=0;'
                'animLayers=0;'
                'selected=selectedOnly;'
                'whichRange=1;'
                'range=1:10;'
                'hierarchy=none;'
                'controlPoints=0;'
                'useChannelBox=1;'
                'options=keys;'
                'copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0'
                 )

    import_options = (
                ';'
                ';'
                'targetTime=3;'
                'option=scaleReplace;'
                'match=hierarchy;'
                ';'
                'selected=selectedOnly;'
                'search=;replace=;prefix=;'
                'suffix=;'
                'mapFile=;'
                )
                
    if import_file:            
        # import the file
        mc.file(filename, 
                i=True,  
                type = "atomImport",
                ra = True,
                namespace = namespace,
                options=import_options)
    else:
        # export the file using
        mc.file(filename,
                force=True,
                options=export_options,
                ch=True,
                typ="atomExport", 
                es=True)

def get_controls(set=''):
    
    if set:
        control_set = set
    else:
        control_set_selection = mc.ls(sl=True)
    
        if not control_set_selection:
            mc.warning("no controls selected, select the TSM2Controls set in your outliner")
            return
 
        control_set = control_set_selection[-1]

            
    if not control_set.endswith(CONTROL_SET_NAME):
        mc.warning("no controls selected, did you select the TSM2Controls")
        return
    controls_selection = mc.sets(control_set, q=True)
    if controls_selection:
        return controls_selection

vis_data = []

for control_e in control_list:
    value = mc.getAttr(NAMESPACE + ':' + NODE + control_e)
    vis_data.append(value)
         
# get the rig controls        
rig_controls = get_controls()


#promt user to save file
print("Saving file")        
mc.file(save=True)   

# select the controls
mc.select(rig_controls)

#get current time slider min and max
print(min_key)
print(max_key)

#note visibility of orig file
print("saving visibility")
print(f'Value of {control_e} is {value}')

# export the atom file to the temp file path
print("Exporting atom file")        
load_atom(TEMP_FILE_PATH)

# make a new scene
print("New file")        
mc.file(new=True, f=True)

#set timeslider
print("setting new timeslider")
mc.playbackOptions(min= min_key)
mc.playbackOptions(max= max_key)

# create a reference
print("Making ref file")
#multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
# jack_file_path = mc.fileDialog2(fileFilter=multipleFilters, fileMode=1, dialogStyle=2, okc='Select')

namespace = get_namespace_from_file(JACK_FILE_PATH)       
mc.file(JACK_FILE_PATH, r=True, namespace = namespace)

# make a selection
print("Selecting controls")        
sel= get_controls(namespace + ':' + CONTROL_SET_NAME)
mc.select(sel, replace=True)


# import the atom file
print("Importing atom file")        
load_atom(TEMP_FILE_PATH, import_file=True)  

#setting the limb visibility in new file
for control_e, value in zip(control_list, vis_data):
    try:
        mc.setAttr(NAMESPACE + ':' + NODE + control_e, value)
        print(f'Value of {control_e} set to {value}')
    except:
        mc.warning(f"Error setting value of {control_e} to {value}")
   
for x in control_list:
    node = ('jack_rig:Character')
    att_name = node + x
    print(att_name)       
