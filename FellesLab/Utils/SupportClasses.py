# -*- coding: ascii -*-
"""

oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:
@author:       Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3)
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:

"""
from time import sleep, time
import weakref
from multiprocessing.managers import SyncManager
from multiprocessing import Process
import multiprocessing

from threading import Thread

from DataStorage import SensorRealTimeData
    
# ================================ Class ==================================== #
# class FellesNamespace(Namespace):
#     """
#     
#     """
#     # ------------------------------- Method -------------------------------- #
#     def __init__(self, *args, **kwargs):
#         super(FellesNamespace).__init__(*args, **kwargs)

# ================================ Class ==================================== #
# class FellesManager(SyncManager):
#     """
#     Sugar ...
#     """
#     # ------------------------------- Method -------------------------------- #
#     def __init__(self, *args, **kwargs):
#         """
#         Constructor
#         """
#         super(FellesManager, self).__init__()

# ================================ Class ==================================== #
class FellesSampler(Thread):
    """
    Sugar class
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, group=None, target=None, *args, **kwargs):
        self.target = target
        self.source = kwargs['source']

        super(FellesSampler, self).__init__( )

    # ------------------------------- Method -------------------------------- #
    def run(self):
        """
        Method started when "instance.start()" is called
        
        The thread will call "source.target()" at a rate determined by "sample 
        rate" in the caller. 
        """
        while self.source.SAMPLING:
            self.target()
            sleep(self.source['sample_speed'])


# ================================ Class ==================================== #
class GuiUpdater(Thread):
    """
    Sugar class
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, source, target, *args, **kwargs):
        self.frame = target
        self.source = source

        super(GuiUpdater, self).__init__(None)

    # ------------------------------- Method -------------------------------- #
    def run(self):
        """
        Method started when "instance.start()" is called
        
        The thread will call "source.target()" at a rate determined by "sample
        rate" in the caller. 
        """
        while self.source.SAMPLING:
            self.frame(self)
            sleep(1)


# ================================ Class ==================================== #
class ExtendedRef(weakref.ref):
    """
    Weakreference class, creates an alias to "referee". 
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, referee, callback=None):
        self.referee = referee
        super(ExtendedRef, self).__init__(referee, callback)

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        return self.referee()
