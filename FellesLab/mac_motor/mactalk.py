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
This module is mainly an interface to send commands to drive the motor.
It contains the communications definition as well as the individual definitions to operate on different parameters of the motor such as:
mode, velocity, acceleration, address, temperature, errorbits.
Mode, velocity and acceleration can be changed.
Velocity, acceleration, address, temperature and errorbits can be read.
There is also a special function which saves the final settings into the motor memory, so that even if you unplug it, it will still have those settings. This is dangerous though and should be used with care.
'''

import translations
import constants
from parameters import PARAMETERS

class Communications(object):
    def __init__(self, port, address, verbose=False):  
        super(Communications,   self).__init__()

        self.port = port
        self.address = address
        self.PARAMETER = PARAMETERS
        self.verbose = verbose

    def sendmessage(self, hexa, length, read):
        '''
        This definition is used in order to write to and read from the port that is opened
        in this module.

        This definition makes use of specific encoded messages that are made to work on JVL motors.
        Any other use that is effective is sheer coincidence.

        :param hexa: The complete hexadecimal value that should be written to the motor.
        :param length: The length of the bytes that is to be read.
        :param read: This is a boolean that separates the writing to and reading from messages. If True, it will read a registry and return the read value,
                     if False it will return <11><11><11> if the message was received by the motor else will return <><><>.
        '''

        #Connect to the port, must be made as INITIAL
        # if self.port.isOpen()==False:
        #     self.port.open()

        self.port.flushOutput()
        self.port.flushInput()
        if self.verbose: print 'send message', hexa
        message = hexa.decode('hex')
        self.port.write(message)
        data = []


        #Read the data byte per byte and save it in a dict.
        for i in range(length):
            byte = self.port.read()
            data.append(i)
            data[i] = byte.encode('hex')

        #This loop checks if you are reading or writing
        #and acts accordingly
        #self.port.close()
        if read:
            return [data[9],data[11]]

    def write(self, value, address, parameter):
        '''
        Generally, this command generates a HEX message which is then converted to ASCII and send over the
        port line in order to communicate with the motor. The motor will then answer with <11><11><11> if it has
        received an acceptable value.

        :param value: The value you want to write to the parameter of the motor on address.
        :param address: The address of the motor, defined in __init__.
        :param parameter: The parameter you are trying to change of the motor.

        Please note that if you change the port, you have to also change the way you are transmitting and receiving data from the motor.
        '''

        BYTESIZE = 3
        message = translations.createcommand_write(value, address, parameter)
        self.sendmessage(message, BYTESIZE, False)

    def read(self, address, parameter):
        '''
        Asks the motor to give information concerning a parameter,
        if there is a response, the value will be printed otherwise an error will be raised.

        :param address: The address of the motor, defined in __init__.
        :param parameter: The parameter which is being read.
        :raises: Raises if the motor doesn't respond, check the message sent or the connection with the motor.
        '''

        BYTESIZE = 19
        message = translations.createcommand_read(address, parameter)

        values = self.sendmessage(message, BYTESIZE, True)

        if values == None:
            raise ValueError('Values is empty, check connection with motor')

        return values


class Mac050(Communications):
    '''
    This class contains all the definitions that can be summoned in order to change the parameters of a motor.
    It is initialized with the same parameters as for the Communications: Address and port.

    In order to change a different parameter on the motor a new definition needs to be created.
    This should refer to the appropriate parameter and should limit the allowed values.
    '''


    defaultData = {'min_velocity' : 0, # rpm
                   'max_velocity' : 4000, # rpm
                   'min_speed' : 0, # mL/min
                   'max_speed' : 400, # mL/min
                   'min_acceleration' : 0, # %
                   'max_acceleration' : 100, # %
                   }

    # ------------------------------- Method -------------------------------- #    
    def __init__(self,  *args, **kwargs):
        super(Mac050, self).__init__(*args, **kwargs)
        

        self.metaData = {
            'baudrate' : 'asdf',#self.serial.baudrate,
            'bytesize' : 'asdf',#self.serial.bytesize,
            'parity' : 'asdf',#self.serial.parity,
            'timeout' : 'asdf',#self.serial.timeout,
            'channel': None,
            'decimals' : 0,
            'debug' : False,
            'min_velocity' : self.defaultData['min_velocity'],
            'max_velocity' : self.defaultData['max_velocity'],
            'min_speed': self.defaultData['min_speed'],
            'max_speed': self.defaultData['max_speed'],
            'min_acceleration' : self.defaultData['min_acceleration'],
            'max_acceleration' : self.defaultData['min_acceleration'],
            }

    # ------------------------------- Method -------------------------------- #
    def __setitem__(self, key, val):
        """
        Configuration method for changing the following parameters:
          port = str       # serial port name
          baudrate = int   # 9600 (default) or 19200
          bytesize = int   # 8 (default) or 16
          parity   = str   # serial.PARITY_NONE (default)
          stopbits = int   # 1 (default)
          timeout  = float # 0.05 (default)
          address          # this is the slave address number
          mode = str       # minimalmodbus.MODE_RTU,   'rtu' (default) or
                             minimalmodbus.MODE_ASCII, 'ascii' mode

        The method is inked by __init__ when called as:
            xxxModule(portname, slaveaddress, config={ key:val} )
        using the keys listed above.
        """
        self.metaData[key] = val

    # ------------------------------- Method -------------------------------- #
    def __iter__(self):
        return self.metaData.iteritems()

    # ------------------------------- Method -------------------------------- #
    def __getitem__(self, key):
        """
        """
        return self.metaData[key]



    def set_motormode(self, mode, parameter = 'motormode'):
        '''
        :param mode: This value can be 0 or 1; 0 = passive mode, 1 = velocity mode
        '''

        if mode not in (0,1):
            raise ValueError('mode must be 0 or 1')

        else:
            self.write(mode, self.address, self.PARAMETER[parameter])


    def set_velocity(self, rpm, parameter = 'velocity'):
        '''
        :param rpm: rpm set between 0 and 4000

        This sets the velocity the motor should be running on if it is on.

        '''

        pulses = constants.SPPS/constants.RPM*rpm
        if rpm > self['max_velocity'] or rpm < self['min_velocity']:
            raise  ValueError('rpm must be between 0 and 4000')

        else:
            self.write(pulses, self.address, self.PARAMETER[parameter])
            print 'set velocity'

    def set_pumpspeed(self, pumpspeed, parameter = 'velocity'):
        '''
        This sets the speed of a pump in ml/mins.
        :param pumpspeed: The speed at which you want the pump to operate in ml/mins. Cannot exceed 400ml/mins.
        '''

        rpm = constants.RPMMAX/constants.PUMPMAX*pumpspeed
        pulses = constants.SPPS/constants.RPM*rpm
        if pumpspeed <= self['max_speed'] and pumpspeed >= self['min_speed']:
            self.write(pulses, self.address, self.PARAMETER[parameter])

        else:
            raise  ValueError('The speed of the pump must be between 0 and 400ml/mins')

    def set_acceleration(self, perc, parameter = 'acceleration'):
        '''
        :param perc: Sets acceleration in %, the actual rpm/s goes from 0 to 397364
        '''

        acc = constants.SET_ACC/constants.PERC*perc
        pulses = constants.PPSS/constants.ACCEL*acc
        if perc > self['max_acceleration'] or perc < self['min_acceleration']:
            raise ValueError('acceleration is in %, value must be between 0 and 100')
            return 0

        else:
            self.write(pulses, self.address, self.PARAMETER[parameter])

    def get_setvelocity(self, parameter = 'velocity'):
        '''
        reads the velocity that is currently set and returns it in rpm
        '''

        values = self.read(self.address, self.PARAMETER[parameter])

        pulses = translations.hextodec(values)
        rpm = constants.READ_SRPM/constants.RSPPS*pulses
        rpm = translations.rounding(rpm)
        if self.verbose: print 'The velocity is set at ' + str(rpm) + ' rpm'

        return rpm



    def get_actualvelocity(self, parameter = 'actualvelocity'):
        '''
        reads the actual velocity that the motor is running and returns it in rpm, will return 0 if mode is set to 0
        '''

        values = self.read(self.address, self.PARAMETER[parameter])

        pulses = translations.hextodec(values)
        rpm = constants.READ_ARPM/constants.RAPPS*pulses

        rpm = translations.rounding(rpm)

        if self.verbose:
            if rpm == 0:
                print 'The motor is running at ' + str(rpm) + ' rpm, make sure the motor is on'

            else:
                print 'The motor is running at ' + str(rpm) + ' rpm'

        return rpm



    def get_acceleration(self, parameter = 'acceleration'):
        '''
        Reads acceleration and returns the value in rpm/s
        '''

        values = self.read(self.address, self.PARAMETER[parameter])


        pulses = translations.hextodec(values)
        acc = constants.READ_ACC/constants.READ_PPSS*pulses
        acc = translations.rounding(acc)

        if self.verbose: print 'The acceleration is set at ' + str(acc) + ' rpm/s'

        return acc

    def get_address(self, parameter = 'address'):
        '''
        Reads the address of the motor and returns it
        '''

        values = self.read(self.address, self.PARAMETER[parameter])
        address = translations.hextodec(values)
        if self.verbose: print 'The address of the motor is ' + str(address)

        return address

    def get_temperature(self, parameter = 'temperature'):
        '''
        Reads the temperature in degrees Celcius and returns it, will give 0 if mode is set to 0
        '''

        values = self.read(self.address, self.PARAMETER[parameter])
        temp = translations.hextodec(values)

        if self.verbose:
            if temp == 0:
                print 'Please turn the motor on before attempting to measure the temperature.'
            else:
                print 'The Temperature of the motor is ' + str(temp) +' degrees Celcius'

        return temp

    def get_errorstatus(self, parameter = 'errorstatus'):
        '''
        Returns bits which express what the status of the motor is.
        If this returns a non-zero value, you may not be able to change any motor settings depending on the error.
        Depending on the value returned, this may be state of the motor:

        :param Bit0: Overload
        :param Bit1: Follow Error
        :param Bit2: Function Error
        :param Bit3: Regenerative overload
        :param Bit4: In position
        :param Bit5: Accelerating
        :param Bit6: Decelerating
        :param Bit7: Position limits error
        :param Bit11: Motor current too high
        :param Bit12: Supply undervoltage
        :param Bit16: SII Read error

        The mode must be set to 1 before reading any errorbits, otherwise returns 0.

        More details on the errordict is given in the 'Translations' module in the 'Library' section at the 'checkforerrors' definition.
        '''

        errordict = {'Bit 0' : 2**0,
                     'Bit 1' : 2**1,
                     'Bit 2' : 2**2,
                     'Bit 3' : 2**3,
                     'Bit 4' : 2**4,
                     'Bit 5' : 2**5,
                     'Bit 6' : 2**6,
                     'Bit 7' : 2**7,
                     'Bit 8' : 2**8,
                     'Bit 9' : 2**9,
                     'Bit 10' : 2**10,
                     'Bit 11' : 2**11,
                     'Bit 12' : 2**12,
                     'Bit 13' : 2**13,
                     'Bit 14' : 2**14,
                     'Bit 15' : 2**15,
                     'Bit 16' : 2**16,
                     }

        BITS = 16
        hexa = self.read(self.address, self.PARAMETER[parameter])
        error = translations.hextodec(hexa)

        if error != 0:
            bina = translations.dectobin(error,BITS)
            translations.checkforerrors(errordict, bina)

        else:
            if self.verbose: print 'If the mode is set to 1, there is an error in Bit 0'

    def save_and_reset(self, value, parameter = 'command'):
        '''
        Saves current settings in the motor memory, use this only if you know what you are doing.
        After first message is sent, it returns <11><11><11>
        After second message is sent, it returns <><><>
        This means save and reset has worked.
        '''

        if value == 2:
            #write motor into safe mode first
            self.write(15, self.address, self.PARAMETER['motormode'])
            while True:
                a = raw_input('You are about to save in flash, are you sure? (y/n)')
                if a == 'y':
                    #actual save command
                    self.write(value, self.address, self.PARAMETER[parameter])
                    print 'Saved and Reset'
                    break
                elif a == 'n':
                    print 'The motor did not save'
                    break
                else:
                    print 'I did not understand'
        else:
            raise ValueError('You are using the command parameter in the wrong way, please make sure you know what you are trying to do.')

    def get_info(self, address, register):

        command = '50'*3 + format(address,'02X') + format(address^255,'02X') + format(register,'02X') + format(register^255,'02X') + 'AA'*2
        if self.verbose: print 'command ',command

        message = command.decode('hex')
#         print 'return', self.sendmessage(message, 3, True)
        self.port.write(message)

        self.unpackRequestedResponse()

    def unpackRequestedResponse(self):

        message = []

        for i in range(30):
            byte = self.port.read()
            _a1 = byte.encode('hex')
            print 'read byte:' ,_a1
            if _a1 == '52':
                byte = self.port.read()
                _a2 = byte.encode('hex')
                print 'first start byte:' ,_a2
                if _a2 == '52':
                    byte = self.port.read()
                    _b = byte.encode('hex')
                    print 'second start byte:' ,_b
                    if _a2 == '52':
                        print 'third start byte:' ,_b
                        break

        for i in range(30):
            byte = self.port.read()
            _b = byte.encode('hex')
            if _b == 'aa':
                print ' first end byte: ',_b
                byte = self.port.read()
                _e2 = byte.encode('hex')
                if _e2 == 'aa':
                    print 'second end byte: ',_e2
                    break
            else:
                print 'message byte:' ,_b
                message.append(_b)


        print 'get_info', message

        # bytes 0,1 are always 00 ff (manual 5.11)
        # bytes 2,3 is the address of the register
        _address = int(str(message[2]),16)
        _baddress = int(str(message[3]),16)^255
        print 'address: ', _address , _baddress
        # byte 4 is the length -- always 4
        # byte 5 is FB
        # reminder is the data
        # bytes are protected meaning each is repeated in reverse from (currently not checked)
        # bytes come first high byte then low byte so order must be reversed
        # it is assumed that it is always 4 bytes to be converted and that 2 byte words are padded with zeros
        # thus we convert always with basis 32
        data = ''
        print 'range:',range((len(message)-1),5,-2)
        for i in range((len(message)-2),5,-2):
            print 'i: ',i
            data += message[i]
        print 'data: ', data
        result = int(str(data),32)
        print 'data: ',data, result
        return result

