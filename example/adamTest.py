"""
brief script creating a modbus connection and testing it
"""

import minimalmodbus
# from adam_modules import Adam4019




# # ADAM
# # LIQID CONTROLLER
adam = minimalmodbus.Instrument('/dev/ttyUSB0', 4)
print 'ADAM '
# print ((adam.read_register(0)/ 65535.0) - 0.6) / 0.4
# print ((adam.read_register(1)/ float(2**16 -1 )) - 0.6) / 0.4
# print ((adam.read_register(2)/ float(2**16 -1 )) - 0.6) / 0.4
# print ((adam.read_register(3)/ float(2**16 -1 )) - 0.6) / 0.4
# print ((adam.read_register(4)/ float(2**16 -1 )) - 0.6) / 0.4
# # print adam.read_long(4)
# print ((adam.read_register(5)/ float(2**16 -1 )) - 0.6) / 0.4
# print ((adam.read_register(6)/ float(2**16 -1 )) - 0.6) / 0.4
# print ((adam.read_register(7)/ float(2**16 -1 )) - 0.6) / 0.4
# # # channel = 216
for i in xrange(0,7):
	try:
		print i, adam.read_register(i)
		# print i, adam.read_string(i)
	except:
		print i
# # print adam.read_register(channel)
# print adam.read_float(channel)
# print adam.read_string(channel)
# print adam.read_float(0)
# print adam.read_float(4)
# print adam.read_register(0)

if None == 0:
	print 'Eselballe'
