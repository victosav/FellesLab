# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Module for setting up a Modbus communication with minimalmodbus
               to Adam-4000 and Adam-4100 modules
@author:       Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3)
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@TODO 1.0:     Only Adam4019 and 4024 has really been tested...
@TODO 2.0:     Methods should start with caps, some order in the universe...
@TODO 3.0:     Write general getter/setter methods for the modules
@TODO 4.0:     Provide actually helpfull error messages
@TODO 5.0:     Write a "meta-data" convention to facilitate info to a user...
@TODO 6.0:     Document!
@change:
@note: Usage

# import adam module
from adam_modules import Adam4019

# Connect to adam module:
module = Adam4019(portname='/dev/ttyUSB0', slaveaddress=9)

# Dummy module for developer use:
module = Adam4019("Dummy")

"""

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

import minimalmodbus
from utils import scan_ports
from random import random

# ================================= Class =================================== #
class DummySerial(object):
    """
    Dummy class impersonating a serial connection
    """
    port = 'Dummy' # serial port name
    baudrate = 9600 # Transfer rate: bits/s
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
    Dummy class impersonating a Adam module
    """

    def __init__(self, *args, **kwargs):
        self.slaveaddress = 'slaveaddress'
        self.portname = 'portname'
        self.serial = DummySerial()
    # ------------------------------- Method -------------------------------- #
    def read_register(self, channel, numberOfDecimals):
        if numberOfDecimals == 0:
            return random()
        else:
            return random() * numberOfDecimals * 10
    # ------------------------------- Method -------------------------------- #
    def read_registers(self, channel, number_of_channels):
        return random()
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
    # ------------------------------- Method -------------------------------- #
    def flushOutput(self):
        pass
    # ------------------------------- Method -------------------------------- #
    def flushInput(self):
        pass
    # ------------------------------- Method -------------------------------- #
    def write(self, msg):
        pass
    # ------------------------------- Method -------------------------------- #
    def read(self):
        pass


# ================================= Class =================================== #
class Instrument(minimalmodbus.Instrument, object):
    """
    Sugar class.

    The reason it is used is the following:
        minimalmodbus.Instrument is an old-style class, does not work with
        __new__ or super(). However, by inheriting "object" (new-style) it can
        be "tricked" into thinking it is a new-style class...
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, portname, slaveaddress, mode=minimalmodbus.MODE_RTU):
        super(Instrument, self).__init__(portname, slaveaddress, mode)

# ================================= Class =================================== #
class AdamModule(object):
    """
    Parent class for ADAM modules

    Args:
         * portname (string, e.g. '/dev/ttyUSB1'): port name
         * slaveaddress (integer): slave address in the range 1 to 247
    """
    def __new__(cls, base='Instrument', *args, **kwargs):
        """
        Creator.
        called !!before!! __init__, returns instance.

        Changes the "type" of the class according to 'base', default is to
        attempt connecting to the AdamModule, however, it is possible to
        add an argument "Dummy" for "simulating" the Adam module.

        This is how it looks like:
          < adam_modules.adam_modules.'MODULE' + 'BASE' object at ... >
            MODULE: Adam4019 etc...
            MODE: Dummy or Instrument
        """
        addCls = {'Dummy': DummyModbus, 'Instrument': Instrument}[base]
        cls = type(cls.__name__ + '+' + addCls.__name__, (cls, addCls), {})

        return  super(AdamModule, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """

        if ('slaveaddress') not in kwargs:
            Exception("Required arguments are missing")

        if ('mode') not in kwargs:
          kwargs['mode'] = 'rtu'

        if not kwargs.has_key('port'):
            # Search for port
            # TODO: Implement possibility for adding a "hint" e.g. 'USB', use
            #       regex to match "hint" to portnames.
            for port in list(scan_ports()):
                try:
                    super(AdamModule, self).__init__(port, kwargs['slaveaddress'], mode=kwargs['mode'])
                    if self.is_correct_module():
                        break
                except:
                    Exception("Signal portname on the ADAM module is missing")
        else:
            super(AdamModule, self).__init__(kwargs['port'], kwargs['slaveaddress'], mode=kwargs['mode'])

        self.metaData = {
            'port' : 'asdf',#self.serial.port,
            'baudrate' : 'asdf',#self.serial.baudrate,
            'bytesize' : 'asdf',#self.serial.bytesize,
            'parity' : 'asdf',#self.serial.parity,
            'timeout' : 'asdf',#self.serial.timeout,
            'channel': None,
            'decimals' : 0,
        }

    # ------------------------------- Method -------------------------------- #
    def SetMetaData(self, key, val):
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
    def GetMetaData(self, key=None):
        """
        """
        return self.metaData if not key else self.metaData[key]

    # ------------------------------- Method -------------------------------- #
    def module_name(self):
        """
        Read name from module
        """
        return self.read_register(210) # child.moduleName

    # ------------------------------- Method -------------------------------- #
    def module_version(self):
        """
            Read module version
        """
        return self.read_register(212) # child.moduleVersion

    # ------------------------------- Method -------------------------------- #
    def is_correct_module(self):
        """
        Check if the module class is correct

        TODO: This is a bad check, consider simply removing it...
        """
        if self.name == self.module_name(): #
            return True
        else:
            return False

    # ------------------------------- Method -------------------------------- #
    def is_valid_channel(self, channel, number_of_channels):
        """
        Check if channel is valid

        TODO: This is a bad check, consider simply removing it...
        """
        try:
            int(channel)
        except ValueError:
            print('Channel input not an integer')
            return False

        if channel >= 0 and channel <= number_of_channels:
            return True
        else:
            print('Channel input outside available channels: [0, ' + str(number_of_channels) + ']')
            return False

    # ------------------------------- Method -------------------------------- #
    def __getitem__(self, key):
        """
        Method for retrieving meta information
        """
        return self.metaData[key]

    # ------------------------------- Method -------------------------------- #
    def __setitem__(self, key, val):
        """
        Method for setting meta information
        """
        self.metaData[key] = val
        return None

    # ------------------------------- Method -------------------------------- #
    def get_in(self):
        """
        TODO: write a general getter/setter method for the modules!
        """
        pass

