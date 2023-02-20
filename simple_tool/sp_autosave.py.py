import threading
import winsound
import maya.cmds as mc

'''
class TimerThread(threading.Thread):
    def __init__(self, duration, callback):
        super().__init__()
        self.duration = duration
        self.callback = callback
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            self._stop_event.wait(self.duration)
            self.callback()

    def stop(self):
        self._stop_event.set()
        
'''

class TimerThread(threading.Thread):
    def __init__(self, duration, callback):
        super().__init__()
        self.duration = duration
        self.callback = callback
        self._stop_event = threading.Event()
        self._stop_requested = False

    def run(self):
        while not self._stop_event.is_set():
            self._stop_event.wait(self.duration)
            if self._stop_requested:
                break
            self.callback()

    def stop(self):
        self._stop_requested = True

def timer_callback():
    global timer_thread
    print("callback")
    print(threading.get_ident())
    
    winsound.Beep(529, 500)


    # timer_thread.stop()

    result = mc.promptDialog(
        title='Save prompt',
        message='Enter Seconds:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        tx = str(timer_thread.duration),
        cancelButton='Cancel',
        dismissString='Cancel')

    if result == 'OK':
        print("result ok")
        print(threading.get_ident())
        text = mc.promptDialog(query=True, text=True)
        text = [int(i) for i in text.split() if i.isdigit()][0]
        new_duration = timer_thread.duration
        if text:
            new_duration = int(text)
        timer_thread.duration = new_duration
    else:
        print("stop")
        print(threading.get_ident())
        # stop_timer()
        timer_thread.stop()
        winsound.Beep(129, 1000)

def setup_timer(duration=3):
    global timer_thread
    timer_thread = TimerThread(duration, timer_callback)
    timer_thread.start()
    print('setup')
    print(threading.get_ident())

def stop_timer():
    print('stopping')
    print(threading.get_ident())
    global timer_thread
    timer_thread.stop()    
    winsound.Beep(129, 1000)

if __name__ == '__main__':
    print('main')
    print(threading.get_ident())
    setup_timer()