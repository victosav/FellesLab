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

import numpy as np
from math import floor, ceil
from collections import defaultdict

import wx
from wx.lib.pubsub import pub
import wxmplot

from SupportClasses import FellesSampler, ExtendedRef, DataStorage
from FellesBase import FellesBaseClass
from SupportFunctions import sensorTypes, findSensor
from GUI import FellesFrame, FellesButton, FellesTextInput, FellesLabel
from random import random
# ================================ Class ==================================== #
class Sensor(FellesBaseClass):
    """
    Syntactic sugar...
    """
    __sensors__ = defaultdict(list)
    # ------------------------------- Method -------------------------------- #
    def __init__(self,module, *args, **kwargs):
        
        self.module = module # This is the reference to the Adam module
        self.__sensors__[self.__class__].append(ExtendedRef(self)) # Add instance to references

        super(Sensor, self).__init__(*args, **kwargs)

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def InitGUI(cls):
        """
        Method creating sensor frames for the sensors
        """
        SensorGUI = {}
        for ref,instnts in cls.Instances():
            print "Creating GUI for Sensor: '%s'" %ref.__name__
            SensorGUI[instnts[0]().__class__.__name__] = SensorFrame(
                                         sensors = instnts ,
                                         title = ref.__name__ ,
                                         )
        return SensorGUI

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Instances(cls):
        """
        """
        for ref,lst in cls.__sensors__.iteritems():
            yield ref, lst

    # ------------------------------- Method -------------------------------- #
    def GetMeassurements(self):
        return self.module.get_analog_in(self.module.GetMetaData('channel'))

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        return '<%s.%s sensor at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.ID
        )

# ================================ Class ==================================== #
class Temperature(Sensor):
    """
    Syntactic sugar...
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Temperature, self).__init__(*args, **kwargs)


# ================================ Class ==================================== #
class Voltage(Sensor):
    """
        Syntactic sugar...
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Voltage, self).__init__(*args, **kwargs)



