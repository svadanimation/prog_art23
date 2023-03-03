'''
Open a series of shots and submit to farm

There is an interesting decorator here:
http://josbalcaen.com/maya-python-progress-decorator/
Will probably pass in a class instance to the render loop instead of using a decorator

Ideally, we would like to have a progress bar that shows the progress of the
render loop in the main ui window.

probably makes sense to import this into a UI class that can update the progress window
not sure how to properly interrupt the loop if the user cancels the progress window

'''
# builtins
import winsound
import os
import time

# qt
from PySide2 import QtCore # pylint: disable=import-error
from PySide2 import QtWidgets # pylint: disable=import-error

import maya.cmds as mc # pylint: disable=import-error

# internal
from render_submit import vray_submit
from render_submit import shot_data


def open_scene(filepath):
    '''Open the scene file'''
    if not os.path.isfile(filepath):
        mc.warning(f'Error opening file {filepath} does not exist')
        return

    # open the scene
    try:
        mc.file(filepath, open=True, force=True)
    except Exception as ex:
        mc.warning(f'Exception {ex} opening scene: {filepath}')


# not sure how to yield the progress information
# attempt to pass class instance in
def render_shots(shots_data, 
                #  label=None,
                #  progress=None, 
                ui = None,
                audition=False):
    '''Given a dictionary of shot data, open the scene and submit to farm

    :param shots_data: dictionary of shots data, defaults to None
    :type shots_data: dict, optional
    :param audition: allows the scene loop to run without submission, defaults to False
    :type audition: bool, optional
    '''

    # validate the progress bar by making sure it is a ProgressWindow
    # if not isinstance(progress, render_submit.ui.ProgressWindow):
    #     progress = None

    # TODO: Think about if we should filter the active list here or on ui side
    # probably here
    # use a list comprehension to get the length of the active shots
    # filters into a list
    active_shots = [shot for shot in shots_data if shot.get('active')]

    # update progress bar if we have one
    # use is instance to check if it's a QProgressBar
    # if isinstance(progress, QtWidgets.QProgressBar):
    if isinstance(ui, QtWidgets.QMainWindow):
        if ui.submit_in_progress:
            return
        ui.progress_bar.setRange(0, len(active_shots))
        ui.progress_bar_label.setText("Submit In Progress")

        ui.submit_in_progress = True
        ui.update_visibility()

    for i, shot in enumerate(active_shots):
        
        # update the progress bar
        # if isinstance(progress, QtWidgets.QProgressBar):
        if isinstance(ui, QtWidgets.QMainWindow):
            # check for interrupt
            if not ui.submit_in_progress:
                cancel_sound()
                break
            current_file = os.path.basename(shot.get('file'))
            ui.progress_bar_label.setText(f"{current_file}: {i} (of {len(active_shots)})")
            ui.progress_bar.setValue(i)
            time.sleep(0.5)
            QtCore.QCoreApplication.processEvents()

        # this opens every scene
        filepath = shot.get('file')
        if not os.path.isfile(filepath):
            mc.warning(f'Error opening file {filepath} does not exist. SKIPPING')
            continue
        
        open_scene(filepath)

        res= shot.get('res')
        height = None
        width = None
        ASPECT_RATIO = 1.7777777777777777
        if res:
            height = res
            width = int(res*ASPECT_RATIO)
        vray_submit.apply_render_settings(
            # get the shot data
            cut_in = shot.get('cut_in'),
            cut_out = shot.get('cut_out'),
            height = height,
            width = width,
            filename = shot.get('filename'),
            outfile = shot.get('outfile'),
            step = shot.get('step')
        )

        # audtion mode skips submitting and just checks the render loop
        if not audition:
            make_movie = shot.get('movie')
            project = shot.get('osx')
            vray_submit.vray_submit_jobs(make_movie=bool(make_movie),
                                         project=bool(project))
        
        progress_sound()
    
    if isinstance(ui, QtWidgets.QMainWindow):
        ui.submit_in_progress = False
        ui.update_visibility()
    # play a sound when the loop is complete
    completion_sound()

def completion_sound():
    '''Play a sound when the loop is complete'''
    # for count in range(5):
    #     winsound.Beep(440-count*100, 100-count*2)
    winsound.Beep(440, 500)
    winsound.Beep(640, 500)
    winsound.Beep(540, 300)
    winsound.Beep(640, 1000)

def progress_sound():
    '''Play a sound when the loop updates'''
    winsound.Beep(440, 100)

def cancel_sound():
    '''Play a sound when the loop updates'''
    winsound.Beep(100, 500)
    winsound.Beep(80, 1000)

if __name__ == "__main__":
    # get the shot data
    shots_data = shot_data.load_shot_data(r'Z:/vs_code_svad/prog_art23/render_submit/test/test_shot_data.json')
    render_shots(shots_data, audition=True)
    