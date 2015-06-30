# -*- coding: ascii -*-
"""

oooooooooooo       oooo oooo                    ooooo                 .o8      
`888'     `8       `888 `888                    `888'                "888      
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo. 
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      TODO
@author:       Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3), although credit is appreciated  
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:     
@change:       
@note:         

"""

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


    
