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

from time import time, sleep
from SupportClasses import ExtendedRef, DataStorage, MyThread

from collections import defaultdict
from threading import Thread, Lock
import os
from time import localtime
from calendar import weekday

SAMPLE = True
IDLE = False

# ================================ Class ==================================== #
class FellesBaseClass(MyThread):
    """
    Thread 
    """
    __refs__ = defaultdict(list)
    __sfer__ = {}
    t0 = time()
    dt = time()
    sampling_rate = 0.5
    SAMPLE = True
    SAVE = False
    ReSTART = False

    lock = Lock() # Lock
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
        'calibrationCurve' : lambda x: x, # Calibration curve
    }

    Data = DataStorage

    # ------------------------------- Method -------------------------------- #
    def __init__(self, module, module_metadata = {}, meta_data={}, gui_configuration={}, data_processing={}, *args, **kwargs):
        """
        constructor
        """
        super(FellesBaseClass, self).__init__(*args, **kwargs)
        self.__refs__[self.__class__].append(ExtendedRef(self)) # Add instance to references
        self.__sfer__[hex(id(self))] =  ExtendedRef(self)
        self.ID = hex(id(self)) # ID used to look up objects (Will change for each run!)
        self.module = module # This is the reference to the Adam module

        self.MetaData = { k : v for k,v in self.FellesMetaData.iteritems()}
        for k,v in self.FellesMetaData.iteritems():
            if meta_data.has_key(k):
                self.MetaData[k] = meta_data[k]

        for k,v in self.module.GetMetaData().iteritems():
            if module_metadata.has_key(k):
                self.MetaData[k] = module_metadata[k]
            else:
                self.MetaData[k] = v

        self.plot_config = {k:v for k,v in self.GuiMetaData.iteritems()}
        for k,v in self.GuiMetaData.iteritems():
            if gui_configuration.has_key(k):
                self.plot_config[k] = gui_configuration[k]

        self.data_config = {k:v for k,v in self.DataProcessing.iteritems()}
        for k,v in self.GuiMetaData.iteritems():
            if data_processing.has_key(k):
                self.plot_config[k] = data_processing[k]

        self.data = self.Data(self) # Dict object reading and writing data, capable of reporting to onClose

        
        self.start() # target -> sample source -> self

    # ------------------------------- Method -------------------------------- #
    def run(self):
        """
        Instance method executed by "self.start()". 

        This method performs the sampling
        """
#        while FellesBaseClass.STATUS == IDLE:
#            self.data.Update(FellesBaseClass.Timer(), self.Sample())

        while FellesBaseClass.SAMPLE:
            # Attempt to aquire lock on the module
            while not FellesBaseClass.lock.acquire():
                pass
            try:
                s = self.GetMeassurements()
                t = FellesBaseClass.Timer()
                self.data.Update(t, s) # Sample Module
            except:
                print "'%s' instance: '%s'; Failed to read meassurement at time %.2f " %(self.__class__.__name__, self.GetMetaData('label'), FellesBaseClass.Timer())
                pass # In the event that the sampling fails, the thread will not fail
            finally:
                FellesBaseClass.lock.release()

            sleep(self.GetMetaData('sample_speed'))

        # TODO: Implement method allowing "restart" aka. pause...
        if FellesBaseClass.ReSTART:
            print "Trying again"
            FellesBaseClass.Start()
            self.run()
        else:
            pass

        print "Stopping Thread: '%s' in instance: '%s', base class: '%s'" %(
                                               self.GetMetaData('label'),
                                               self.__class__.__name__,
                                  self.__class__.__bases__[0].__name__,
                                  )

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        """
        Instance "magic method" returning the object instance itself
        """
        return self

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Timer(cls):
        """
        Class method returning a timestamp
        """
        return time() - cls.t0


    # ------------------------------- Method -------------------------------- #
    @classmethod
    def StartSampling(cls):
        """
        Class method starting the Execution of the "static method" Exec by 
        setting "START" to "True"
        
        Moreover, it sets the time stamp for the initial time when all sensors
        started sampling
        """
        cls.t0 = time()
        cls.SAVE = True

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def PauseThreads(cls):
        """
        Class method starting the Execution of the "static method" Exec by 
        setting "START" to "True"
        
        Moreover, it sets the time stamp for the initial time when all sensors
        started sampling
        """

        cls.t0 = time()
        cls.SAMPLE = False


    # ------------------------------- Method -------------------------------- #
    @classmethod
    def StopSampling(cls):
        """
        Class method starting the Execution of the "static method" Exec by 
        setting "START" to "True"
        
        Moreover, it sets the time stamp for the initial time when all sensors
        started sampling
        """
        cls.SAVE = False
        cls.SAMPLE = False
        cls.Data.Save()

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def FindInstance(cls, ID):
        """
        Class method locating a sensor from "__refs__" using a unique string ID
        which was created on object instantiation.

        The method returns an instance of the object whose ID matches the input. 
        """
        for refID in cls.__sfer__.iterkeys():
            if refID == ID:
                return cls.__sfer__[refID]()
    
    # ------------------------------- Method -------------------------------- #
    def GetMetaData(self, key=None):
        """
        """
        return self.MetaData if not key else self.MetaData[key]
    
    # ------------------------------- Method -------------------------------- #
    def GetPlotConfig(self, key=None):
        """
        """
        return self.PlotConfig if not key else self.PlotConfig[key]

    # ------------------------------- Method -------------------------------- #
    def GetDataProcessing(self, key=None):
        """
        """
        return self.DataProcessing if not key else self.DataProcessing[key]

    # ------------------------------- Method -------------------------------- #
    def SetPlotConfig(self, key, val):
        """
        """
        self.plot_config[key] = val

    # ------------------------------- Method -------------------------------- #
    def SetDataProcessing(self, key, fnc):
        """
        """
        self.data_config[key] = fnc

    # ------------------------------- Method -------------------------------- #
    def SetMetaData(self, key, val):
        """
        """
        self.MetaData[key] = val

    # ------------------------------- Method -------------------------------- #
    def UpdateSampleSpeed(self, speed):
        """
        Method updating the sample_speed
        """
        print "Updating '%s' sampling speed from '%s to '%s'"\
             %( self.GetMetaData('label'),\
                self.GetMetaData('sample_speed'),\
                speed )

        self.SetMetaData('sample_speed', speed)

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        """        
        """
        NotImplementedError("Method is overwritten by child")



