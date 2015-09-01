# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Python driver for Alicat mass flow controller devices
@author:       Arne Tobias Elve and Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      elve@ntnu.no        sigveka@ntnu.no
@license:      Free (GPL.v3)
@requires:     Python 2.7.6 or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:

[manual](http://minimalmodbus.sourceforge.net/minimalmodbus.pdf)

Data type in slave |      Read       | Function |      Write       | Function| 
-------------------|-----------------|----------|------------------|---------|
Bit                | read_bit()      | 2 [or 1] | write_bit()      |  5 [15] | 
Register Integer   | read_register() | 3 [or 4] | write_register() | 16 [ 6] | 
Long (32bits=2regs)| read_long()     | 3 [or 4] | write_long()     | 16      | 
Float(32 or 64bits)| read_float()    | 3 [or 4] | write_float()    | 16      | 
String             | read_string()   | 3 [or 4] | write_string()   | 16      | 
Registers Integers | read_registers()| 3 [or 4] | write_registers()| 16      | 

"""

import minimalmodbus
from random import random

import serial
import platform
from serial.tools import list_ports


# ================================= Class =================================== #
class DummySerial(object):
    """
    Dummy class impersonating a serial connection
    """
    port = 'Dummy' # serial port name
    baudrate = 19200 # Transfer rate: bits/s
    bytesize = 8 # bits in a byte
    parity = minimalmodbus.serial.PARITY_NONE # the same as: 'N'
    timeout = 0.05 # seconds
    mode = minimalmodbus.MODE_RTU # or minimalmodbus.MODE_ASCII # <=> 'rtu' or 'ascii'

    def flushOutput(self):
        pass
    def flushInput(self):
        pass
    def write(self, message):
        pass
    def read(self):
        return 'FooBar'

# ================================= Class =================================== #
class DummyModbus(object):
    """
    Dummy class impersonating an Alicat module
    """
    from random import random

    def __init__(self, *args, **kwargs):
        self.slaveaddress = 1
        self.portname = 'COMport'
        self.serial = DummySerial()
    # ------------------------------- Method -------------------------------- #
    def read_register(self, channel):
        return 1
#        if channel == 2054 or channel == 2048:
#            return 1
#        
#        return random()
    # ------------------------------- Method -------------------------------- #
    def read_registers(self, channel, number_of_channels):
        return list()
    # ------------------------------- Method -------------------------------- #
    def read_bit(self, channel):
        return None
    # ------------------------------- Method -------------------------------- #
    def read_float(self, channel):
        return random()
    # ------------------------------- Method -------------------------------- #
    def read_long(self, channel):
        return random()
    # ------------------------------- Method -------------------------------- #
    def read_string(self, channel):
        return random()
    # ------------------------------- Method -------------------------------- #
    def write_float(self, channel, value):
        pass
    # ------------------------------- Method -------------------------------- #
    def write_long(self, channel, value):
        pass
    # ------------------------------- Method -------------------------------- #
    def write_registers(self, channel, value):
        pass
    # ------------------------------- Method -------------------------------- #
    def write_string(self, channel, value):
        pass
    # ------------------------------- Method -------------------------------- #
    def write_register(self, channel, value):
        pass
    # ------------------------------- Method -------------------------------- #
    def write_bit(self, channel, value):
        pass

# ================================= Class =================================== #
class Instrument(minimalmodbus.Instrument, object):
    """
    
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, portname, slaveaddress, mode=minimalmodbus.MODE_RTU):
        super(Instrument, self).__init__(portname, slaveaddress, mode)


# ================================= Class =================================== #

