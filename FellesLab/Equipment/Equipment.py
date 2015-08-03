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

# ================================ Class ==================================== #
class Equipment(FellesBaseClass):
    """
    Syntactic sugar... 
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Equipment, self).__init__(*args, **kwargs)

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        return '<%s.%s equipment at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.ID
        )

# ================================ Class ==================================== #
class Pump(Equipment):
    """
    
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Pump, self).__init__(*args, **kwargs)
        
        self.Initialise()

    # ------------------------------- Method -------------------------------- #
    def Initialise(self):
        """
        Procedure for initialising the pump.
        
        * Start
        * Set velocity to zero
        """
        self.module.set_motormode(1)

        # If setpoint velocity is not zero, set it to zero
        if self.module.get_setvelocity():
            self.module.set_velocity(0)

    # ------------------------------- Method -------------------------------- #
    def ShutDown(self):
        """
        Procedure to shut down the pump
        
        * Set velocity to zero
        * Wait...
        * Stop
        """
        # If setpoint velocity is not zero, set it to zero
        if self.module.get_setvelocity():
            self.module.set_velocity(0)
        
        print "waiting for pump velocity to decreace before shutting down..."
        while self.GetSpeed():
            pass
        
        # Turn off pump
        self.module.set_motormode(0)
    

    # ------------------------------- Method -------------------------------- #
    def GetSetpoint(self):
        """
        Read pump setpoint
        """
        return self.module.get_setvelocity()

    # ------------------------------- Method -------------------------------- #
    def SetSetpoint(self, speed_rpm):
        """
        Set new pump setpoint
        """
        self.module.set_velocity(speed_rpm)

    # ------------------------------- Method -------------------------------- #
    def GetSpeed(self):
        """
        Read the actual pump speed
        """
        self.module.get_actualvelocity()

    # ------------------------------- Method -------------------------------- #
    def GetTemperature(self):
        """
        Read pump temperature
        """
        pass
    
    # ------------------------------- Method -------------------------------- #
    def GetAcceleration(self):
        """
        Read pump acceleration
        """
        pass
