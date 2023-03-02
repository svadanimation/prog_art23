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
import json

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
def render_shots(shots_data, progress=None, audition=False):
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
    if progress:
        progress.minValue=0
        progress.maxValue=len(active_shots)

    for shot in active_shots:
        
        # update the progress bar
        if progress:
            # check for interrupt
            progres.progress_bar_label.setText(f"Processing operation: {i} (of {1})".format(i, number_of_operation))
            progress.progress_bar.setValue(i)
            progress.step()

        # this opens every scene
        open_scene(shot.get('filepath'))

        # stub, this may change
        vray_submit.apply_render_settings(
            # get the shot data
            cut_in = shot.get('cut_in'),
            cut_out = shot.get('cut_out'),
            height = shot.get('height'),
            width = shot.get('width'),
            filename = shot.get('filename'),
            outfile = shot.get('outfile'),
            step = shot.get('step')
        )

        # audtion mode skips submitting and just checks the render loop
        if not audition:
            vray_submit.vray_submit_jobs(make_movie=False)


    # play a sound when the loop is complete
    completion_sound()

def completion_sound():
    '''Play a sound when the loop is complete'''
    for count in range(5):
        winsound.Beep(440-count*100, 100-count*2)

if __name__ == "__main__":
    # get the shot data
    shots_data = shot_data.load_shot_data(r'Z:/vs_code_svad/prog_art23/render_submit/test/test_shot_data.json')
    render_shots(shots_data, audition=True)
    