**Note:** The repository uses a ".gitinclude" file, **not** gitignore, i.e. all files are ignored by default.

```
       .O
      o .
    aaaaaaa
    "8.o 8"
     8. O8
     8 o.8     ooooooooo      ooo ooo                  oooo             .o8
  ,adPO .Yba,  `88'   `8      `88 `88                  `88'            "888
 dP". O  o "Yb  88     .oooo.  88  88  .oooo.  .oooo.o  88      .ooo.  888ooo.
dP' O . o .O`Yb 88oo8 d88'`88b 88  88 d88'`88b d8(  "8  88     `P  )8b d88'`88b
8^^^^^^^^^^^^^8 88  " 888oo888 88  88 888oo888` "Y8b.   88      .oP"88 888  888
Yb,         ,dP 88    888   .o 88  88 888   .oo.  )88b  88    od8(  88 888  888
 "Ya,_____,aP" o88o   `Y8bd8P'o88oo88o`Y8bd8P'8""888P' o88oood8`Y88""8o`Y8od8P'
   `"""""""'


      Python framework for sensor connections and GUI for the "Felles Lab".


                             Sigve Karolius

                   Department of Chemical Engineering
             Norwegian University of Science and Technology

                                .            .
                               / \          / \
                              /   \   /\   /   \
                              |   |  /  \  |   |
                       .______|   |_/    \_|   |______.
                     _/                                \_
          /\        |                                    |        /\
    _____/  \  _____|                                    |_____  /  \_____
             \/                                                \/

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
sudo pip install -U pyserial, minimalmodbus, matplotlib, wxmplot
```

