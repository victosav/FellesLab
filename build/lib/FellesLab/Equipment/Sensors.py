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

# from FellesLab.Utils.SupportFunctions import sensorTypes
from FellesLab.Utils.SupportClasses import *
from FellesLab.Utils.DataStorage import DataStorage


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
    sample_rate = 0.5 # Default sampling rate
    SAMPLING = True # Default start sampling

    # Create, Objects
    Sampler = FellesSampler # thread used to perform sampling
    Meta = dict # Dictionary containing meta data
    Data = DataStorage # Dictionary containing sampling data

    # List of object instances
    ___refs___ = []

    # ------------------------------- Method -------------------------------- #
    def __init__(self, module, module_configuration = {}, meta_data={}, gui_configuration={}, data_processing={}):
        """
        constructor
        args:
            module : instance 
            module_configuration
            meta_data
            GUI_configuration
            data_processing
        
        class variables:
        
        instance variables:
          self.module (instance)
          self.Data (instance)
          self.Meta (instance)
          self.Sampler (instance)
          self.thread (instance)
        """
        self.___refs___.append(ExtendedRef(self)) # Add instance to references

        self.ID = hex(id(self)) # ID used to look up objects (Will change for each run!)

        self.module = module
        meta_data.update(self.module.metaData) # Add module metadata to kwargs

        # Check for label, why?
        # Specific label for a sensor, e.g. 'Inlet Temperature', can be given
        # in the 'meta_data' argument as follows:
        #       meta_data = { ... , ... , 'label' : 'Inlet Temperature , ... }
        # Otherwise an automatically generated label:
        #       '<Sensor Type> <INT>'
        # e.g. 'Temperature 3', will be created.
        if not meta_data.has_key('label'):
            meta_data['label'] = '%s %d' %(self.__class__.__name__, len(sensorTypes()[self.__class__.__name__]))

        # Check for unit
        if not meta_data.has_key('unit'):
            meta_data['unit'] = ' '

        # Setting sampling speed (four cases are possible):
        if not meta_data.has_key('sample_speed'):
            meta_data['sample_speed'] = self.sample_rate

        self.plot_config = gui_configuration
        self.data_config = data_processing
        self.meta = self.Meta(**meta_data) # Dict object with **static** metadata
        self.data = self.Data(self) # Dict object reading and writing data, capable of reporting to onClose

        self.t0 = time()
        self.thread = self.Sampler(group=None, target=self.Sample, source=self)
        self.thread.start()

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        """
        Magic method, executed when the object is called.
        
        return: 
            object instance
        """
        return self

    # ------------------------------- Method -------------------------------- #
    def Timer(self):
        """
        Timer method, keeping track of the time since the sampling started
        
        return:
            Elapsed time
        """
        return time() - self.t0

    # ------------------------------- Method -------------------------------- #
    def Sample(self, event=None):
        """
        
        """
        self.data.Update( self.Timer(), self.module.get_analog_in() )

    # ------------------------------- Method -------------------------------- #
    def StopSampling(self, event=None):
        """
           asdf
        """
        self.SAMPLING = False

        print "Process '%s' terminated by event: '%s'" %(self.meta['label'], event)

    # ------------------------------- Method -------------------------------- #
    def UpdateSampleSpeed(self, event, caller):
        """
        Method updating the sample_speed
        """
        print "Updating '%s' sampling speed from '%s to '%s'"\
             %( self.meta['label'],\
                self.meta['sample_speed'],\
                event.GetValue() )

        self.meta['sample_speed'] = event.GetValue()

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        return '<%s.%s sensor_instance at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.ID
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
