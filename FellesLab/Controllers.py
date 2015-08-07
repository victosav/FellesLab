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

from FellesBase import FellesBaseClass
from collections import defaultdict

# ================================ Class ==================================== #
class Controller(FellesBaseClass):
    """
    Syntactic sugar...
    """
    __controllers__ = defaultdict(list)
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__(*args, **kwargs)
        self.__controllers__[self.__class__].append(ExtendedRef(self)) # Add instance to references

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def InitGUI(cls):
        """
        Method creating sensor frames for the sensors

        GUI = {}
        for ControllerType,Instances in cls.Instances():
            print "Creating GUI for Sensor: '%s'" %ControllerType.__class__.__name__
            SensorGUI[ControllerType.__class__.__name__] = SensorFrame(
                                         sensors = Instances ,
                                         title = ControllerType.__class__.__name__ ,
                                         )

        return GUI

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Instances(cls):
        for ref in cls.__controllers__[cls]:
            inst = ref()
            if inst is not None:
                yield inst

    # ------------------------------- Method -------------------------------- #
    def GetMeassurements(self):
        return self.module.get_analog_in()

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        return '<%s.%s controller at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.ID
        )
