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
#
from GUI import FellesFrame, FellesButton, FellesTextInput, FellesLabel
#
from FellesLab.Equipment import Sensor#, sensorTypes
from PlotGUI import FellesPlot
#
#from FellesLab.Utils.SupportFunctions import sensorTypes
from FellesLab.Utils.DataStorage import *
from FellesLab.Utils.SupportClasses import *

from random import random


# ............................... Function .................................. #
def sensorTypes():
    """
    Temperature: list( <weakref at ; to obj.instances>] )
    Volume: list( <weakref at ; to obj.instances> )
    """

    types = {}
    for s in Sensor.___refs___:
        if not types.has_key(s().__class__.__name__):
            types[s().__class__.__name__] = [s]
        else:
            types[s().__class__.__name__].append(s)
    return types

# =============================== Class ====================================== #
def findSensors(ID):
    """
    ID list. sensor.ID
    """
    return [s for s in Sensor.___refs___ if s().ID in ID]
    
# =============================== Class ====================================== #
class SensorFrame(FellesFrame):
    """
    @summary: Parent class frame for sensors. Each sensor **type**, e.g. 
              Temperature, will have ONE sensor frame keeping track of the 
              output from **all** the sensors.

                                    +--------------+
                                    |  Temperature |
                                    |              |
                                    |  T1   298 K  |
                                    |  T2    25 C  |
                                    .  :     :  :  .
                                    .  :     :  :  .
                                    +--------------+

              The class **must** be initiated **after** **all** sensors have
              been defined. The reason is that the constructor will locate all
              sensort
    """
    
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent=None, debug=False, *args, **kwargs):
        """
        TODO: create debug mode.
        
        Constructor method
        
        args:
            title (str): REQUIRED
        """
        super(SensorFrame, self).__init__( *args, **kwargs)
        
        wx.EVT_CLOSE(self, self.StopSamplers)

        self.sensors = sensorTypes()[self.GetLabel()]
        
        # Dictionary keeping track of which sensors to plot
        self.plot_config = { s().ID : s().plot_config for s in self.sensors}


        self.gLabel = dict() # Labels, i.e. Sensor 1, 2, ...
        self.gValue = dict() # Values, i.e. measurements ...

        self.InitUI() # Create frame
        self.Show()   # Show frame

        self.plot = self.Plot() # Initiate Plot
        self.plot.Show() # Show frame

        self.timer.start()
    # ------------------------------- Method --------------------------------- #
    def InitUI(self):
        self.panel = wx.Panel(self, wx.ID_ANY)

#         closeBtn = wx.Button(self.panel, label="Close")
#         closeBtn.Bind(wx.EVT_BUTTON, self.onClose)


        # adding sizers
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(rows=len(self.sensors)+1, cols=2, hgap=5, vgap=5)
        
        # NOTE: s() executes the __call__ method in the ExtendedRef class,
        #       which in turn executes the __call__ method in the Sensor class.
        #       Finally, the Sensor returns itself.
        #
        #       This means that s().meta['label'] is simply a way of looking up the
        #       'label' key of a Sensor.         
        self.gLabel = { s().meta['label']: wx.StaticText(self, label=s().meta['label']) for s in self.sensors }
        self.gValue = { s().meta['label']: wx.StaticText(self, label=str(s().data.val)) for s in self.sensors }

        for s in self.sensors:
            grid_sizer.Add( self.gLabel[s().meta['label']] , 0, wx.ALL, 5 )
            grid_sizer.Add( self.gValue[s().meta['label']] , 0, wx.ALL, 5 )

        # arranging and sizing the widgets
        # alignment of title
        title_sizer.Add(wx.StaticText(self, label=self.GetTitle()), 0, wx.ALL, 5)

        # overall arrangement of the panel
        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(grid_sizer, 0, wx.ALL|wx.CENTER, 5)

        self.panel.SetSizerAndFit(top_sizer)
        top_sizer.Fit(self)
        self.top_sizer = top_sizer
        
        

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, sender=None, args=None):
        """
        Method for updating GUI
        """
        for s in self.sensors:
            self.gValue[s().meta['label']].SetLabel('%.2f %s'%(s().data.val, str(s().meta['unit'])))
        self.top_sizer.Fit(self)
        self.plot.UpdatePlot()

    def Dummy(self, *args, **kwargs):
        pass

    # ------------------------------- Method --------------------------------- #
    def StopSamplers(self, event):
        """
        Method stopping sampler threads AND GUI update thread.
        """
        for s in self.sensors:
            s().SAMPLE = False

        self.timer.target = self.Dummy
        self.SAMPLE = False

        self.onClose(self)
        
    # ------------------------------- Method --------------------------------- #
    def Plot(self):
        """
        
        """
        return FellesPlot( parent=self, sensors = self.sensors )
    # ------------------------------- Method --------------------------------- #
    def onClose(self, event):
        """"""
        print "closing"

        self.plot.onClose(self)
        self.Destroy()
