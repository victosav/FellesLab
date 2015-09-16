
Experiences from version 0.1 of the software:
---------
** For the next version of the software there are some experiences that need to be documented

* The GUI, the software and the controllers should be operating independently.
* The software should connect to all the controllers and sensors prior to launching the GUI
* The connections should be tested before using them
* For giving set-point in psig to liquid-flow controller settings are done in register 20 in modbus.
* DO NOT TOUCH REGISTER 20 (19)
* Settings to register 20 for psig is 61718 (40020 needs to be 61718)
* Especially for the membrane rig: Messy user interface. Should implement tabs


** Currently for the new distillation rig, the software should be updated