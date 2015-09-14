"""
brief script creating a modbus connection and testing it
"""

import minimalmodbus
from adam_modules import Adam4019

portName = '/dev/ttyUSB0'
adamModule = Adam4019(portname=portName, slaveaddress=4)

# Pressure controller
resource = minimalmodbus.Instrument('/dev/ttyUSB0', 29)
print 'ID: ',
print resource.read_register(64)
print 'Setpoint1: ',
print resource.read_register(2047)
print 'Setpoint2: ',
print resource.read_register(2048)
print 'Pressure: ',
print resource.read_register(2040)
# resource.write_register(23,10000)
print resource.read_register(2048)
# print
# print 'ID: ',
# print resource.read_float(64)
# print 'Setpoint1: ',
# print resource.read_float(2047)
# print 'Setpoint2: ',
# print str(resource.read_float(2048))
# print 'Pressure: ',
# print resource.read_float(2040)
# # resource.write_register(23,10000)
# print 'Flow: ',
# print resource.read_float(2044)
# print



# LIQID CONTROLLER
r2 = minimalmodbus.Instrument('/dev/ttyUSB0', 23)
print 'ID: ',
print r2.read_register(64)
print 'Setpoint1: ',
print r2.read_register(2047)
print 'Setpoint2: ',
print r2.read_register(2049)
print 'Pressure: ',
print r2.read_register(2040)
print 'Pressure2: ',
print r2.read_register(2041)
print 'Termperature',
print r2.read_register(2042)
print 'Setpoint',
# r2.write_register(24,64000)
print r2.read_register(2047)
print

# LIQID CONTROLLER
r3 = minimalmodbus.Instrument('/dev/ttyUSB0', 21)
print 'ID: ',
print r3.read_register(64)
print 'Setpoint1: ',
print r3.read_register(2047)
print 'Setpoint2: ',
print r3.read_register(2049)
print 'Pressure: ',
print r3.read_register(2040)
print 'Pressure2: ',
print r3.read_register(2041)
print 'Termperature',
print r3.read_register(2042)
print 'Setpoint',
# r3.write_register(23,6000)
print r3.read_register(2048)
print


	# print 
	# print resource.read_register(24)
	# resource.write_register(24,16000)

	# resource.write_register(2047, 16000)


r4 = minimalmodbus.Instrument('/dev/ttyUSB0', 17)
print 'ID: ',
print r4.read_register(64)
print 'Setpoint1: ',
print r4.read_register(2047)
print 'Setpoint2: ',
print r4.read_register(2049)
print 'Pressure: ',
print r4.read_register(2040)
print 'Pressure2: ',
print r4.read_register(2041)
print 'Termperature',
print r4.read_register(2042)
print 'Setpoint',
# r4.write_register(23,0)
print r4.read_register(2048)
print


# ADAM
# LIQID CONTROLLER
adam = minimalmodbus.Instrument('/dev/ttyUSB0', 4)
print 'ADAM '
print adam.read_register(1)
print adam.read_register(2)
print adam.read_register(3)
print adam.read_register(4)
print adam.read_register(5)
print adam.read_register(6)
print adam.read_register(7)

