import maya.cmds as mc
import threading
import winsound

def setInterval():
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                global auto_save_interval
                interval = auto_save_interval
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

global auto_save_interval
global auto_save_stop
auto_save_interval = 1
auto_save_stop = None


@setInterval()
def auto_save_prompt():
    winsound.Beep(529, 500)
    # create a modal confirm dialog that says
    # https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/promptDialog.html

    
    # always stop on each cycle so we can reset the interval
    global auto_save_stop
    global auto_save_interval 
    auto_save_stop.set()

    '''
    interval = 10
    result = mc.promptDialog(
		title='Autosave reminder',
		message='Enter Duration:',
        tx = str(auto_save_interval),  
		button=['Save', 'Wait'],
		defaultButton='OK',
		cancelButton='Wait',
		dismissString='Kill')
    
    text = mc.promptDialog(query=True, text=True)
    if text.isdigit():
        interval = int(text)

    if result == 'Save':
        # put save code here
        print('saving')
        setup_autosave(interval)
    elif result == 'Wait':
        print('waiting')
        setup_autosave(interval)
    else:
        print ('stopping')
    '''

    
 # start timer, the first call is in .5 seconds
def setup_autosave(interval):
    global auto_save_interval
    global auto_save_stop
    auto_save_interval = interval
    auto_save_stop = auto_save_prompt()
 # stop 
#stop.set()
# auto_save_stop.set()
setup_autosave(5)