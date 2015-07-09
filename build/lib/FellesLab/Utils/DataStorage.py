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

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

import os
import collections

from time import localtime
from calendar import weekday

global SensorMetaData, SensorRealTimeData
    
class MinMaxVal(object):
    min = float
    max = float
    val = float
    
# =============================== Class ===================================== #
class RealTimeData(object):
    """
    
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        self.dict = dict(**kwargs)
        self.history = dict()
        # self()

    # ------------------------------- Method -------------------------------- #
    def __call__(self, keys):
        """
        Call method retrieves list history for plotting.
        
        args:
          * keys list(str): keys for the measurements that should be plotted
        """
        return {key: self.history[key] for key in keys}

    # ------------------------------- Method -------------------------------- #
    def __setitem__(self, obj):
        """
        
        """
        DataStorage.obj[key] = self[key]
        self.dict.update({key : val})

        if not self.history.has_key(key):
            self.history.update({key : collections.deque()} )
        self.history[key].append(val)
        
        return None

    # ------------------------------- Method -------------------------------- #
    def __getitem__(self, key):
        """
        
        """
        return self.dict[key]



# =============================== Class ===================================== #
class MetaData(dict):
    """
    
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(MetaData, self).__init__(kwargs)

# ............................... Function .................................. #
def timeStamp():
    """
    Function creating a timestamp in the format:
                        Wed_Jun_17_hourminsec_year
    """
    LT = localtime() # Timestamp information for filename
    Day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    Mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return '{D}_{M}_{d}_{h}{m}{s}_{Y}'.format(\
               D= Day[weekday(LT[0],LT[1],LT[2])], M= Mon[LT[1]-1], d= LT[2],\
               h= LT[3], m= LT[4], s= LT[5], Y= LT[0] )

# =============================== Class ===================================== #
class MyList(list):
    def longpop(self, start=0, length=1):
        slice = self[start:start+length]
        del self[start:start+length]
        return slice

    @property
    def length(self):
        return len(self)

# =============================== Class ===================================== #
class DataStorage(object):
    """
    This should be a clever data storage container.
    
    * Receive data from "real time data object".
    * Write data to file.
    * Provide historical data to plotter.
    
    """
    file_path = '%s/Desktop/'%(os.path.expanduser("~"))
    
    # ------------------------------- Method -------------------------------- #
    def __init__(self, owner):
        """
        args:
          owner (instance): Parent object to which the DataStorage instance belongs
        """
        
        self.owner = owner

        # Create a vector holding historical data for the purpose of plotting.
        # The length may vary because the sampling speed of the units are 
        # different. Moreover
        history_length = int(round(owner.plot_config['time_span']/owner.meta['sample_speed']))
        self.history = {'time': collections.deque( [], history_length ),\
                        'data': collections.deque( [], history_length )
                        }
        del history_length

#        self.writer = WriteData( self )
    
    def Update(self, time, val):
        self.history['data'].append(val)
        self.history['time'].append(time)

        self.val = val

#        self.writer.Write('self')

        return None


# =============================== Class ===================================== #
class WriteData:
    """
    
    """
    SAVE_PATH = '%s/Desktop/'%(os.path.expanduser("~"))
    SAVE_NAME = timeStamp()
    # ------------------------------- Method -------------------------------- #
    def __init__(self, parent, save_path=None, save_name=None):
        ''' Create a save object '''

        self.parent = parent

        if not save_path:
            self.savePath = self.SAVE_PATH
        else:
            self.savePath = save_path
            
        if not save_name:
            self.saveName = self.SAVE_NAME
        else:
            self.saveName = save_name

        with open(self.savePath + self.saveName,'a') as self.f:
            self.f.write( 'time' + ',' + self.parent.__class__.__name__)
            while parent.owner.SAMPLING:
                pass
            self.f.close()

    def Writer(self, parent=None):
        if parent:
            self.f.write( str(self.parent.history['time'][-1]) + ',' + str( parent.history['data'][-1]) ) 