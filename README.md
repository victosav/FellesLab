**Note:** The repository uses a ".gitinclude" file, **not** gitignore, i.e. all files are ignored by default.

```
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
 o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


      Python framework for sensor connections and GUI for the "Felles Lab".


                             Sigve Karolius

                   Department of Chemical Engineering
             Norwegian University of Science and Technology

                             .            .
                            / \          / \
                           /   \   /\   /   \
                   /\      |   |  /  \  |   |        /\
           _______/  \  ___|   |_/    \_|   |_____  /  \_____
                      \/                          \/
```

**Currently under development, repository is for the moment only for convenience. Future versions will be stored as a Python module**

Contains:
---------
* Drivers for (advantec) Adam modules
* Drivers for Pump Motors
* Standardised classes for various sensor types and equipment
* GUI framework

Requires:
---------
* Python v.2.7.6+ ( **NOT** Python 3)
* wxPython
* minimalmodbus

Install procedure (Ubuntu):
---------------------------

```{.bash}
sudo apt-get python-pip 
```

```{.bash}
sudo pip install minimalmodbus
```

