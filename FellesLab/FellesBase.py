# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Felles lab parent classes
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

from time import time
from SupportClasses import FellesSampler, ExtendedRef, DataStorage
from SupportFunctions import sensorTypes
from collections import defaultdict
# ================================ Class ==================================== #
class FellesBaseClass(object):
    """
    Sensor parent class
    """
    # Class variables, when edited will affect **all** sensors
    sample_rate = 0.5 # Default sampling rate
    SAMPLING = True # Default start sampling
    SAVE = False
    # Create, Objects
    Sampler = FellesSampler # thread used to perform sampling
    FellesMetaData = {
        'idlig' : True, # The gui is updated, but data is not necessarily stored
        'sampling' : False, # The sampling of data should not start imediately
        'label' : None, # Some unique string
        'sample_speed' : 0.5, # Default sampling rate
        'unit' : '[]', # Unit of the sampled data
    } # Dictionary containing default meta data
    GuiMetaData = {
        'plot' : False, # To plot or not to plot...
        'time_span' : 20, # default plot range in seconds
        'color': 'red', # Plot line color
        'pos' : None, # Position of frame
        'size' : None, # Size of frame
        'style' : None, # frame style
    }
    DataProcessing = {
        'signalFiltering' : None, # Noise filter
        'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
        'calibrationCurve' : None, # Calibration curve
    }
    Data = DataStorage # Dictionary containing sampling data

    # List of object instances
    __refs__ = defaultdict(list)

    # ------------------------------- Method -------------------------------- #
    def __init__(self, module, module_metadata = {}, meta_data={}, gui_configuration={}, data_processing={}):
        """
        constructor
        """
        self.__refs__[self.__class__].append(ExtendedRef(self)) # Add instance to references

        self.ID = hex(id(self)) # ID used to look up objects (Will change for each run!)
        self.module = module # This is the reference to the Adam module

        meta_data.update(self.module.metaData) # Add module metadata to kwargs

        self.MetaData = self.FellesMetaData

        for (key, val) in module_metadata.iteritems():
            pass

        for (key,val) in meta_data.iteritems():
            self.SetMetaData(key,val)

        self.plot_config = gui_configuration
        self.data_config = data_processing

        self.data = self.Data(self) # Dict object reading and writing data, capable of reporting to onClose

        self.t0 = time()
        self.thread = self.Sampler(group=None, target=self.Sample, source=self)
        self.thread.start()

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def GetAllInstances(cls):
        for ref in cls.__refs__[cls]:
            inst = ref()
            if inst is not None:
                yield inst

    # ------------------------------- Method -------------------------------- #
    @staticmethod
    def EmptyIterator(iterable):
        try:
            first = next(iterable)
        except StopIteration:
            return None
        return True

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
    def GetMeassurements(self, event=None):
        pass


    # ------------------------------- Method -------------------------------- #
    def Sample(self, event=None):
        """
        TODO
        """
        self.data.Update( self.Timer(), self.GetMeassurements() )

    # ------------------------------- Method -------------------------------- #
    def StartSampling(self, event=None):
        """
        TODO
        """
        self.t0 = time()
        self.SAVE = True
        self.data.Restart(self.Timer(), self.module.get_analog_in())
        print "Sensor '%s' started at time: '%s' by event: '%s'" %(
                                       self.GetMetaData('label'), self.Timer(),
                                                       event.__class__.__name__)

    # ------------------------------- Method -------------------------------- #
    def PauseSampling(self, event=None):
        """
        TODO: Write
        """
        pass
        #self.StartSampling()
        #self.t0 = time()

    # ------------------------------- Method -------------------------------- #
    def StopSampling(self, event=None):
        """
        TODO
        """
        self.SAMPLING = False

        print "Instance '%s' terminated by event: '%s'" %(self.GetMetaData('label'), event.__class__.__name__)

    # ------------------------------- Method -------------------------------- #
    def UpdateData(self):
        """
        """
        pass

    # ------------------------------- Method -------------------------------- #
    def GetID(self):
        """
        """
        return hex(id(self))

    # ------------------------------- Method -------------------------------- #
    def HasID(self, ID):
        """
        """
        return 1 if self.GetID() == ID else 0

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Find(cls, ID):
        """
        """

        for cls,lst in cls.__refs__.iteritems():
            for inst in lst:
                if inst().GetID() == ID:
                    return inst()

    # ------------------------------- Method -------------------------------- #
    def FindAll(self):
        """
        """
        pass

    # ------------------------------- Method -------------------------------- #
    def UpdatePlotConfig(self, key, val):
        """
        """
        self.plot_config[key] = val

    # ------------------------------- Method -------------------------------- #
    def UpdateDataProcessing(self, key, fnc):
        """
        """
        self.data_config[key] = fnc

    # ------------------------------- Method -------------------------------- #
    def GetMetaData(self, key=None):
        """
        """
        return self.MetaData if not key else self.MetaData[key]

    # ------------------------------- Method -------------------------------- #
    def SetMetaData(self, key, val):
        """
        """
        self.MetaData[key] = val

    # ------------------------------- Method -------------------------------- #
    def UpdateSampleSpeed(self, event, caller):
        """
        Method updating the sample_speed
        """
        print "Updating '%s' sampling speed from '%s to '%s'"\
             %( self.GetMetaData('label'),\
                self.GetMetaData('sample_speed'),\
                event.GetValue() )

        self.SetMetaData('sample_speed', event.GetValue())

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        pass
