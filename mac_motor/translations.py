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

from string import maketrans    

'''
Mathematical Definitions
'''

global writeseq, readseq, write, read, endseq, end

writeseq = '<52>'*3
readseq = '<50>'*3
write = '52'*3
read = '50'*3
endseq = '<AA>'*2
end = 'AA'*2
    
def createlist(value, x):
    '''
    This definition creates a list from a string taking every x letters together 
    and defining it as one element in the list and this is done over the entire string.
    
    This is mainly done to separate hexa and hexa_reverse so that each can be called separately.
    
    :param value: Is the string or integer that needs to be split up
    :param x: Is the amount in value per step that is taken
    '''
    r = [value[i:i+x] for i in range(0, len(value), x)]
    return r

def trunc(flo, n):
    '''Truncates/pads a float to n decimal places without rounding'''
    if flo == 0:
        flo = '0'        
        return flo
    else:
        slen = len('%.*f' % (n, flo))
        return str(flo)[:slen]
    
def rounding(value):
    ''' Rounds the value that is given to a more understanding answer'''
    value = str(trunc(value,1))
    valuelength = len(value)-1
    if int(value[valuelength]) < 5:
        value = trunc(float(value),0)        
    else:
        value = int(float(value)) + 1
        value = trunc(float(value),0)
    return value

def hex_hexinverse(decimal):
    '''
    Calculation to create hex and hex_inverse to be used in the message sent
    '''
    #Calculation of Hex
    hexa = hex(int(decimal)).lstrip('0x')    
    hexalist = createlist(hexa, 1)
    if hexa == '':
        hexa = '00'
    elif len(hexalist)%2 ==0: 
        hexa = hexa
    else: 
        hexa = '0' + hexa
        
    #Calculation of binary
    hexlength = len(hexa)*4
    bina = bin(int(hexa, 16))[2:].zfill(hexlength)
    
    #Calculation of binary reversed
    reverse = bina.translate(maketrans("10","01"))
    
    #Calculation of hexreverse
    hexa_inverse = hex(int(reverse,2)).lstrip('0x').upper()  
    hexa = hexa.upper()
    return [hexa, hexa_inverse]

def hextodec(hexa):
    '''
    Translation from Hex to decimals for the Read command
    '''
    hexaa = hexa[1]+hexa[0]
    decimal = int(str(hexaa), 16)
    return decimal
    
def dectobin(dec,x):
    '''
    Translation from decimals to x bits of binary code. This is specifically used for the errorstatus.
    '''
    bina = bin(dec)[2:].zfill(x)
    return bina

'''
Hexadecimal message definitions

These commands allow the sending sequence to be returned in order to be sent through the port to the
motor.
'''

def createcommand_write(value, address, channel):
    '''
    This definition is specifically used to return a message in order to change parameters of the motor.
    
    :param value: The value that the channel is to be changed to on the motor.
    :param address: The address of the motor that is communicated with.
    :param channel: The channel that is linked to the parameter which is being changed, also known as registry number.
    '''
    hexa = hex_hexinverse(value)  
    channel = hex_hexinverse(channel)
    address = hex_hexinverse(address)
    
    hexlength = len(hexa[0])
    if hexlength == 2:
        code = writeseq + '<%s><%s><%s><%s><02><FD><%s><%s><00><FF>'%(address[0], address[1], 
                                                                      channel[0],channel[1], 
                                                                      hexa[0], hexa[1]) + endseq
                                                                    
        hexa = write + '%s%s%s%s02FD%s%s00FF'%(address[0],address[1], 
                                               channel[0],channel[1], 
                                               hexa[0], hexa[1]) + end
        return hexa
        
    elif hexlength == 4:
        asplit = createlist(hexa[0],2)
        bsplit = createlist(hexa[1],2)
       
        code = writeseq + '<%s><%s><%s><%s><02><FD><%s><%s><%s><%s>'%(address[0], address[1], 
                                                                      channel[0],channel[1],
                                                                      asplit[1], bsplit[1], 
                                                                      asplit[0], bsplit[0]) + endseq
                                                                    
        hexa = write + '%s%s%s%s02FD%s%s%s%s'%(address[0], address[1], 
                                               channel[0],channel[1],
                                               asplit[1], bsplit[1], 
                                               asplit[0], bsplit[0]) + end
        return hexa
    else:
        print 'The length of the hexadecimal is not 2 or 4'  

def createcommand_read(address, channel):
    '''
    This definition is specifically used to return a message in order to read parameter values 
    from the motor.
    
    :param address: The address of the motor that is being read.
    :param channel: The channel that is linked to the parameter which is being read, also known as registry number.
    '''
    channel = hex_hexinverse(channel)
    address = hex_hexinverse(address)
    
    code = readseq + '<%s><%s><%s><%s>'%(address[0], address[1], 
                                         channel[0], channel[1]) + endseq
                                         
    hexa = read + '%s%s%s%s'%(address[0], address[1], 
                              channel[0], channel[1]) + end
    return hexa

def checkforerrors(errordict, error):
    '''
    This definition checks which errorbits are returned and provides the appropriate message for that status.
    
    :param errordict: This is a dictionary which contains all the errorbits of the motor. It is different for every motor and should be changed as such.
    The messages provided in this definition should therefore also correspond to the correct errorbits.
    :param error: The bit value that is read from the motor in binary code.
    '''
    
    MAX = 15
    errlist = createlist(error,1)
    
    for i in range(len(errlist)):
        if errlist[i] == '1':
            if errordict['Bit ' + str(MAX-i)] == errordict['Bit 4']:
                print 'The motor is in position'
            elif errordict['Bit ' + str(MAX-i)] == errordict['Bit 5']:
                print 'The motor is accelerating'
            elif errordict['Bit ' + str(MAX-i)] == errordict['Bit 6']:
                print 'The motor is decelerating'
            else:
                raise 'There is an error in Bit ' + str(MAX-i)
