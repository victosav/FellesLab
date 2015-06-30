import threading
import time

class SimpleEventTimer(threading.Thread):
    def __init__(self, event, sampling_time, threadID=1, name='timer', counter=1):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.do_run = True
        self.event = event
        self.sampling_time = sampling_time


    def run(self):
        while self.do_run:
            self.event()
            time.sleep(self.sampling_time)

    def stop(self):
        self.do_run = False


    