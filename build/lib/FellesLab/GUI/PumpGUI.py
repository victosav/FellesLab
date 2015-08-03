# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Felles lab GUI graphics parent classes
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

import wx
from wx.lib.pubsub import pub

from GUI import FellesFrame, FellesButton, FellesTextInput, FellesLabel
from PlotGUI import FellesPlot

from FellesLab.Equipment import Sensor, Pump
from FellesLab.Utils import sensorTypes, DataStorage
from FellesLab.Equipment import Sensor 
from random import random


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
    def __init__(self, parent=None, debug=False, *args, **kwargs):
        """
        TODO: create debug mode.

        Constructor method

        args:
            title (str): REQUIRED
        """
        super(PumpFrame, self).__init__( *args, **kwargs)

        self.sensors = sensorTypes(Pump)[self.GetLabel()]

        # Dictionary keeping track of which sensors to plot
#        self.plot_config = { s().ID : s().plot_config for s in self.sensors}

        self.InitUI() # Create frame
        self.Show()   # Show frame

#        self.plot = FellesPlot(parent=self, sensors = self.sensors) # Initiate Plot
#        self.plot.Show() # Show frame

        self.timer.start()


    def InitUI(self):

        # adding panel for cross-platform appearance 
        self.panel = Panel(self, wx.ID_ANY)

        # adding sizers
        top_sizer       = wx.BoxSizer(wx.VERTICAL)
        title_sizer     = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer      = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=5)
        input_sizer     = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer    = wx.BoxSizer(wx.HORIZONTAL)
        
        # adding GUI widgets
        self.label_name = wx.StaticText(self.panel, label=self.GetName())
        self.obj['label_setpoint'] = FellesLabel(self.panel, label='Speed setpoint [rpm]')
        self.obj['spin_setpoint'] = FellesTextInput(self.panel, source= self, target=self.obj.SetpointChange)

        self.obj['label_description_speed'] = FellesLabel(self.panel, label='Speed [{unit}]'.format(unit=self.obj['unit']))
        self.obj['label_speed'] = FellesLabel(self.panel, label='{val} {unit}'.format(val=self.obj['initial'], unit=self.obj['unit']))
        
        # Buttons
        self.on  = FellesButton(self.panel, source=self, target=self.obj.ON , label='On' )
        self.off = FellesButton(self.panel, source=self, target=self.obj.OFF, label='Off')

        # arranging and sizing the widgets 
        # alignment of title
        title_sizer.Add(self.label_name, 0, wx.ALL, 5)

        # arrangement of the pump setpoint and pump speed 
        grid_sizer.Add(self.obj['label_setpoint'], 0, wx.ALL, 5)
        grid_sizer.Add(self.obj['spin_setpoint'], 0, wx.ALL, 5)
        grid_sizer.Add(self.obj['label_description_speed'], 0, wx.ALL, 5)
        grid_sizer.Add(self.obj['label_speed'], 0, wx.ALL, 5)

        # arrangement of the on/off buttons
        button_sizer.Add(self.on, 0, wx.ALL, 5)
        button_sizer.Add(self.off, 0, wx.ALL, 5)

        # overall arrangement of the panel
        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(grid_sizer, 0, wx.ALL|wx.CENTER, 5)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(button_sizer, 0, wx.ALL|wx.CENTER, 5)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        top_sizer.Fit(self)

        # setting initial status of on/off buttons
        self.off()
    
    # Pump operations
    def turn_on_pump(self, pump_name):
        self.pump[pump_name].set_motormode(1)
        pub.sendMessage('pump_status_changed', pump_name=pump_name, pump_status='on')

    def turn_off_pump(self, pump_name):
        self.pump[pump_name].set_motormode(0)
        pub.sendMessage('pump_status_changed', pump_name=pump_name, pump_status='off')

    def set_pump_speed_setpoint(self, pump_name, speed_rpm):
        self.pump[pump_name].set_velocity(speed_rpm)
        pub.sendMessage('pump_setpoint_changed', pump_name=pump_name, setpoint_speed=speed_rpm)

    def get_pump_speed_setpoint(self, pump_name):
        return self.pump[pump_name].get_setvelocity()

    def get_pump_speed(self, pump_name):
        return self.pump[pump_name].get_actualvelocity()
 