class AlicatModule(object):
    """
    Mother class for all the different alicat module. 
    TODO:
    Add gas mass flow controller
    Add liquid mass flow controller
    Add pressure controller
    """

    # FLUIDS = {"Air":0, "Ar":1, "CH4":2, "CO":3, "CO2":4, "C2H6":5, "H2":6, 
    #           "He":7, "N2":8, "N2O":9, "Ne":10, "O2":11, "C3H8":12, 
    #           "n-C4H10":13, "C2H2":14, "C2H4":15, "i-C2H10":16, "Kr":17, 
    #           "Xe":18, "SF6":19, "C-25":20, "C-10":21, "C-8":22, "C-2":23, 
    #           "C-75":24, "A-75":25, "A-25":26, "A1025":27, "Star29":28, "P-5":29}

    # INFO = ["flow_setpoint", "gas", "mass_flow", "pressure", "temperature", 
    #         "volumetric_flow"]

    # ------------------------------- Method -------------------------------- #
    def __new__(cls, base='Instrument', *args, **kwargs):
        """
        Creator.
        called !!before!! __init__, returns instance.

        Changes the "type" of the class according to 'base', default is to
        attempt connecting to the AdamModule, however, it is possible to
        add an argument "Dummy" for "simulating" the Adam module.

        This is how it looks like:
          < alicat.alicat_modules.'DEVICE' + 'BASE' object at ... >
            MODULE: Adam4019 etc...
            MODE: Dummy or Instrument
        """
        addCls = {'Dummy': DummyModbus, 'Instrument': Instrument}[base]
        cls = type(cls.__name__ + '+' + addCls.__name__, (cls, addCls), {})

        return  super(AlicatModule, cls).__new__(cls)

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        Connects with the appropriate USB / serial port.

        Args:
            port: The serial port. Default "/dev/ttyUSB0".
            address: The Alicat-specified address, A-Z. Default "A".
        """

        if ('slaveaddress') not in kwargs:
            Exception("Required arguments are missing")

        if ('mode') not in kwargs:
          kwargs['mode'] = minimalmodbus.MODE_RTU

        if not kwargs.has_key('port'):
            # Search for port
            # TODO: Implement possibility for adding a "hint" e.g. 'USB', use
            #       regex to match "hint" to portnames.
            for port in list(self.scan_ports()):
                try:
                    super(AlicatModule, self).__init__(port, kwargs['slaveaddress'], mode=kwargs['mode'])
                    if self.is_correct_module():
                        break
                except:
                    Exception("Signal portname on the ADAM module is missing")
        else:
            super(AlicatModule, self).__init__(kwargs['port'], kwargs['slaveaddress'], mode=kwargs['mode'])

        self.metaData = {
            'baudrate' : 'asdf',#self.serial.baudrate,
            'bytesize' : 'asdf',#self.serial.bytesize,
            'parity' : 'asdf',#self.serial.parity,
            'timeout' : 'asdf',#self.serial.timeout,
            'channel': None,
            'decimals' : 0,
            'debug' : False,
        }

    # ------------------------------- Method -------------------------------- #
    def __setitem__(self, key, val):
        """
        Configuration method for changing the following parameters:
          port = str       # serial port name
          baudrate = int   # 9600 (default) or 19200
          bytesize = int   # 8 (default) or 16
          parity   = str   # serial.PARITY_NONE (default)
          stopbits = int   # 1 (default)
          timeout  = float # 0.05 (default)
          address          # this is the slave address number
          mode = str       # minimalmodbus.MODE_RTU,   'rtu' (default) or
                             minimalmodbus.MODE_ASCII, 'ascii' mode

        The method is inked by __init__ when called as:
            xxxModule(portname, slaveaddress, config={ key:val} )
        using the keys listed above.
        """
        self.metaData[key] = val

    # ------------------------------- Method -------------------------------- #
    def __iter__(self):
        return self.metaData.iteritems()

    # ------------------------------- Method -------------------------------- #
    def __getitem__(self, key):
        """
        """
        return self.metaData[key]

    # ------------------------------- Method -------------------------------- #
    @staticmethod
    def scan_ports():
        """
        Returns a generator for all available serial ports.
        """
        system = platform.system()  # Checks the current operating system
        if system == 'Windows':  # Windows
            print('Windows system')
            for i in range(256):
                try:   
                    serial_port = serial.Serial(i)
                    serial_port.close()
                    yield i
                except serial.SerialException:
                    pass
        elif system == 'Linux' or 'Darwin':  # Linux or osX
            print('Unix system')
            for port in list_ports.comports():
                yield port[0]


# class AlicatGMF(AlicatModule):
# 	"""Class used for the gasous mass flow controllers"""
# 	def __init__(self, *args, **kwargs):
# 		super(AlicatGMF, self).__init__(*args, **kwargs)
# *		self.args = args
# **		self.kwargs = kwargs
		