import maya.cmds as cmds
import time
import threading
import winsound

'''this code will save your work in maya automatically
 depending how much time do you want per each save '''

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

@setInterval(10.5)
def function():
    winsound.Beep(529, 500)
    cmds.file(save=True, force=True)
    print("FILE SAVED")
    
stop = function()
 # start timer, the first call is in .5 seconds
 # stop 
#stop = function()
#stop.set()