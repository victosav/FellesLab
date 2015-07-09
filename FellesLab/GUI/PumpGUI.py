class FellesViewPump(FellesFrame):
    """
        Mmmmmmmm sugar
    """
    
    def __init__(self, obj, *args, **kwargs):
        
        self.obj = obj
        super(FellesViewPump, self).__init__( *args, **kwargs)

        self.InitUI()


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
     
    def set_title(self, name='Pump name'):
    	self.label_name.SetLabel(name)

    def set_speed(self, speed=0):
    	self.label_speed.SetLabel(str(speed))

    def set_speed_setpoint(self, setpoint=0):
    	self.spin_setpoint.SetValue(float(setpoint)) 
