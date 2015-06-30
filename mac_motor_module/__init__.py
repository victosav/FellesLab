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

from mactalk import Mac050
import translations

class SetupMotor():

    def __init__(self, port, motor_found = False, setup = True):
        '''
        This class initializes the communications interface with a motor.
        
        First, it searches which motors are connected and adds a number to each motor in order of rising address starting from 1.
        
        Next, it asks you which of the motors you wish to setup a connection with in order to be able to send commands to. The value that is set to the motors needs to be added here.

        :param port: The port that is communicated with from the ProcessInterface, the interface that you are using in order to send messages to the motor.
        :param motor: This is the connected motor which you wish to use, multiple motors can be connected as long as the addresses are different for each motor. 
        '''
        
        self.port = port 
        self.motor_found = self.__findMotor(motor_found)
        if not self.motor_found:
            print 'No motor connected. You can still operate the Adam module.'
        addr = 1
        self.Motor = []
        self.Motor.append(Mac050(self.port, addr))
        

#         try:
#             while self.motor_found == True:
#                 while setup:
#                     addr = raw_input('What is the address of the motor you wish to setup? (write any string to exit) ')
#                     if addr == 'q':
#                         self.motor_found = False
#                         setup = False
#                     elif int(addr) == self.addr['motor']:
#                         self.Motor.append(Mac050(self.port, int(addr)))
#                         print 'Motor on address ' + addr + ' is ready to use.'
#                     else:
#                         print 'The address ' + addr + ' does not belong to any motor.'
#         except:
#             pass
#                 
#         print self.Motor
            

                
    
    def __findMotor(self, start =0, end=10, found = False):
        '''
        Scans to see if a motor is connected and to which address.
        
        Writes the same message to different addresses, if it receives a reply it returns True.
        
        It also saves the address every time a motor is found in a list and each address can be summoned with
        a definition found below.        
        '''
        
        BYTESIZE = 19
        ADDRESREGISTER = 156
#         MOTOR_TYPE=153
#         SERIAL_NBR = 154
        data = []
        self.addr = dict()
        if self.port.isOpen()==False:
            self.port.open()
        try: 
            for j in range(start,end):
            
                address = translations.createcommand_read(j, ADDRESREGISTER) #ADDRESREGISTER)# SERIAL_NBR) #MOTOR_TYPE)#)
                self.port.write(address.decode('hex'))
                for k in range(BYTESIZE):
                    byte = self.port.read()     
                    data.append(k)
                    data[k] = byte.encode('hex')
                try:
                    values = [data[9],data[11]]
                    decim = translations.hextodec(values)
                    if decim == 1:
                        found = True
                        if 'motor' in self.addr:
                            self.addr.append(j)
                        else:
                            self.addr['motor'] = j
                    print 'Motor found on address ' + str(j)+ ' decim: %s'%decim, ' values: %s'%values
                except:
                    print 'No motor on address ' + str(j)
        finally:
            self.port.close()
            return found
