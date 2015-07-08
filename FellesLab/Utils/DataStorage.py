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


# Instatiate data objects
SensorMetaData = MetaData()
SensorRealTimeData = RealTimeData()

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
    # ------------------------------- Method -------------------------------- #
    def __init__(self, file_path='%s/Desktop/'%(os.path.expanduser("~")), store_length=40, remove_length=10):
        self.store_length = store_length
        self.remove_length = remove_length
        self.data_writer = WriteDataToFile('%s/Desktop/'%(os.path.expanduser("~")), timeStamp() )

    # ------------------------------- Method -------------------------------- #
    def add_data(self, new_data):
        try:
            for key in new_data:
                self.data[key].extend(new_data[key])
        except AttributeError:
            self.data = dict()
            for key in new_data:
                self.data[key] = MyList()
            self.data_writer.write_header(self.data)
            self.add_data(new_data)

        # writing older data to file
        if self.data[self.data.keys()[0]].length > self.store_length:
            self.data_writer.write_data(self.remove_data(self.remove_length))
    
    # ------------------------------- Method -------------------------------- #
    def get_data(self):
        return self.data
    
    # ------------------------------- Method -------------------------------- #
    def remove_data(self, remove_length):
        data_temp = dict()
        for key in self.data:
            data_temp[key] = self.data[key].longpop(length=remove_length)
        return data_temp
    
    # ------------------------------- Method -------------------------------- #
    def write_and_delete_data(self): 
    # intended for storing the rest of the data after closing the application
        print('removing and writing all data')
        self.data_writer.write_data(self.remove_data(self.data[self.data.keys()[0]].length))

# =============================== Class ===================================== #
class WriteDataToFile:
    """
    
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, path_to_save_file, name_of_save_file):
        ''' Create a save object '''
        self.path_to_save_file = path_to_save_file
        self.name_of_save_file = name_of_save_file
    
    # ------------------------------- Method -------------------------------- #
    def write_header(self, data):
        os.chdir(self.path_to_save_file)
        openfile = open(self.name_of_save_file,'a')
        
        header_string = ', '.join(data.keys())
        
        openfile.write(str(header_string))
        openfile.write('\n')
        openfile.close()
    
    # ------------------------------- Method -------------------------------- #
    def write_data(self, data):
        ''' When called it will write the data (dict) to the file'''
        os.chdir(self.path_to_save_file)
        openfile = open(self.name_of_save_file,'a')

        tmp_list = list()

        for key in data:
            tmp_list.append((data[key]))
            
        tmp_list = zip(*tmp_list)
        
        
        for list_element in tmp_list:
            list_element = ', '.join(map(str, list_element)) #Separe data by commas
            openfile.write(str(list_element))
            openfile.write('\n')
        openfile.close()
