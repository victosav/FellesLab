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
@author:       Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3)
@requires:     Python 2.7.6 or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:

"""

from distutils.core import setup

setup(
    name='FellesLab',
    version='0.01',
    description='Laboratory Framework',
    author='Sigve Karolius',
    url='https//sigveka.github.io/FellesLab',
    packages=['FellesLab','adam_modules','mac_motor', 'alicat_devices'],
    install_requires=["pyserial","minimalmodbus"],
    package_dir={ 'FellesLab':'FellesLab', 'adam_modules':'adam_modules', 'mac_motor':'mac_motor', 'alicat_devices':'alicat_devices'},
    #package_data={'FellesLab': ['Equipment/*.py','GUI/*.py','Utils/*.py'] , 'adam_modules':['utils/*.py']},
    package_data={'FellesLab': [] , 'adam_modules':['utils/*.py']},
    long_description="""\
      FellesLab is a framework for reading information between lab units...
      """,
      classifiers=[
        "License :: GNU General Public License (GPL)"
        "Programming Language :: Python"
        "Development Status :: 0 - Beta"
        "Intended Audience :: Inhouse use"
        "Topic :: Systems engineering"
      ],
      keywords='modbus networking laboratory',
      license='GPL',
)
