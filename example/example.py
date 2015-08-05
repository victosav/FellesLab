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

"""

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__    = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

from adam_modules import Adam4019
from mac_motor_module import Mac050

from FellesLab import MasterClass, Temperature, Pump



def main(GUI=False):

    module1 = Adam4019(base='Dummy')
    module2 = Adam4019(base='Dummy')
#   module3 = Mac050(module1.serial, 1)


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

    t1 = Temperature(
         module = module1,
         module_metadata = {
            'channel' : 3, # Configure module, set channel etc...
            'decimals' : 1,
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
            'color': 'red',
         },
    )

    t2 = Temperature(
         module = module2,
         module_metadata = {
            'channel' : 3, # Configure module, set channel etc...
            'decimals' : 1,
         },
         meta_data = {
            'label' : 'Temperature 2',
            'unit' : '[K]',
            'sample_speed' : 0.5,
         },
         data_processing = {
             'signalFiltering' : None, # Noise filter
             'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
             'calibrationCurve' : lambda x: x, # Calibration curve
         },
         gui_configuration = {
            'plot' : True,
            'time_span' : 20, # seconds
            'color': 'blue',
         },
    )

    if GUI:
        Framework.InitGUI()

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == "__main__":
    main(True)

