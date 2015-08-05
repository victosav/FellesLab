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

import os
import collections
import weakref
import wx
from calendar import weekday
from time import sleep, time, localtime
from threading import Thread
from SupportFunctions import timeStamp
from tempfile import TemporaryFile, mkdtemp


# ================================ Class ==================================== #
class FellesSampler(Thread):
    """
    Thread class.
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, group=None, target=None, source=None):
        """
        args:
            target (callable): Method to execute
            source (instance): Object to which the thread belongs
        """
        self.target = target
        self.source = source

        super(FellesSampler, self).__init__()

        # Create a vector holding historical data for the purpose of plotting.
        # The length may vary because the sampling speed of the units are
        # different. Moreover
        history_length = int( round(self.source.plot_config['time_span']/ \
                                    self.source.GetMetaData('sample_speed')) )
        self.history = {'time': collections.deque( [], history_length ),\
                        'data': collections.deque( [], history_length )
                        }
        del history_length

    # ------------------------------- Method -------------------------------- #
    def Update(self, time, val):
        self.val = self.source.data_config['calibrationCurve'](val)
        self.history['data'].append(self.val)
        self.history['time'].append(time)

        return None

    # ------------------------------- Method -------------------------------- #
    def run(self):
        """
        Method started when "instance.start()" is called

        The thread will call "source.target()" at a rate determined by "sample
        rate" in the caller.

        "source.target" is the method that reads a sample
        from the device
        """

        while self.source.SAMPLING:
            self.target()
            sleep(self.source.GetMetaData('sample_speed'))

        self.Terminate()

    # ------------------------------- Method -------------------------------- #
    def Terminate(self):
        """

        """
        print "Stopping Thread: '%s' in instance: '%s', base class: '%s'" %(
                                               self.source.GetMetaData('label'),
                                               self.source.__class__.__name__,
                                  self.source.__class__.__bases__[0].__name__,
                                  )


# ================================ Class ==================================== #
class GuiUpdater(Thread):
    """
    Sugar class
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, source, target, *args, **kwargs):
        self.target = target
        self.source = source
        self.sample = self.source.SAMPLING
        super(GuiUpdater, self).__init__(None)

    # ------------------------------- Method -------------------------------- #
    def run(self):
        """
        Method started when "instance.start()" is called

        The thread will call "source.target()" at a rate determined by "sample
        rate" in the caller.

        NOTE: It is necesary to call target trough wx.CallAfter on Linux.
         "wx.CallAfter(self.target, self)" is a synonym for "self.taget(self)"
        """

        while self.sample:
            wx.CallAfter(self.target, self)
            sleep(1)

        self.Terminate()

    # ------------------------------- Method -------------------------------- #
    def Terminate(self):
        """

        """
        print "Stopping GUI thread: '%s', instance: '%s', base class: '%s'" %(
                                                       self.source.GetLabel(),
                                               self.source.__class__.__name__,
                                  self.source.__class__.__bases__[0].__name__,
                                  )

        print "Stopping GUI thread: '%s'" %self.source.GetLabel()

# ================================ Class ==================================== #
class ExtendedRef(weakref.ref):
    """
    Weakreference class, creates an alias to "referee".

    This is an important class, the example in the __call__ method shows how
    to use it.
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, referee, callback=None):
        self.referee = referee
        super(ExtendedRef, self).__init__(referee, callback)

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        """
        Magic method.

        Returns the object that the class referes to. The practical
        implication is that it becomes possible to access the objects methods
        and variables through the reference class.

        Understand how to use this class through the following example:

        example.py
        ----------------------------------------------------------------------
        import weakref

        class ExtendedRef(weakref.ref):

            def __init__(self, referee, callback=None):
                self.referee = referee
                super(ExtendedRef, self).__init__(referee, callback)

            def __call__(self):
                return self.referee()

        class Referee:
            message = "References are clever"

            def __call__(self):
                return self

            def ChangeMessage(self, msg):
                self.message = msg

        a = Referee()
        b = ExtendedRef(a)

        print b().message
        b().ChangeMessage("A different message")
        print a.message
        ----------------------------------------------------------------------

        """
        return self.referee()

# =============================== Class ===================================== #
class DataStorage(object):
    """
    This should have been be a clever data storage container.
    """

    # List of object instances
    ___refs___ = []

    # ------------------------------- Method -------------------------------- #
    def __init__(self, owner):
        """
        args:
          owner (instance): Parent object to which the DataStorage instance belongs
        """
        self.___refs___.append(ExtendedRef(self)) # Add instance to references

        self.owner = owner # Object whose data will be saved

        self.File = TemporaryFile()
        self.File.write('time, %s %s\n' %(self.owner.GetMetaData('label'),self.owner.GetMetaData('unit')) )

        self.Resize()

    # ------------------------------- Method -------------------------------- #
    def Scale(self, val):
        return self.owner.data_config['calibrationCurve'](val)
    # ------------------------------- Method -------------------------------- #
    def Resize(self):
        """
        Resize the array needed to store

        Use this method if the sample rate is changed.
        """
        if ('time_span') not in self.owner.plot_config:
            self.owner.plot_config['time_span'] = 5 # seconds

        self.history_length = int( round( self.owner.plot_config['time_span']/self.owner.GetMetaData('sample_speed')))
        self.FreshStart()

    # ------------------------------- Method -------------------------------- #
    def FreshStart(self):
        """
        Use this method if you just need a fresh start
        """
        # Create a vector holding historical data for the purpose of plotting.
        # The length may vary because the sampling speed of different are
        # sensors may vary.

        self.history = {'time': collections.deque( [], self.history_length ),\
                        'data': collections.deque( [], self.history_length )
                       }

    # ------------------------------- Method -------------------------------- #
    def Restart(self, time, val):
        """
        """
        # Create a vector holding historical data for the purpose of plotting.
        # The length may vary because the sampling speed of different are
        # sensors may vary.

        self.history = {'time': collections.deque( [], self.history_length ),\
                        'data': collections.deque( [], self.history_length )
                       }
        self.Update(time, val)

    # ------------------------------- Method -------------------------------- #
    def Update(self, time, val):
        """
        Method updating the history
        """
        self.history['data'].append(self.Scale(val))
        self.history['time'].append(time)

        if self.owner.SAVE:
            self.File.write('%f , %f\n' %(time, self.history['data'][-1] ))

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        """

        """
        return self

