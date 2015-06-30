'''
Parameter list, also known as registry.
In order to switch from one motor to another, 
the registry corresponding to the parameter should be altered.

:motormode: The mode that the motor can obtain, must be 0 or 1.(0=off; 1=on)
:velocity: The velocity of the motor, must be between 0 and 4000rpm.
:pumpspeed: This talks to the same registry as velocity but you input it in ml/min, must be between 0 and 400.
:acceleration: The acceleration of the motor, must be in %.
:actualvelocity: The velocity the motor is actually running at.
:address: The address of the motor (default = 1).
:temperature: The temperature of the motor, the mode must be set to 1 in order for this to work.
:errorstatus: The status that the motor can obtain, will raise errors if the motor is not functioning properly. This is defined for each motor differently.
:modbusmactalk: Switching the protocol between 1Mbps Modbus and 19.2kbps MacTalk. At value of 0 the motor waits for Modbus and switches to MacTalk otherwise, at 1 the motor only operates with MacTalk and at 2 the motor only operates with Modbus
:command: Special command used to save in flash, use with care. Protection is built in so it will not allow user to set this to anything by default.

parameters.PARAMETERS = {'acceleration': 6, 'errorstatus': 35, 'command': 211, 'temperature': 16, 'actualvelocity': 12, 'modbusmactalk': 182, 'velocity': 5, 'motormode': 2, 'address': 156}
'''



PARAMETERS = {
              'motormode':      2,
              'velocity':       5,
              'pumpspeed':      5,
              'acceleration':   6,
              'actualvelocity': 12,
              'address':        156,
              'temperature':    16,
              'errorstatus':    35,
              'modbusmactalk':  182,
              'command':        211
                                          }