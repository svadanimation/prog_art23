import maya.cmds as cmds
import time
import threading
import winsound

def save_file():
    cmds.file(save=True, force=True)
    print("FILE SAVED")
    


def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

@setInterval(20.5)
def function():
    winsound.Beep(529, 500)
    cmds.file(save=True, force=True)
    print("FILE SAVED")
    
stop = function()
 # start timer, the first call is in .5 seconds
 # stop 
#stop = function()
#stop.set()