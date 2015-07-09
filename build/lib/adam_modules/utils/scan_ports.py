# -*- coding: ascii -*-
"""

oooooooooooo       oooo oooo                    ooooo                 .o8      
`888'     `8       `888 `888                    `888'                "888      
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo. 
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Function locating serial ports that are in use.
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

import serial
import platform
import minimalmodbus
from serial.tools import list_ports

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



def scan_addresses(port, start_address=0, end_address=256):
    """
    Search for Modus compatible units on a serial port.
    """
    available_modbus_modules = []

    for address in range(start_address, end_address):
        try:
            instrument = minimalmodbus.Instrument(port, address)
            instrument.read_register(0, 1)
            available_modbus_modules.append(address)
            break
        except:
            pass

    return available_modbus_modules


if __name__ == '__main__':
    print(list(scan_ports()))
