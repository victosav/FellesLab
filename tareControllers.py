#!/usr/bin/python
# -*- coding: ascii -*-

"""
brief script creating a modbus connection and testing it
"""

import minimalmodbus
from adam_modules import Adam4019


def tareControllers():
	portName = '/dev/ttyUSB0'
	adamModule = Adam4019(portname=portName, slaveaddress=4)

	# Pressure controller
	resource = minimalmodbus.Instrument('/dev/ttyUSB0', 29)
	resource.write_register(23,640*17)

	# LIQID CONTROLLER
	r2 = minimalmodbus.Instrument('/dev/ttyUSB0', 23)
	r2.write_register(23,640*0)

	# CO2 CONTROLLER
	r3 = minimalmodbus.Instrument('/dev/ttyUSB0', 21)
	r3.write_register(23,0)

	# N2
	r4 = minimalmodbus.Instrument('/dev/ttyUSB0', 17)
	r4.write_register(23,0)

if __name__ == '__main__':
	tareControllers()



