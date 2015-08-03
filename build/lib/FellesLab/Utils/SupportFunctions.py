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
__date__ = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

from time import localtime
from calendar import weekday

# ............................... Function .................................. #
def dayStamp():
    """
    Function returning a timestamp (string) in the format:
                        Wed_Jun_17_hourminsec_year
    """
    LT = localtime() # Timestamp information for filename
    Day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    Mon = ['Jan','Feb','Mar','Apr','May','Jun',\
           'Jul','Aug','Sep','Oct','Nov','Dec']
    return '{D}_{Num}_{M}_{Y}'.format(\
               D= Day[weekday(LT[0],LT[1],LT[2])], M= Mon[LT[1]-1], Num= LT[2],\
               Y= LT[0] )

# ............................... Function .................................. #
def timeStamp():
    """
    Function returning a timestamp (string) in the format:
                        Wed_Jun_17_hourminsec_year
    """
    LT = localtime() # Timestamp information for filename
    Day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    Mon = ['Jan','Feb','Mar','Apr','May','Jun',\
           'Jul','Aug','Sep','Oct','Nov','Dec']
    return '{D}_{M}_{d}_{h}{m}{s}_{Y}'.format(\
               D= Day[weekday(LT[0],LT[1],LT[2])], M= Mon[LT[1]-1], d= LT[2],\
               h= LT[3], m= LT[4], s= LT[5], Y= LT[0] )

# ............................... Function .................................. #
def findSensor(Sensor, id):
    """
    Find a sensor based on "id", the id is an address in memory for the sensor
    object.
    """
    for sensor in Sensor.___refs___:
        if sensor().ID == id:
            return sensor

# ............................... Function .................................. #
def sensorTypes(cls):
    """
    Temperature: list( <weakref at ; to obj.instances>] )
    Volume: list( <weakref at ; to obj.instances> )
    """

    types = {}
    for s in cls.___refs___:
        if not types.has_key(s().__class__.__name__):
            types[s().__class__.__name__] = [s]
        else:
            types[s().__class__.__name__].append(s)
    return types