# ================================= Class =================================== #
class AnalogIn(AdamModule):
    """
        Class for analog input ADAM modules
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
            Constructor
        """
        AdamModule.__init__(self, *args, **kwargs)
    # ------------------------------- Method -------------------------------- #
    def get_analog_in(self, channel=-1, numberOfDecimals=0):
        """
        Getter method
        """
        if channel == -1:
            # TODO for some reason analog_in_start_channel is a tuple... why!?
            return self.read_registers(self.analog_in_start_channel[0] - 1, self.analog_in_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_in_number_of_channels):
            return self.read_register(self.analog_in_start_channel[0] - 1 + channel, numberOfDecimals)
        else:
            print('Channel out of range')
    # ------------------------------- Method -------------------------------- #
    def set_type_analog_in(self, channel, value):
        """
        Setter method
        """
        return self.write_register(self.type_analog_in_start_channel - 1 + channel, value)
    # ------------------------------- Method -------------------------------- #
    def get_type_analog_in(self, channel=-1, numberOfDecimals = 0):
        """
            Getter method
        """
        if channel == -1:
            return self.read_registers(self.type_analog_in_start_channel - 1, self.analog_in_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_in_number_of_channels):
            return self.read_register(self.type_analog_in_start_channel - 1 + channel, numberOfDecimals)
        else:
            print('Channel out of range')
    # ------------------------------- Method -------------------------------- #
    def get_burn_out_signal(self, channel):
        """
            Burn signal
        """
        return self.read_bit(self.burn_out_signal_start_channel - 1 + channel)

