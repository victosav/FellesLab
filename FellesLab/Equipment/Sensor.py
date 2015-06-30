# -*- coding: ascii -*-
"""

oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Felles lab GUI graphics parent classes
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

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"

#__revision__  = "$Rev: 155 $"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"


from threading import Thread
from multiprocessing import Process
from time import sleep, time
import weakref
from collections import namedtuple
from adam_modules import *
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub


from random import random


def sensorTypes():
    """
    
    Temperature: list( <weakref at ; to obj.instances>] )
    Volume: list( <weakref at ; to obj.instances> )
    """

    types = {}
    for s in Sensor.___refs___:
        if not types.has_key(s().__class__.__name__):
            types[s().__class__.__name__] = [s]
        else:
            types[s().__class__.__name__].append(s)
    return types
# ================================ Class ==================================== #
# class DataStorage(namedtuple):
#     """
#     asdf
#     """
#     def __init__(self, *args, **kwargs):
#
#         for k,v in kwargs.iteritems():
#             self.k = v

# ================================ Class ==================================== #
class RealTimeData(namedtuple('RealTimeData', 'min max val')):
    """

    """
#     def __init__(self, **kwargs):
#         print kwargs
#         if not kwargs['min']:
#             kwargs['min'] = 1e-99
#         if not kwargs['max']:
#             kwargs['min'] = 1e99
#         if not kwargs['val']:
#             kwargs['min'] = float
#
#         self(kwargs)
#         for k,v in kwargs.iteritems():
#             self.k = v

    def __str__(self):
        print self.val # "Sensor reading %.2f" %(self.val)

# ================================ Class ==================================== #
class SensorMetaInformation(dict):
    def __init__(self, *args, **kwargs):
        super(SensorMetaInformation).__init__(*args, **kwargs)

# ================================ Class ==================================== #
class StopAtOutputValue:
    def __init__(self, *args, **kwargs):
        print "Simulation will be stopped at..."
# ================================ Class ==================================== #
class ExtendedRef(weakref.ref):
    """
    Weakreference class
    """
    def __init__(self, ref, callback=None):
        self.ref = ref
        super(ExtendedRef, self).__init__(ref, callback)

    def __call__(self):
        return self.ref
# ================================ Class ==================================== #
class Sensor(dict):
    """
    Sensor parent class
    """
    # Class variables, when edited will affect **all** sensors
    sample_rate = 1.7 # Default sampling rate
    # data = RealTimeData # Data History
    SAMPLING = True # Default start sampling
    thread = Process #

    # List of object instances
    ___refs___ = []

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        constructor
        """
        self.___refs___.append(ExtendedRef(self)) # Add instance to references

        # Instance variables, when edited will only affect the specific sensor
        if not kwargs.has_key('module'):
            Exception("The address if the Adam module")

        self.module = kwargs['module']

        # Check for label
        if not kwargs.has_key('label'):
            kwargs['label'] = '%s %d' %(self.__class__.__name__, len(sensorTypes()[self.__class__.__name__]) )

        # Check for unit
        if not kwargs.has_key('unit'):
            kwargs['unit'] = ' '

        # Setting sampling speed (four cases are possible):
        # 1. User provides 'sample_rate' but not 'sample_speed'
        if kwargs.has_key('sample_rate') and not kwargs.has_key('sample_speed'):
            self['sample_speed'] = kwargs['sample_rate']
        # 2. User does not provide 'sample_rate', but 'sample_speed'
        elif not kwargs.has_key('sample_rate') and kwargs.has_key('sample_speed'):
            self['sample_speed'] = kwargs['sample_speed']
        # 3. User provides both 'sample_rate' and 'sample_speed'
        elif kwargs.has_key('sample_rate') and kwargs.has_key('sample_speed'):
            print "Provided both sample speed and sample rate"
            self['sample_speed'] = kwargs['sample_rate']
        # 4. User provides neither 'sample_rate' or 'sample_speed'
        else:
            self['sample_speed'] = self.sample_rate # Default use "sample rate"

        # Check for events...
        if kwargs['events']:
            for (index,event) in enumerate(kwargs['events']):
                kwargs['events'][index] = event(self)

        self.process = self.thread(target=self.StartSampling)
        self.metadata = namedtuple('MetaData', kwargs.keys())(**kwargs)
        self.data = RealTimeData(1,2,3)

        super(Sensor, self).__init__(*args, **kwargs)

        self.Idle_sampling()

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        pass
    # ------------------------------- Method -------------------------------- #
    def Identify(self):
        return self
    # ------------------------------- Method -------------------------------- #
    def Idle_sampling(self):
        """
            asdf
        """
        time()
        self.process.start()

    # ------------------------------- Method -------------------------------- #
    def StartSampling(self, event=None):
        """
            asdf
        """
        while self.SAMPLING:
            sleep(self['sample_speed'])
            print "Sampling speed %.2f from %s" %(round(self['sample_speed'],2), self['label'])
            self.Change_rate()
            pub.sendMessage("Sampled %s" %(self['label']), True)
#            self.data.val = 1
#            print self.data

        self.StopSampling()
    # ------------------------------- Method -------------------------------- #
    def StopSampling(self, event=None):
        """
           asdf
        """
        print "Terminating process '%s'" %(self['label'])
        #self.process.terminate()
    # ------------------------------- Method -------------------------------- #

    # ------------------------------- Method -------------------------------- #
    def Change_rate(self, event=None):
        """
            asdf
        """
        self['sample_speed'] -= random()
        if self['sample_speed'] < 0.1:
            self.SAMPLING = False

# ================================ Class ==================================== #
class Temperature(Sensor):
    """
        Temperature sensor class
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        self.TEST = 0000
        super(Temperature, self).__init__(*args, **kwargs)

# ================================ Class ==================================== #
class Voltage(Sensor):
    """
        Voltage sensor class
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        self.TEST = 0000
        super(Voltage, self).__init__(*args, **kwargs)
