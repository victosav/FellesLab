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


class Panel(wx.Panel):
    def __init__(self, parent, id, pos, size):
        wx.Panel.__init__(self, parent, id, pos, size) 

class Frame(wx.Frame):
    def __init__(self, parent, id, title, pos, size, style):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        framePanel = wx.Panel(self)
        self.userpanel = Panel(framePanel, -1, (0,0), (300,180))
        self.userpanel.SetBackgroundColour('Gold')

class FellesApp(wx.App):

    def __init__(self):
        super(FellesApp, self).__init__()

        self.InitUI()

    def InitUI(self):
        wx.App.__init__(self)
        frame = Frame(None, -1, "Internet Login Tool", (-1,-1), (300,400),\
        wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        frame.Show()
        self.SetTopWindow(frame)


# =============================== Class ====================================== #
class MainFrame(wx.Frame):
    """
    
    """
    # ------------------------------- Method --------------------------------- #  
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor
        """
        super(MainFrame, self).__init__(parent, **kwargs)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    
    def InitUI(self):
        """
        Create 
        """
        # Create two buttons, Start/Stop sampling
        # Stop sampling should close all windows and stop all threads
        pass
    
    def StartSampling(self):
        """
        Start sampling, i.e. start writing numbers to file(s). 
        
        Disable all 
        """
        
        pass
    
    def PauseSampling(self):
        """
        Pause sampling, i.e. stop writing numbers to file(s), but keep file open.
        Print warning that the clock is "stupid" and will have sudden "jumps".

        time  msrmnt
        10.0  12345
        10.5  54321
        11.0  24135
        40.5  41253

        """
        pass

    def StopSampling(self):
        """
        Stop sampling, i.e. stop writing numbers to file(s), close files, 
        print message, ask for filename, and close all windows. 
        """
        pass
    
    def OnClose(self, event):
        """
        1. StopSampling
        2. close...
        """
        pass


# =============================== Class ====================================== #
class FellesFrame(wx.Frame):
    """
        Frame Class
    """
    sample_rate = 1.2 # Default sampling rate
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
            kwargs['size'] = wx.DefaultSize

        # Check for frame style
        if not kwargs.has_key('style'):
            kwargs['style'] = wx.DEFAULT_FRAME_STYLE

        # Check for frame position
        if not kwargs.has_key('pos'):
            kwargs['pos'] = wx.DefaultPosition

        super(FellesFrame, self).__init__(parent, *args, **kwargs)


        self.timer = GuiUpdater(group=None, target=self.UpdateFrame, source=self)
        # self.Bind(wx.EVT_CLOSE, self.OnClose)

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
class FellesButton(wx.Button):
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
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
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
class FellesTextInput(wx.SpinCtrl): #(wx.SpinCtrlDouble):
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
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSetpointChange)
#        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSetpointChange)
    # ------------------------------- Method --------------------------------- #
    def OnSetpointChange(self, event):
        self.target(self, self.source)

# =============================== Class ====================================== #
class FellesLabel(wx.StaticText):
    """
        Sugar class
    """
    # ------------------------------- Method --------------------------------- #  
    def __init__(self, *args, **kwargs):
        super(FellesLabel, self).__init__(*args, **kwargs)

