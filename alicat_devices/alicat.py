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
@author:       Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
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
        self.slaveaddress = 'slaveaddress'
        self.portname = 'COMport'
        self.serial = DummySerial()
    # ------------------------------- Method -------------------------------- #
    def read_register(self, channel):
        return random()
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
class Device(minimalmodbus.Instrument, object):
    """
    
    """
    def __init__(self, *args, **kwargs):
        super(Device, self).__init__(**kwargs)

# ================================= Class =================================== #
class AlicatModule(Device):
    """
      * Print port settings: stty --file=/dev/ttyUSB0
      * Print all settings for port: stty --file=/dev/USB0 -a
      * Reset port to default values: stty --file=/dev/ttyUSB0 sane
      * Change port to raw behaviour: stty --file=/dev/ttyUSB0 raw
      * and: stty --file=/dev/ttyUSB0 -echo -echoe -echok
      * Change port baudrate: stty --file=/dev/ttyUSB0 19200
    """

    fluids = ["Air", "Ar", "CH4", "CO", "CO2", "C2H6", "H2", "He", "N2", "N2O",
              "Ne", "O2", "C3H8", "n-C4H10", "C2H2", "C2H4", "i-C2H10", "Kr", 
              "Xe", "SF6", "C-25", "C-10", "C-8", "C-2", "C-75", "A-75", 
              "A-25", "A1025", "Star29", "P-5"]

    info = ["flow_setpoint", "gas", "mass_flow", "pressure", "temperature", 
            "volumetric_flow"]

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
        addCls = {'Dummy': DummyModbus, 'Instrument': Device}[base]
        cls = type(cls.__name__ + '+' + addCls.__name__, (cls, addCls), {})

        return  super(AlicatModule, cls).__new__(cls)

    # ------------------------------- Method -------------------------------- #
    def __init__(self, port="/dev/ttyUSB0", baudrate=19200, address="A", timeout=0.25):
        """
        Connects with the appropriate USB / serial port.

        Args:
            port: The serial port. Default "/dev/ttyUSB0".
            address: The Alicat-specified address, A-Z. Default "A".
        """

        if ('slaveaddress') not in kwargs:
            Exception("Required arguments are missing")

        if ('mode') not in kwargs:
          kwargs['mode'] = minimalmodbus.MODE_ASCII

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



# ================================= Class =================================== #
class FlowMeter(AlicatModule):
    """
    
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(FlowMeter, self).__init__(*args, **kwargs)

# ================================= Class =================================== #
class FlowController(AlicatModule):
    """
    
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(FlowController, self).__init__(*args, **kwargs)
    # ------------------------------- Method -------------------------------- #
    def set_flow_rate(self, flow, retries=2):
        """Sets the target flow rate.

        Args:
            flow: The target flow rate, in units specified at time of purchase
        """
        command = "{addr}S{flow:.2f}\r\n".format(addr=self.address, flow=flow)
        line = self._write_and_read(command, retries)
        if abs(float(line) - flow) > 0.01:
            raise IOError("Could not set flow.")


