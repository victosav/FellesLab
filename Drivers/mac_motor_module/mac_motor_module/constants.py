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
This is a module containing all the constants used in the file MacTalk.py.
These constants are determined on the basis of a calibration done on the motor.
They need to be adapted depending on the type of motor you use.

Write to velocity constants, the value to write is in RPM.

:SPPS: 2097; SET_PULSE_PER_SAMPLE, the amount of pulses per 1000rpm
:RPM: Chosen at 1000rpm


Write to acceleration constants, the value to write is in %.

:SET_ACC: 397364; the max set acceleration, defined by the motor
:PERC: Percentage chosen at 100%
:PPSS: PULSE_PER_SAMPLE_SAMPLE, the amount of pulses chosen at 50
:ACCEL: 12418; The acceleration that is found at 50PPSS


Read from velocity constants, the value read is in RPM.

:READ_SRPM: READ_SET_RPM, chosen at 1000 rpm
:RSPPS: 2097; READ_PULSE_PER_SAMPLE, the amount of pulses per 1000 rpm


Read from actual velocity, the value read is in RPM.

:READ_ARPM: READ_ACTUAL_RPM, chosen at 1000rpm
:RAPPS: 131.43; READ_ACTUAL_PULSE_PER_SAMPLE, the pulse per sample that is found at 1000rpm. The 2 decimals after the comma are to ensure a more accurate reading.


Read from acceleration, the acceleration returned is in RPM/s.

:READ_ACC: 12418; Acceleration that is found at 50PPSS
:READ_PPSS: READ_PULSE_PER_SAMPLE_SAMPLE, chosen at 50PPSS
'''

SPPS = 2097     
RPM = float(1000)  

RPMMAX = 4000
PUMPMAX = float(400)

SET_ACC = 397364              
PERC = float(100)               
PPSS = 50          
ACCEL = float(12418)            

READ_SRPM = 1000         
RSPPS = float(2097)      

READ_ARPM = 1000            
RAPPS = float(131.43)       

READ_ACC = 12418            
READ_PPSS = float(50)       
        
