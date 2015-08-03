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

import wx
from wx.lib.pubsub import pub

from GUI import FellesFrame, FellesButton, FellesTextInput, FellesLabel
from FellesBase import FellesBaseClass
from SupportClasses import ExtendedRef

# ================================ Class ==================================== #
class Equipment(FellesBaseClass):
    """
    Syntactic sugar... 
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Equipment, self).__init__(*args, **kwargs)
        

    # ------------------------------- Method -------------------------------- #
    def InitGUI(self):
        """
        Method creating GUI
        """
        pass 

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
    ___pumps___ = []
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Pump, self).__init__(*args, **kwargs)
        self.___pumps___.append(ExtendedRef(self))

        self.Initialise()

    # ------------------------------- Method -------------------------------- #
    def TurnOn(self, caller=None, event=None):
        pass
        # self.module.set_motormode(1)

    # ------------------------------- Method -------------------------------- #
    def TurnOff(self, caller=None, event=None):
        pass
        # self.module.set_motormode(0)

    # ------------------------------- Method -------------------------------- #
    def Initialise(self, event=None, caller=None):
        """
        Procedure for initialising the pump.
        
        * Start
        * Set velocity to zero
        """
        self.TurnOn()

        # If setpoint velocity is not zero, set it to zero
        if self.GetSetpoint():
            self.SetSetpoint(0)

        self.meta['initial'] = 0

    # ------------------------------- Method -------------------------------- #
    def ShutDown(self, event=None, caller=None):
        """
        Procedure to shut down the pump
        
        * Set velocity to zero
        * Wait...
        * Stop
        """
        # If setpoint velocity is not zero, set it to zero
        if self.GetSetpoint():
            self.SetSetpoint(0)
        
        print "waiting for pump velocity to decreace before shutting down..."
        while self.GetSpeed():
            pass
        
        # Turn off pump
        self.TurnOff()
        
    # ------------------------------- Method -------------------------------- #
    def GetSetpoint(self):
        """
        Read pump setpoint
        """
        return 0
        #return self.module.get_setvelocity()

    # ------------------------------- Method -------------------------------- #
    def SetSetpoint(self, speed_rpm):
        """
        Set new pump setpoint
        """
        #self.module.set_velocity(speed_rpm)
        print "Pump speed setpoint changed to %.2f" %speed_rpm

    # ------------------------------- Method -------------------------------- #
    def GetSpeed(self):
        """
        Read the actual pump speed
        """
        return 0
        #self.module.get_actualvelocity()

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

    # ------------------------------- Method -------------------------------- #
    def InitGUI(self):
        """
        Method creating GUI
        """
        pass 
        PumpGUI = {}
        for s in self.___pumps___:
            if not PumpGUI.has_key(s().__class__.__name__):
                print "Creating GUI for Equipment: '%s'" %s().__class__.__name__
                PumpGUI[s().__class__.__name__] = [PumpFrame( pump = s() )]
            else:
                PumpGUI[s().__class__.__name__].append(PumpFrame(pump = s() ))

        return PumpGUI

# =============================== Class ====================================== #
class PumpFrame(FellesFrame):
    """
    @summary: Parent class frame for a pump. 

                            +-------------------------+
                            |          Pump           |
                            |       Speed      Meta   |
                            |  Setpt. 100 ^   T 298 K |
                            |  Mesrd  0.2   Acc 100 ..|
                            +-------------------------+

    """

    # ------------------------------- Method --------------------------------- #
    def __init__(self, pump, parent=None, debug=False, *args, **kwargs):
        """
        TODO: create debug mode.

        Constructor method

        args:
            title (str): REQUIRED
        """
        self.Pump = pump
        
        super(PumpFrame, self).__init__( title=pump.meta['label'])
        # Dictionary keeping track of which sensors to plot
#        self.plot_config = { s().ID : s().plot_config for s in self.sensors}

        self.InitUI() # Create frame
        self.Show()   # Show frame

#        self.plot = FellesPlot(parent=self, sensors = self.sensors) # Initiate Plot
#        self.plot.Show() # Show frame

        self.timer.start()

    def InitUI(self):

        # adding panel for cross-platform appearance 
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.obj = {}
        # adding sizers
        top_sizer       = wx.BoxSizer(wx.VERTICAL)
        title_sizer     = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer      = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=5)
        input_sizer     = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer    = wx.BoxSizer(wx.HORIZONTAL)

        self.lables = {}

        # adding GUI widgets
        self.label_name = wx.StaticText(self.panel, label=self.GetName())
        self.lables['label_setpoint'] = FellesLabel(self.panel, label='Speed setpoint [rpm]')
        self.lables['spin_setpoint'] = FellesTextInput(self.panel, source= self, target=self.SetSetpoint)

        self.lables['label_description_speed'] = FellesLabel(self.panel, label='Speed [{unit}]'.format(unit=self.Pump.meta['label']))
        self.lables['label_speed'] = FellesLabel(self.panel, label='{val} {unit}'.format(val=self.Pump.meta['initial'], unit=self.Pump.meta['unit']))
        
        # Buttons
        self.On  = FellesButton(self.panel, source=self, target=self.TurnOn, label='On' )
        self.Off = FellesButton(self.panel, source=self, target=self.TurnOff, label='Off')

        # arranging and sizing the widgets
        # alignment of title
        title_sizer.Add(self.label_name, 0, wx.ALL, 5)

        # arrangement of the pump setpoint and pump speed
        grid_sizer.Add(self.lables['label_setpoint'], 0, wx.ALL, 5)
        grid_sizer.Add(self.lables['spin_setpoint'], 0, wx.ALL, 5)
        grid_sizer.Add(self.lables['label_description_speed'], 0, wx.ALL, 5)
        grid_sizer.Add(self.lables['label_speed'], 0, wx.ALL, 5)

        # arrangement of the on/off buttons
        button_sizer.Add(self.On, 0, wx.ALL, 5)
        button_sizer.Add(self.Off, 0, wx.ALL, 5)

        # overall arrangement of the panel
        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(grid_sizer, 0, wx.ALL|wx.CENTER, 5)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(button_sizer, 0, wx.ALL|wx.CENTER, 5)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        self.top_sizer = top_sizer
        self.top_sizer.Fit(self)

        # setting initial status of on/off buttons
        self.Off()

    # ------------------------------- Method --------------------------------- #
    def TurnOn(self, event):
        """
        Convenience methods; acts as a buffer receiving button calls and
        sending the result to the Pump class instead of directly coupling the
        button to the Equipment.
        
        This is an advantage because it allows for separation between GUI and
        the underlying framework.
        """
        self.On.Disable()
        self.Off.Enable()

        self.Pump.Initialise()

    # ------------------------------- Method --------------------------------- #
    def TurnOff(self, event):
        self.Off.Disable()
        self.On.Enable()

        self.Pump.ShutDown()

    # ------------------------------- Method --------------------------------- #
    def SetSetpoint(self, event, caller):
        self.Pump.SetSetpoint(event.GetValue())

    # ------------------------------- Method --------------------------------- #
    def GetSetpoint(self):
        return self.Pump.GetSetpoint()

    # ------------------------------- Method --------------------------------- #
    def GetSpeed(self):
        return self.Pump.GetSpeed()
 
    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, sender=None, args=None):
        """
        Method for updating GUI
        """
        # Update label for sensor: s().meta['label']
        # with the most recent measurement: s().data.history['data'][-1]
#        self.lables['label_setpoint']
        self.lables['spin_setpoint'].SetLabel( '%.2f %s' %(self.GetSetpoint(), str(self.Pump.meta['unit'])) )
#        self.lables['label_description_speed']
        self.lables['label_speed'].SetLabel( '%.2f %s' %( self.Pump.data.history['data'][-1], str(self.Pump.meta['unit'])) )

#        pub.sendMessage( 'Plot.%s' %self.GetLabel() )
        self.top_sizer.Layout()

    # ------------------------------- Method --------------------------------- #
    def OnClose(self, event):
        """
        Method stopping the sampling threads for **all** sensors in the Window
        before closing the plot and text panel.

        args:
          event : instance, call the method using: <OBJ>.onClose(self)

        """
        self.timer.sample = False
        while self.timer.isAlive():
            pass

        self.Off()
        pub.sendMessage( 'Close.%s' %self.GetLabel(), event=self )

        print "Window: '%s', closed by event: '%s'" %( self.GetLabel(), event.__class__.__name__ )
        self.Destroy()
