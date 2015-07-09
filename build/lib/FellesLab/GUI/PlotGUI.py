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

class FellesPlot(wx.Frame):
    """
    
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor
        """
        super(FellesPlot, self).__init__(parent)
        
        # Input: parent, X, Y, 

        self.candidates = kwargs['sensors']
        #self.number_of_lines = len(plot_fields)
        self.first_time = True

        self.ymin = min( [ min(c().data.history['data']) for c in self.candidates ] )
        self.ymax = min( [ max(c().data.history['data']) for c in self.candidates ] )

        # setting up plot
        self.plotpanel = wxmplot.PlotPanel(parent=self, size=(500, 350), dpi=100)
        self.plotpanel.messenger = self.write_message

        # adding sizer
        self.panel_sizer = wx.BoxSizer()
        self.panel_sizer.Add(self.plotpanel)

        # assigning the sizer to the panel
        self.SetSizer(self.panel_sizer)

        # Retrieve plot data
        self.plots = {}
        print self.PlotData()
        for id,dct in self.PlotData().iteritems():
            #self.plots[id] = self.plotpanel.oplot(
            self.plotpanel.oplot(
                                   dct['x'],
                                   dct['y'],
                                   side ='left',
                                   label = dct['label'],
                                   color = dct['color'],
                                   show_legend=True,
                                   style = 'solid',
                                   draw=False,
                                   grid=True,
                                 )

        # fit the sizer to the panel
        self.Fit()

    # ------------------------------- Method -------------------------------- #
    def write_message(self, message, panel=0):
        pass

    # ------------------------------- Method -------------------------------- #
    def UpdatePlot(self):
        """
        
        """
        # Retrieve plot data
        data = self.PlotData()

#         for id in data.iterkeys():
#             #self.plots[id] = self.plotpanel.update_line(0, data[id]['x'], data[id]['y'], side ='left')
#             self.plotpanel.update_line(0, data[id]['x'], data[id]['y'], draw=False)

        self.plotpanel.set_xylims([ floor(min( [ min(data[id]['x']) for id in data.iterkeys()] )),\
                                    ceil( max( [ max(data[id]['x']) for id in data.iterkeys()] )),\
                                    floor(min( [ min(data[id]['y']) for id in data.iterkeys()] )),\
                                    ceil( max( [ max(data[id]['y']) for id in data.iterkeys()] ))\
                                   ])

        self.panel_sizer.Fit(self)

    # ------------------------------- Method -------------------------------- #
    def PlotData(self):
        """
        
        """
        data = {}
        for c in self.candidates:
            if c().plot_config['plot']:
                data[c().ID] = {
                            'x': np.array(c().data.history['time']),\
                            'y': np.array(c().data.history['data']),\
                        'color': c().plot_config['color'],\
                        'label': c().meta['label']
                            }
        return data


if __name__ == '__main__':
    app = wx.App()

    plot = FellesPlot()
    plot.Show()

    x = np.linspace(0., 20, 1000)
    y = 5*np.sin(4*x)/(x+6)
    plot.update_plot(x, y)
    

    app.MainLoop()
