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
@license:      Free (GPL.v3)
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
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

from threading import Thread
from multiprocessing import Process
from time import sleep, time
from adam_modules import *

#from FellesLab.Utils.SupportFunctions import sensorTypes
from FellesLab.Utils.SupportClasses import *
from FellesLab.Utils.DataStorage import *


# ............................... Function .................................. #
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
class Sensor(dict):
    """
    Sensor parent class
    """
    # Class variables, when edited will affect **all** sensors
    sample_rate = 1.7 # Default sampling rate
    SAMPLING = True # Default start sampling
    thread = FellesSampler #
    Meta = MetaData()

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
            # Result: '<Sensor Type> <INT>', e.g. 'Temperature 1'
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

        # Create instance of process, **not** started here.
        self.process = self.thread(group=None, target=self.StartSampling, source=self)
        
        SensorRealTimeData[kwargs['label']] = 0.0


        super(Sensor, self).__init__(*args, **kwargs)

        # Start process in "idle" mode, i.e. without storing data
        self.Idle_sampling()

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        return self

    # ------------------------------- Method -------------------------------- #
    def Idle_sampling(self):
        """
            asdf
        """
        self.time = time()
        self.calls = 0
        self.process.start()

    # ------------------------------- Method -------------------------------- #
    def StartSampling(self, event=None):
        """
            asdf
        """
        SensorRealTimeData.__setitem__(self, self['label'], self.module.get_analog_in())

        self.calls += 1
        if self.calls > 10:
            self.SAMPLING=False

    # ------------------------------- Method -------------------------------- #
    def StopSampling(self, event=None):
        """
           asdf
        """
        print "Process '%s' terminated by event: '%s'" %(self['label'], event)
        event.stop()

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        return '<%s.%s sensor_instance at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )

# ================================ Class ==================================== #
class Temperature(Sensor):
    """
        Syntactic sugar... 
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Temperature, self).__init__(*args, **kwargs)

# ================================ Class ==================================== #
class Voltage(Sensor):
    """
        Syntactic sugar... 
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Voltage, self).__init__(*args, **kwargs)
