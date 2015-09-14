# -*- coding: ascii -*-
"""

oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Felles lab GUI graphics parent classes
@author:       Arne Tobias Elve
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3)
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:

Colors:
b: blue
g: green
r: red
c: cyan
m: magenta
y: yellow
k: black
w: white
"""

__author__  = "Arne Tobias Elve"
__email__   = "elve@stud.ntnu.no"
__license__ = "GPL.v3"
__date__    = "$Date: 2015-08-26 (Wed, 28 Aug 2015) $"

from adam_modules import Adam4019
from mac_motor import Mac050
from alicat_devices import AlicatFMC
import minimalmodbus
import math

from FellesLab import MasterClass, Temperature, Voltage, Pump, AlicatFlowController, Pressure
from FellesLab import Consentration, Humidity, AlicatPressureController, AlicatLiquidController

def main(GUI=False):
    portName = '/dev/ttyUSB0'
    adamModule = Adam4019(portname=portName, slaveaddress=4)
    upperLeftAlicatGMFC = AlicatFMC(portname=portName, slaveaddress=17)
    lowerLeftAlicatGMFC = AlicatFMC(portname=portName, slaveaddress=21)
    upperRightAlicatBPC = AlicatFMC(portname=portName, slaveaddress=29)
    lowerRightAlicatLMFC = AlicatFMC(portname=portName, slaveaddress=23)
    
    Framework = MasterClass()

    

    p1 = Pressure(
        resource = adamModule,
        resource_settings = {
            'channel': 0,
            'decimals' : 0,
        },
        meta_data = {
            'label' : 'Pressure transmitter: gas feed',
            'unit'  : '[psi]',
            'sample_speed' : 1,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): (1.0/280.34)*x-121.7, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'green',
         },
        )

    p2 = Pressure(
        resource = adamModule,
        resource_settings = {
            'channel': 1,
            'decimals' : 0,
        },
        meta_data = {
            'label' : 'Pressure transmitter: gas product',
            'unit'  : '[psi]',
            'sample_speed' : 1,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): (1.0/280.34)*x-121.7, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'red',
         },
        )

    p3= Pressure(
        resource = adamModule,
        resource_settings = {
            'channel': 2,
            'decimals' : 0,
        },
        meta_data = {
            'label' : 'Pressure transmitter: water feed',
            'unit'  : '[psi]',
            'sample_speed' : 1,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): (1.0/280.34)*x-121.7, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'blue',
         },
        )

    p4= Pressure(
        resource = adamModule,
        resource_settings = {
            'channel': 3,
            'decimals' : 0,
        },
        meta_data = {
            'label' : 'Pressure transmitter: water product',
            'unit'  : '[psi]',
            'sample_speed' : 1,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): (1.0/280.34)*x-121.7, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'black',
         },
        )


    c1 = Consentration(
         resource = adamModule,
         resource_settings = {
            'channel' : 4, # Configure module, set channel etc...
            'decimals' : 0,
         },
         meta_data = {
            'label' : 'CO_2 sensor',
            'unit' : '[%]',
            'sample_speed' : 1,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): 1.0/6112 * x - 5.6451243, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'cyan',
         },
    )

    h1 = Humidity(
        resource = adamModule,
        resource_settings = {
            'channel' : 5, # Configure module, set channel etc...
            'decimals' : 0,
        },
        meta_data = {
            'label' : 'Humidity sensor',
            'unit' : '[%]',
            'sample_speed' : 1,
        },
        data_processing = {
            'signalFiltering' : None, # Noise filter
            'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
            'calibrationCurve' : lambda (x): (8.0/503.0)*x-34335*(8.0/503.0), # Calibration curve
        },
        gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'cyan',
        },
    )

    t1 = Temperature(
         resource = adamModule,
         resource_settings = {
            'channel' : 0, # Configure module, set channel etc...
            'decimals' : 0,
         },
         meta_data = {
            'label' : 'Humidity sensor temperature',
            'unit' : '[Celcius]',
            'sample_speed' : 1,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): (0.724/48.0)*x-(0.724/48.0)*37726, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'blue',
         },
    )

    gmfc1 = AlicatFlowController(
         resource = upperLeftAlicatGMFC,
         resource_settings = {
            'channel' : 2044, # Configure module, set channel etc...
         },
         meta_data = {
            'label' : 'Flow Controller: N2',
            'unit' : '[l/min]',
            'sample_speed' : 1,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourier(?), Laplace(?)
             'calibrationCurve' : lambda (x): x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'black',
         },
         )

    



    gmfc2 = AlicatFlowController(
         resource = lowerLeftAlicatGMFC,
         resource_settings = {
            'channel' : 2044, # Configure module, set channel etc...
         },
         meta_data = {
            'label' : 'Flow Controller: CO_2',
            'unit' : '[l/min]',
            'sample_speed' : 1,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourier(?), Laplace(?)
             'calibrationCurve' : lambda (x): x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'black',
         },
         )


    bpc = AlicatPressureController(
         resource = upperRightAlicatBPC,
         resource_settings = {
            'channel' : 2040, # Configure module, set channel etc...
         },
         meta_data = {
            'label' : 'Pressure controller',
            'unit' : '[bara]',
            'sample_speed' : 1,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourier(?), Laplace(?)
             'calibrationCurve' : None, # Calibration curve
         },
         gui_configuration = {
            'plot' : False,
            'time_span' : 20, # seconds
            'color': 'black',
         },
         )

    lmfc = AlicatLiquidController(
         resource = lowerRightAlicatLMFC,
         resource_settings = {
            'channel' : 2040, # Configure module, set channel etc...
         },
         meta_data = {
            'label' : 'Flow Liqid Controller',
            'unit' : '[l/min]',
            'sample_speed' : 1,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourier(?), Laplace(?)
             'calibrationCurve' : lambda (x): x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'black',
         },
         )

    if GUI:
        Framework.InitGUI()

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == "__main__":
    main(True)