# ================================= Class =================================== #
class AnalogOut(AdamModule):
    analog_out_start_channel = 1
    type_analog_out_start_channel = 201
    analog_out_number_of_channels = 8
    # ------------------------------- Method -------------------------------- #
    def set_analog_out(self, channel, value):
        """
            Setter
        """
        return self.write_register(self.analog_out_start_channel - 1 + channel, value)
    # ------------------------------- Method -------------------------------- #
    def get_analog_out(self, channel=-1):
        """
            Getter
        """
        if channel == -1:
            return self.read_registers(self.analog_out_start_channel - 1, self.analog_out_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_out_number_of_channels):
            return self.read_register(self.analog_out_start_channel - 1 + channel)
        else:
            print('Channel out of range')
    # ------------------------------- Method -------------------------------- #
    def set_type_analog_out(self, channel, value):
        """
            Setter
        """
        return self.read_register(self.analog_out_start_channel - 1 + channel, value)
    # ------------------------------- Method -------------------------------- #
    def get_type_analog_out(self, channel=False):
        """
            Getter
        """
        if channel == -1:
            return self.read_registers(self.analog_out_start_channel - 1, self.analog_out_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_out_number_of_channels):
            return self.read_register(self.analog_out_start_channel - 1 + channel)
        else:
            print('Channel out of range')

# ================================= Class =================================== #
class DigitalIn(AdamModule):
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 8
    # ------------------------------- Method -------------------------------- #
    def get_digital_in(self, channel):
        """
            Getter
        """
        return self.read_bit(self.diginal_in_start_channel - 1 + channel)

# ================================= Class =================================== #
class DigitalOut(AdamModule):
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8
    # ------------------------------- Method -------------------------------- #
    def set_digital_out(self, channel, value):
        """
            Setter
        """
        return self.write_bit(self.digital_out_start_channel - 1 + channel, value)
    # ------------------------------- Method -------------------------------- #
    def get_digital_out(self, channel):
        """
            Getter
        """
        return self.read_bit(self.digital_out_start_channel - 1 + channel)

# ================================= Class =================================== #
class Adam4117(AnalogIn):
    """
    Adam-4117
    """
    name = 16663
    analog_in_start_channel = 1
    type_analog_in_start_channel = 201
    burn_out_signal_start_channel = 1
    analog_in_number_of_channels = 8
    # ---------------------------- Method ----------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        kwargs['module'] = self
        super(Adam4117, self).__init__(self, *args, **kwargs)
    # Type       Code
    # +/- 100mV: 2
    # +/-500 mV: 3
    # +/-1V:     4
    # +/- 2,5V:  5
    # 4~20mA:    7
    # +/-10V:    8
    # +/-5V:     9
    # 0~20 mA:   13
    # K:         15
    # T:         16
    # E:         17
    # R:         18
    # S:         19
    # B:         20
    # J:         14

# ================================= Class =================================== #
class Adam4019(AnalogIn):
    """
        ADAM4019 sugar class
    """
    analog_in_start_channel = 1,
    type_analog_in_start_channel = 201,
    burn_out_signal_start_channel = 1,
    analog_in_number_of_channels = 8
    min = 0.1
    # ---------------------------- Method ----------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        kwargs['module'] = self
        super(Adam4019, self).__init__(self, *args, **kwargs)


# ================================= Class =================================== #
class Adam4024(AnalogOut, DigitalIn):
    """
    ADAM4024
    """
    name = None
    analog_in_start_channel = 1
    type_analog_in_start_channel = 201
    burn_out_signal_start_channel = 201
    analog_in_number_of_channels = 4
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 4
    # ---------------------------- Method ----------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
    # Analog out signal range is 0 to 409[5 or 6]
    # should scale such that value goes from 0 to 1

    # Types
    # 48: 0~20 mA
    # 49: +/- 10V
    # 50: 4~20 mA
        kwargs['module'] = self
        super(Adam4024, self).__init__(self, *args, **kwargs)

# ================================= Class =================================== #
class Adam4055(DigitalIn, DigitalOut):
    """
    ADAM4055
    """
    name = None
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 8
    # ---------------------------- Method ----------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        kwargs['module'] = self
        super(Adam4055, self).__init__(self, *args, **kwargs)

# ================================= Class =================================== #
class Adam4069(DigitalOut):
    """
    ADAM4069
    """
    name = None
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8
    # ---------------------------- Method ----------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        kwargs['module'] = self
        super(Adam4069, self).__init__(self, *args, **kwargs)
