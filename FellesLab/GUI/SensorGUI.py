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
@license:      Free (GPL.v3), although credit is appreciated  
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:     
@change:       
@note:         

"""

# Classes
from wx import Frame, Button, StaticText, StaticLine, Panel
# Sizes
from wx import DefaultSize, VERTICAL, HORIZONTAL, GridSizer, BoxSizer, EXPAND,\
               ALL, CENTER
# Styles
from wx import DEFAULT_FRAME_STYLE
# Positions
from wx import DefaultPosition
# Events
from wx import EVT_BUTTON, ID_ANY#, EVT_SPINCTRLDOUBLE
# Basic GUI classes
from GUI import FellesFrame, FellesButton, FellesTextInput, FellesLabel
#
from Sensor import Sensor

def findSensor(_id):
    for s in Sensor.___refs___:
        if s()['_id'] == _id:
            return s

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


def InitiateSensors():
     for s in Sensor.___refs___:
         s().StartSampling()
    
def StopSensors():
     for s in Sensor.___refs___:
         s().StopSampling()


# =============================== Class ====================================== #
class FellesSensorGUI(FellesFrame):
    """
        Class
    """
    # ------------------------------- Method --------------------------------- #  
    def __init__(self, *args, **kwargs):
        Windows = sensorTypes()
        print Windows

        super(FellesSensorGUI, self).__init__( *args, **kwargs)

        self.InitUI()
    
    # ------------------------------- Method --------------------------------- #
    def InitUI(self):
        
        # adding panel for cross-platform appearance 
        self.panel = wx.Panel(self, ID_ANY)

        # adding sizers
        top_sizer       = BoxSizer(VERTICAL)
        title_sizer     = BoxSizer(HORIZONTAL)
        grid_sizer      = GridSizer(rows=2, cols=2, hgap=5, vgap=5)
        input_sizer     = BoxSizer(HORIZONTAL)
        button_sizer    = BoxSizer(HORIZONTAL)
        
        # adding GUI widgets
        self.label_name = StaticText(self.panel, label='{sensor} Sensor'.format(sensor=self.obj.__class__.__name__) )

        self.label_description_speed = FellesLabel(self.panel, label='{label}'.format(label=self.GetLabel()))
        self.label_speed = FellesLabel(self.panel, label='{unit}'.format(unit=self.obj['unit']))

        self.label_setpoint = FellesLabel(self.panel, label='{msmnt} [{unit}]'.format(msmnt=self.obj.__class__.__name__,unit=self.obj['unit']))
        
        # arranging and sizing the widgets 
        # alignment of title
        title_sizer.Add(self.label_name, 0, ALL, 5)

        # arrangement of the pump setpoint and pump speed 
        grid_sizer.Add(self.label_setpoint, 0, ALL, 5)
        grid_sizer.Add(self.label_description_speed, 0, ALL, 5)
        grid_sizer.Add(self.label_speed, 0, ALL, 5)

        # overall arrangement of the panel
        top_sizer.Add(title_sizer, 0, CENTER)
        top_sizer.Add(StaticLine(self.panel), 0, ALL|EXPAND, 5)
        top_sizer.Add(grid_sizer, 0, ALL|CENTER, 5)
        top_sizer.Add(StaticLine(self.panel), 0, ALL|EXPAND, 5)
        top_sizer.Add(button_sizer, 0, ALL|CENTER, 5)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        top_sizer.Fit(self)


