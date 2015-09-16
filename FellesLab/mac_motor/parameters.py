# -*- coding: ascii -*-
"""

oooooooooooo       oooo oooo                    ooooo                 .o8      
`888'     `8       `888 `888                    `888'                "888      
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo. 
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      TODO
@author:       TODO
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      TODO
@license:      Free (GPL.v3), although credit is appreciated  
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:     
@change:       
@note:         

"""

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
