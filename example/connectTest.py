"""
brief script creating a modbus connection and testing it
"""

import minimalmodbus

resource = minimalmodbus.Instrument('/dev/ttyUSB0', 1)

resource.read_register(64)

# resource.write_register(64, 21)