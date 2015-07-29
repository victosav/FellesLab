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

import wx
import wxmplot
import numpy as np
from math import floor, ceil

from FellesLab.Equipment import Sensor #, sensorTypes

# ............................... Function .................................. #
def findSensor(id):
    """
    Find a sensor based on "id"

    TODO: implement
    """
    for s in Sensor.___refs___:
        if s().ID == id:
            return s

# =============================== Class ====================================== #
class FellesPlot(wx.Frame):
    """
    Rudimentary class creating a plot frame that is updated dynamically.
    The class takes one argument "parent".
    
     'Unit' .-------------------.
            |          ____     |
            |         /    |    |
            |        /      \/  |
            |__/\   /           |
            |    \_/            |
            |                   |
            .-------------------.
                    Time
    
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor
        """
        super(FellesPlot, self).__init__(parent)

        self.candidates = kwargs['sensors'] # List of all sensors
        self.parentFrame = parent # Parent SensorFrame (from SensorGUI.py)
        wx.EVT_CLOSE(self, self.onClose)

        # setting up plot
        self.plot_panel = wxmplot.PlotPanel(parent=self, size=(500, 350), dpi=100)

        # adding sizer
        self.panel_sizer = wx.BoxSizer()
        self.panel_sizer.Add(self.plot_panel)

        # assigning the sizer to the panel
        self.SetSizer(self.panel_sizer)

        # plotIDs keeps track over which sensor to plot.
        #      ID            bool  ,       ID          bool
        # {'0x7f921e6977a0': False , '0x7f921e696530': True }
        # (The ID is the address in memory of the sensor object)
        self.plotIDs = { c().ID : c().plot_config['plot'] for c in self.candidates }

        # fit the sizer to the panel
        self.Fit()

    # ------------------------------- Method -------------------------------- #
    def UpdatePlot(self):
        """
        Method for updating the plot frame.
        
        The sensors in "self.plotIDs" that are not "True" will not be plotted.
        """

        for id, plt in self.plotIDs.iteritems():
            if plt:
                self.plot_panel.oplot(
                                findSensor(id)().data.history['time'],
                                findSensor(id)().data.history['data'],
                                side ='left',
                                label = findSensor(id)().meta['label'],
                                color = findSensor(id)().plot_config['color'],
#                               show_legend=True,
                                marker = 'None',
                                drawstyle='line',
                                style = 'solid',
                                grid=True,
                                )

        self.plot_panel.set_xylims(\
          [\
           floor( min( [ min( findSensor(id)().data.history['time'] )\
                         for id,plt in self.plotIDs.iteritems() if plt ] ) ),\
           ceil( max( [ max( findSensor(id)().data.history['time'] )\
                         for id,plt in self.plotIDs.iteritems() if plt ] ) ),\
           floor( min( [ min( findSensor(id)().data.history['data'] )\
                         for id,plt in self.plotIDs.iteritems() if plt ] ) ),\
           ceil( max( [ max( findSensor(id)().data.history['data'] )\
                          for id,plt in self.plotIDs.iteritems() if plt ] ) )\
          ]\
        )

        self.panel_sizer.Fit(self)

    # ------------------------------- Method --------------------------------- #
    def onClose(self, event):
        """
        
        """

        print "Plot %s closed by event: '%s'" %( self.parentFrame.GetName() ,\
                                                 event.__class__.__name__)
        self.Destroy()
