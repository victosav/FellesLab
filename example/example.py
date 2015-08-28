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
@author:       Sigve Karolius
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

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__    = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

from adam_modules import Adam4019
from mac_motor import Mac050
from alicat_devices import AlicatFMC

from FellesLab import MasterClass, Temperature, Voltage, Pump, AlicatFlowController

def main(GUI=False):

    module1 = Adam4019(base='Dummy')
    module2 = Adam4019(base='Dummy')
    module3 = AlicatFMC(base='Dummy', portname='COMport', slaveaddress=1)
#    module3 = Mac050(module1.serial, 1)


    Framework = MasterClass()

#    b = Pump(
#          module = module3,
#          meta_data = {
#             'label' : 'Pump',
#             'unit' : '[rpm]',
#             'sample_speed' : 0.5,
#          },
#          data_processing = {
#              'signalFiltering' : None, # Noise filter
#              'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
#              'calibrationCurve' : lambda (x): x, # Calibration curve
#          },
#          gui_configuration = {
#             'plot' : False,
#             'time_span' : 20, # seconds
#             'color': 'red',
#            },
#     )

    a1 = AlicatFlowController(
         resource = module3,
         resource_settings = {
            'channel' : 17, # Configure module, set channel etc...
         },
         meta_data = {
            'label' : 'Flow Controller: Permeate',
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
            'color': 'cyan',
         },
         )

    v1 = Voltage(
         resource = module1,
         resource_settings = {
            'channel' : 3, # Configure module, set channel etc...
            'decimals' : 3,
         },
         meta_data = {
            'label' : 'Temperature 1',
            'unit' : '[K]',
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

    v2 = Voltage(
         resource = module2,
         resource_settings = {
            'channel' : 3, # Configure module, set channel etc...
            'decimals' : 2,
         },
         meta_data = {
            'label' : 'Temperature 2',
            'unit' : '[K]',
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
            'color': 'magenta',
         },
    )

    t2 = Temperature(
         resource = module1,
         resource_settings = {
            'channel' : 3, # Configure module, set channel etc...
            'decimals' : 1,
         },
         meta_data = {
            'label' : 'Temperature 1',
            'unit' : '[K]',
            'sample_speed' : 0.1,
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

    if GUI:
        Framework.InitGUI()

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == "__main__":
    main(True)

