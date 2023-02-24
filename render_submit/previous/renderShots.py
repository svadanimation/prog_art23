import maya.cmds as mc
import maya.mel as mm
import winsound
import vray_standaloneSubmit as vss
reload(vss)

import sys
import os
import pprint

# auto render


import shotgunConnect as shotgunConnect
reload(shotgunConnect)

COMPONENT = 'Light'


def get_shot_data():

    projectID = shotgunConnect.getProjectFromCode(mc.optionVar( q="op_currProjectName" ))['id']
    sequences = shotgunConnect.getSequences(projectID)
    
    shot_data = []
    
    for seq in sequences:
         shots = shotgunConnect.getShotsFromSequence(seq['id'], projectID)
         for shot in shots:
             if shot['sg_status_list'] == 'ip':
                shot_data.append({
                                    'sequence': seq['code'],
                                    'shot': shot['code']
                                })
    return shot_data





def open_scene(seq, shot):
    try:
        shotgunConnect.pyop_openPipelineOpenItem('workshop', 3, seq, shot, COMPONENT, 0, 1, 0)
    except:
        print 'Probably a version error or might not exist, traceback through open pipeline'
        print 'or openPipeline hasnt been opened'






def renderShots(export=False):
    import time
    current_shot_data = get_shot_data()
    pprint.pprint(current_shot_data)
    confirmString = 'Shots flagged as "in progress" for render \r\n'
    for d in current_shot_data:
        confirmString += ('seq{} shot{} \r\n'.format(d['sequence'], d['shot']))
    
    result = mc.confirmDialog(
                title='Multiple Shot Submit',
                message=confirmString,
                button=['Proceed', 'Cancel'],
                defaultButton='Proceed',
                cancelButton='Cancel',
                dismissString='Cancel')

    if result == 'Cancel':
        return
    

    def progress(status):
        mc.progressWindow(e=True, step=1, status = status)
        time.sleep(.2)
        if mc.progressWindow(q=True, isCancelled=True):
            print 'Export cancelled by user.'
            mc.progressWindow( endProgress=True)
            return True
        return False
    
    # init progress window
    if current_shot_data:
        window = mc.progressWindow(	title='Rendering shots...', maxValue=len(current_shot_data)*3, status='Initializing...', isInterruptable=True )
    else:
        mc.error('No in progress shots found')
    
    for active_shot in current_shot_data:
        shot = active_shot.get('shot')
        seq = active_shot.get('sequence')

        if export and shot is not None and seq is not None:
            print 'Shot :', active_shot

            if progress('Opening seq {} shot {} '.format(seq, shot)): return

            open_scene(seq, shot)

            if progress('Translating seq {} shot {} '.format(seq, shot)): return

            vss.vray_standalone(pipeline=True, show_ui=False)

            if progress('Submitting seq {} shot {} '.format(seq, shot)): return



    mc.progressWindow(endProgress=1)
    for x in range(5):
        winsound.Beep(440-x*100, 100-x*2)



if __name__ == "__main__":
    renderShots(export=True)
    pass

