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

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"


import wx
# Classes
from wx import Frame, Button, StaticText, StaticLine, Panel, TextCtrl,\
               SpinCtrl, App #, SpinCtrlDouble
# Sizes
from wx import DefaultSize, VERTICAL, HORIZONTAL, GridSizer, BoxSizer, EXPAND,\
               ALL, CENTER
# Styles
from wx import DEFAULT_FRAME_STYLE, TE_MULTILINE, SYSTEM_MENU, CAPTION, CLOSE_BOX
# Positions
from wx import DefaultPosition
# Events
from wx import EVT_BUTTON,ID_ANY, EVT_SPINCTRL, EVT_CLOSE #, EVT_SPINCTRLDOUBLE
#
from FellesLab.Equipment import Sensor
#
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
#
from time import sleep, time
#
from FellesLab.Utils.SupportClasses import ExtendedRef, GuiUpdater


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
class FellesApp(App):
    """
    
    """
    def __init__(self):
        super(FellesApp, self).__init__()
    
    def OnInit(self):
        MainFrame = Frame(None, -1, "Main ")
        MainFrame.Show()
        return True

# =============================== Class ====================================== #
class FellesFrame(Frame):
    """
        Frame Class
    """
    sample_rate = 1.12 # Default sampling rate
    timer = GuiUpdater
    SAMPLING = True
    # ------------------------------- Method --------------------------------- #  
    def __init__(self, parent=None, *args, **kwargs):

        # Check for title 
        if not kwargs.has_key('title'):
            kwargs['title'] = 'Untitled'

        # Check for name
        if not kwargs.has_key('name'):
            kwargs['name'] = 'Un-named'

        # Check for size of frame
        if not kwargs.has_key('size'):
            kwargs['size'] = DefaultSize

        # Check for frame style
        if not kwargs.has_key('style'):
            kwargs['style'] = DEFAULT_FRAME_STYLE

        # Check for frame position
        if not kwargs.has_key('pos'):
            kwargs['pos'] = DefaultPosition

        super(FellesFrame, self).__init__(parent, *args, **kwargs)
# 
#         # Setting sampling speed (four cases are possible):
#         # 1. User provides 'sample_rate' but not 'sample_speed'
#         if kwargs.has_key('sample_rate') and not kwargs.has_key('sample_speed'):
#             self.sample_speed = kwargs['sample_rate']
#         # 2. User does not provide 'sample_rate', but 'sample_speed'
#         elif not kwargs.has_key('sample_rate') and kwargs.has_key('sample_speed'):
#             self.sample_speed = kwargs['sample_speed']
#         # 3. User provides both 'sample_rate' and 'sample_speed'
#         elif kwargs.has_key('sample_rate') and kwargs.has_key('sample_speed'):
#             print "Provided both sample speed and sample rate"
#             self.sample_speed = kwargs['sample_rate']
#         # 4. User provides neither 'sample_rate' or 'sample_speed'
#         else:
#             self.sample_speed = self.sample_rate # Default use "sample rate"

        self.timer = GuiUpdater(group=None, target=self.UpdateFrame, source=self)
        self.Bind(EVT_CLOSE, self.OnClose)

    # ------------------------------- Method --------------------------------- #
    def InitUI(self):
        NotImplementedError("User interface is not implemented")

    # ------------------------------- Method --------------------------------- #
    def OnClose(self, event):

        if event.CanVeto():# and self.fileNotSaved:

            if wx.MessageBox("The file has not been saved... continue closing?",
                             "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO) != wx.YES:

                event.Veto()
                return None

        print "Stopping frame %s" %(self.__class__.__name__)
        
        # Terminate sampling thread
        self.SAMPLING = False
        # Wait to destroy window until thread is terminated
        while self.timer.isAlive():
            pass
        # Destroy window
        self.Destroy()

#     # ------------------------------- Method --------------------------------- #
#     def OnMove(self, event):
#         print event
#         NotImplementedError("Move method is not implemented")
# 
#     # ------------------------------- Method --------------------------------- #    
#     def OnExit(self, event):
#         self.SAMPLING = False
#         print "Stopping frame %s" %(self.__class__.__name__)
# 
#     # ------------------------------- Method --------------------------------- #
#     def OnQuitApp(self):
#         self.SAMPLING = False
#         print "Stopping frame %s" %(self.__class__.__name__)

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self):
        NotImplementedError("Quit method is not implemented")

# =============================== Class ====================================== #
class FellesButton(Button):
    """
        Button Class
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, *args, **kwargs):

        # Check for source
        if not kwargs.has_key('source'):
            self.source = None
        else:
            self.source = kwargs['source']
            del kwargs['source']

        # Check for target, provide dummy output if there is none
        if not kwargs.has_key('target'):
            import DummyOutput
            self.target = DummyOutput.DummyButton()
        else:
            self.target = kwargs['target']
            del kwargs['target']

        # Names and shit...
        if not kwargs.has_key('name'):
            kwargs['name'] = self.source.GetName()

        if not kwargs.has_key('label'):
            kwargs['label'] = 'No Label'
        
        # Create button
        super(FellesButton, self).__init__(*args, **kwargs)
        # Bind button to an event executed on click
        self.Bind(EVT_BUTTON, self.OnButtonClicked)
    # ------------------------------- Method --------------------------------- #
    def OnButtonClicked(self, event):
        """
            Method executed on click
        """
        self.target(self, self.source)
    # ------------------------------- Method --------------------------------- #
    def __call__(self):
        """
            Method for calling button programatically, i.e. button()
        """
        self.target(self, self.source)


# =============================== Class ====================================== #
class FellesTextInput(SpinCtrl): #(SpinCtrlDouble):
    """
        Class
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, *args, **kwargs):

        self.source = kwargs['source']
        self.target = kwargs['target']
        del kwargs['target']
        del kwargs['source']

        if not kwargs.has_key('name'):
            kwargs['name'] = self.source.GetName()

        if not kwargs.has_key('max'):
            kwargs['max'] = 1

        if not kwargs.has_key('min'):
            kwargs['min'] = 0

        if not kwargs.has_key('initial'):
            kwargs['initial'] = kwargs['min']

        if not kwargs.has_key('inc'):
            kwargs['inc'] = 1

        super(FellesTextInput, self).__init__(*args, **kwargs)
        
        self.Bind(EVT_SPINCTRL, self.OnSetpointChange)
#        self.Bind(EVT_SPINCTRLDOUBLE, self.OnSetpointChange)
    # ------------------------------- Method --------------------------------- #
    def OnSetpointChange(self, event):
        self.target(self, self.source)

# =============================== Class ====================================== #
class FellesLabel(StaticText):
    """
        Sugar class
    """
    # ------------------------------- Method --------------------------------- #  
    def __init__(self, *args, **kwargs):
        super(FellesLabel, self).__init__(*args, **kwargs)