# =============================== Class ====================================== #
class SensorFrame(FellesFrame):
    """
    @summary: Parent class frame for sensors. Each sensor **type**, e.g.
              Temperature, will have ONE sensor frame keeping track of the
              output from **all** the sensors.

                            +-------------------------+
                            |       Temperature       |
                            | Lbl   Unit  Sample rate |
                            | T1   298 K    0.5 ^     |
                            | T2    25 C    0.5 ^     |
                            . :     :  :      :       .
                            +-------------------------+

              The class **must** be initiated **after** **all** sensors have
              been defined. The reason is that the constructor will locate all
              sensort
    """

    # ------------------------------- Method --------------------------------- #
    def __init__(self, sensors, parent=None, debug=False, *args, **kwargs):
        """
        TODO: create debug mode.

        Constructor method

        args:
            title (str): REQUIRED
        """
        super(SensorFrame, self).__init__( *args, **kwargs)

        self.sensors = sensors
        # Dictionary keeping track of which sensors to plot
        self.plot_config = { s().GetID() : s().plot_config for s in self.sensors}

        self.InitUI() # Create frame
        self.Show()   # Show frame

        self.plot = FellesPlot(parent=self) # Initiate Plot
        self.plot.Show() # Show frame
        self.plot_deleted = False
        self.timer.start()
    # ------------------------------- Method --------------------------------- #
    def InitUI(self):
        self.panel = wx.Panel(self, wx.ID_ANY)

        # adding sizers
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(rows=len(self.sensors)+2, cols=3, hgap=3, vgap=3)

        # NOTE: s() executes the __call__ method in the ExtendedRef class,
        #       which in turn executes the __call__ method in the Sensor class.
        #       Finally, the Sensor returns itself.
        #
        #  This means that s().GetMetaData('label') is simply a way of looking up the
        #  'label' key of a Sensor.
        for s in iter(self.sensors):
            try:
                iii = s().data.history['data'][-1]
                jjj = s().data.history['time'][-1]
            except:
                s().data.history['data'].append(random())
                s().data.history['time'].append(random())

        self.gLabel = {\
                      s().GetID():FellesLabel(
                                               self.panel, wx.ID_ANY,\
                                                label=s().GetMetaData('label'),\
                                                        style=wx.ALIGN_CENTER )\
                                                          for s in iter(self.sensors)\
                      }
        self.gValue = {\
                      s().GetID():FellesLabel(
                                      self.panel, wx.ID_ANY,\
                                       label=str(s().data.history['data'][-1]),\
                                                        style=wx.ALIGN_CENTER )\
                                                          for s in iter(self.sensors)\
                      }
        self.gSetpt = {\
                      s().GetID():FellesTextInput(
                                    self.panel,
                                    value='%s' %s().GetMetaData('sample_speed'),
                                    initial=s().GetMetaData('sample_speed'),
                                    min=s().module.min,
                                    max=10,
                                    name='asdf',
                                    target=s().UpdateSampleSpeed,
                                    source=self )   for s in iter(self.sensors)\
                      }

        # arranging and sizing the widgets
        grid_sizer.Add( FellesLabel( self.panel, wx.ID_ANY, label='Label' ,
                                         style=wx.ALIGN_CENTER ), 0, wx.ALL, 5 )
        grid_sizer.Add( FellesLabel( self.panel, wx.ID_ANY, label='Unit'  ,
                                         style=wx.ALIGN_CENTER ), 0, wx.ALL, 5 )
        grid_sizer.Add( FellesLabel( self.panel, wx.ID_ANY, label='Sample',
                                         style=wx.ALIGN_CENTER ), 0, wx.ALL, 5 )
        for s in self.sensors:
            grid_sizer.Add( self.gLabel[ s().GetID() ] , 0, wx.ALL, 5 )
            grid_sizer.Add( self.gValue[ s().GetID() ] , 0, wx.ALL, 5 )
            grid_sizer.Add( self.gSetpt[ s().GetID() ] , 0, wx.ALL, 5 )

        # alignment of title
        title_sizer.Add( FellesLabel(self, label=self.GetTitle()), 0, wx.ALL, 5)

        # overall arrangement of the panel
        top_sizer.Add( title_sizer, 0, wx.CENTER)
        top_sizer.Add( wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add( grid_sizer, 0, wx.ALL|wx.CENTER, 5)

        self.panel.SetSizerAndFit(top_sizer)
        top_sizer.Fit(self)
        self.top_sizer = top_sizer
        pub.subscribe(self.ToggleOff, 'DisableSampleRateChange')

    # ------------------------------- Method --------------------------------- #
    def ToggleOff(self):
        """
        """
        for s in self.sensors:
            self.gSetpt[s().GetID()].Disable()

        self.top_sizer.Layout()
        print "Toggle off"

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, sender=None, args=None):
        """
        Method for updating GUI
        """
        # Update label for sensor: s().GetMetaData('label')
        # with the most recent measurement: s().data.history['data'][-1]
        for s in self.sensors:
            self.gValue[s().GetID()].SetLabel( '%.2f %s' %( s().data.history['data'][-1], str(s().GetMetaData('unit'))) )

        try:
            pub.sendMessage( 'Plot.%s' %self.GetLabel() )
        except:
            self.plot_deleted = True

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

        for s in self.sensors:
            s().StopSampling()


        if not self.plot_deleted:
            pub.sendMessage( 'Close.%s' %self.GetLabel(), event=self )

        print "Window: '%s', closed by event: '%s'" %( self.GetLabel(), event.__class__.__name__ )
        self.Destroy()

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

        self.parentFrame = parent # Parent SensorFrame (from SensorGUI.py)
        self.candidates = self.parentFrame.sensors
        self.first_time = True

        # setting up plot
        self.plot_panel = wxmplot.PlotPanel(parent=self, size=(500, 500), dpi=100)

        self.plot_panel.set_xlabel('x')
        self.plot_panel.set_ylabel('y')
