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

from FellesLab import MasterClass, Temperature, Voltage, Pump, AlicatFlowController, Pressure
from FellesLab import Consentration, Humidity, AlicatPressureController, AlicatLiquidController

def main(GUI=False):

    module1 = Adam4019(base='Dummy')
    module2 = AlicatFMC(base='Dummy', portname='COMport', slaveaddress=1)
    module3 = AlicatFMC(base='Dummy', portname='COMport', slaveaddress=1)
    module4 = AlicatFMC(base='Dummy', portname='COMport', slaveaddress=1)
    module5 = AlicatFMC(base='Dummy', portname='COMport', slaveaddress=1)
#    module3 = Mac050(module1.serial, 1)


    Framework = MasterClass()

    p1 = Pressure(
        resource = module1,
        resource_settings = {'channel': 0,
            'desimals': 0,},
        meta_data = {
            'label' : 'Pressure transmitter: gas feed',
            'unit'  : '[bara]',
            'sample_speed' : 0.5,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): 100*x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'green',
         },
        )

    p2 = Pressure(
        resource = module1,
        resource_settings = {'channel': 1,},
        meta_data = {
            'label' : 'Pressure transmitter: gas product',
            'unit'  : '[bara]',
            'sample_speed' : 0.5,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'green',
         },
        )

    p3 = Pressure(
        resource = module1,
        resource_settings = {'channel': 2,},
        meta_data = {
            'label' : 'Pressure transmitter: water feed',
            'unit'  : '[bara]',
            'sample_speed' : 0.5,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'green',
         },
        )

    p4= Pressure(
        resource = module1,
        resource_settings = {'channel': 3,},
        meta_data = {
            'label' : 'Pressure transmitter: water product',
            'unit'  : '[bara]',
            'sample_speed' : 0.5,
        },
        data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'green',
         },
        )


    c1 = Consentration(
         resource = module1,
         resource_settings = {
            'channel' : 4, # Configure module, set channel etc...
            'decimals' : 1,
         },
         meta_data = {
            'label' : 'CO_2 sensor',
            'unit' : '[%]',
            'sample_speed' : 0.5,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'cyan',
         },
    )

    h1 = Humidity(
        resource = module1,
        resource_settings = {
            'channel' : 5, # Configure module, set channel etc...
            'decimals' : 1,
        },
        meta_data = {
            'label' : 'Humidity sensor',
            'unit' : '[%]',
            'sample_speed' : 0.5,
        },
        data_processing = {
            'signalFiltering' : None, # Noise filter
            'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
            'calibrationCurve' : lambda (x): x, # Calibration curve
        },
        gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'cyan',
        },
    )


    t1 = Temperature(
         resource = module1,
         resource_settings = {
            'channel' : 6, # Configure module, set channel etc...
            'decimals' : 1,
         },
         meta_data = {
            'label' : 'Humidity sensor temperature',
            'unit' : '[Celcius]',
            'sample_speed' : 0.5,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda (x): 10000*x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'blue',
         },
    )

    a1 = AlicatFlowController(
         resource = module3,
         resource_settings = {
            'channel' : 2040, # Configure module, set channel etc...
            'setpoint': 0,
         },
         meta_data = {
            'label' : 'Flow Controller: CO_2',
            'unit' : '[ml/h]',
            'sample_speed' : 0.5,
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

    a2 = AlicatPressureController(
         resource = module4,
         resource_settings = {
            'channel' : 17, # Configure module, set channel etc...
         },
         meta_data = {
            'label' : 'Pressure controller pressure',
            'unit' : '[bar]',
            'sample_speed' : 0.5,
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

    a2 = AlicatLiquidController(
         resource = module4,
         resource_settings = {
            'channel' : 17, # Configure module, set channel etc...
         },
         meta_data = {
            'label' : 'Liquid flow controller',
            'unit' : '[l min^-1]',
            'sample_speed' : 0.5,
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

