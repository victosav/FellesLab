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
 term = Terminal()
     |          with term.location(2, 5):
     |              print 'Hello, world!'
     |              for x in xrange(10):
     |                  print 'I can do it %i times!' % x
"""

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

import os
import collections

from FellesLab.Utils.SupportClasses import ExtendedRef
from FellesLab.Utils.SupportFunctions import timeStamp

from tempfile import TemporaryFile, mkdtemp

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

        #WriteOutData.FILES[owner.meta['label']] = TemporaryFile()
        self.File = TemporaryFile()#WriteOutData.FILES[owner.meta['label']]

        self.File.write('time, %s\n' %self.owner.meta['label'] )

        self.Resize()

    # ------------------------------- Method -------------------------------- #
    def Resize(self):
        """
        Resize the array needed to store
        """
        if ('time_span') not in self.owner.plot_config:
            self.owner.plot_config['time_span'] = 5 # seconds

        self.history_length = int( round( self.owner.plot_config['time_span']/self.owner.meta['sample_speed'] ) )
        self.Init()

    # ------------------------------- Method -------------------------------- #
    def Init(self):
        """
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
        self.history['data'].append(val)
        self.history['time'].append(time)

        if self.owner.SAVE:
            self.File.write('%f , %f\n' %(time, val))

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        """
        
        """
        return self