#        self.plot_panel.set_y2label(label)
        self.plot_panel.set_title(self.parentFrame.GetLabel())

#         plotpanel.unzoom()
#         plotpanel.unzoom_all()
#         plotpanel.set_title(title)
#         plotpanel.set_bgcol(color)
#         plotpanel.write_message(message)

        # adding sizer
        self.panel_sizer = wx.BoxSizer()
        self.panel_sizer.Add(self.plot_panel)

        # assigning the sizer to the panel
        self.SetSizer(self.panel_sizer)

        # plotIDs keeps track over which sensor to plot.
        #      ID            bool  ,       ID          bool
        # {'0x7f921e6977a0': False , '0x7f921e696530': True }
        # (The ID is the address in memory of the sensor object)
        self.plotIDs = {c().GetID() : c().plot_config['plot'] for c in self.candidates}
        self.tmp = None
        # fit the sizer to the panel
        self.Fit()

        wx.EVT_CLOSE(self, self.OnClose)
        pub.subscribe(self.OnClose, 'Close.%s' %self.parentFrame.GetLabel() )
        pub.subscribe(self.UpdatePlot, 'Plot.%s' %self.parentFrame.GetLabel() )

    # ------------------------------- Method -------------------------------- #
    def UpdatePlot(self):
        """
        Method for updating the plot frame.

        The sensors in "self.plotIDs" that are not "True" will not be plotted.
        """

        if self.first_time:
            for ID, plt in self.plotIDs.iteritems():
                if plt:
                    self.tmp = FellesBaseClass.Find(ID)
                    self.plot_panel.oplot(
                           np.array(self.tmp.data.history['time']),
                           np.array(self.tmp.data.history['data']),
                           draw=False,
                           side ='left',
                           label = self.tmp.GetMetaData('label'),
                           color = self.tmp.plot_config['color'],
                           xlabel = None, ylabel = None, y2label = None,
                           title = None,
                           dy = None,
                           ylog_scale = False,
                           xmin = None, xmax = None, ymin = None, ymax = None,
                           refresh = True,
                           show_legend= True, legend_loc='ur', legend_on= True,
                           delay_draw = False,
                           marker = 'None', markersize = None,
                           autoscale=True,
                           linewidth = 3, # default 2
                           drawstyle = 'line', style = 'solid',
                           grid = True,
                           bgcolor= None, framecolor= None, gridcolor= None,
                           labelfontsize= 10, # default 9
                           legendfontsize= 12, # default 7
                           fullbox=None, # 'box', 'open', 'bottom'
                           axes_style=None,
                           zorder=None,
                        )
            self.first_time = False

        else:
            i = 0
            for ID,plt in self.plotIDs.iteritems():
                if plt:
                    self.tmp = FellesBaseClass.Find(ID)
                    self.plot_panel.update_line(
                                i,
                                np.array(self.tmp.data.history['time']),
                                np.array(self.tmp.data.history['data']),
                                draw=plt,
                                )
                i += 1

        self.plot_panel.set_xylims(\
          [\
           floor( min( [ min( FellesBaseClass.Find(ID).data.history['time'] )\
                         for ID,plt in self.plotIDs.iteritems() if plt ] ) ),\
           ceil( max( [ max( FellesBaseClass.Find(ID).data.history['time'] )\
                         for ID,plt in self.plotIDs.iteritems() if plt ] ) ),\
           floor( min( [ min( FellesBaseClass.Find(ID).data.history['data'] )\
                         for ID,plt in self.plotIDs.iteritems() if plt ] ) ),\
           ceil( max( [ max( FellesBaseClass.Find(ID).data.history['data'] )\
                          for ID,plt in self.plotIDs.iteritems() if plt ] ) )\
          ]\
        )

        self.panel_sizer.Fit(self)

    # ------------------------------- Method --------------------------------- #
    def OnClose(self, event):
        """

        """

        print "Plot '%s' closed by event: '%s'" %(self.parentFrame.GetLabel(),\
                                                  event.__class__.__name__)
        self.Destroy()
