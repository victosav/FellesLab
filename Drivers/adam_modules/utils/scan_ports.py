
"""
Module for finding the serial ports that are in use.
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
