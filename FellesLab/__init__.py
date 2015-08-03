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
@license:      Free (GPL.v3), although credit is appreciated
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:

"""
import os

from Equipment import Equipment, Pump
from Sensors import Sensor, Temperature, Voltage, SensorFrame
from Controllers import Controller
from FellesBase import FellesBaseClass
from GUI import FellesApp, FellesButton, FellesFrame, FellesLabel, FellesTextInput
from SupportClasses import ExtendedRef, GuiUpdater, FellesSampler, DataStorage
from SupportFunctions import timeStamp, findSensor, sensorTypes, dayStamp

from subprocess import call
import csv
import itertools as it

FILE_PATH = '%s/Desktop/'%(os.path.expanduser("~"))

from time import time

BACKUP_README = \
'''
# Welcome to the FellesLab "backup system"

This document briefly describes how the output from an experiment is saved, and how a backup may be created.
Please note that this is not a sophisticated backup system.
The output is file saved on the desktop and a backup file is created as long as the student pushes "Stop Sampling".
In the event that the user "closes" the program using the "`X`" button, a backup is **not** created.
Let us say that together, "If I do not push the Stop Sampling button I will not have a backup. When this happens there is **no** way of retrieving the data and I will not receive any sympathy from the software developer."

**Note:**

*The entire "backup directory" can be deleted when the lab is completed.* All sub-directories and files are created **automatically** (yes, that includes "FellesLab_Backup").

---
    oooooooooooo       oooo oooo                    ooooo                 .o8
    `888'     `8       `888 `888                    `888'                "888
     888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
     888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
     888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
     888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
    o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'

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
---

# Conventions

* **File names:** The file names are generated automatically using the following convention: `Day_Month_Num_HourMinSecond_Year`, e.g. `Sun_Aug_2_221728_2015.csv`.

* **Directory names:** The directories are created automatically as: `Day_Num_Month_Year`, e.g. `Sun_2_Aug_2015`.

* **File format:** The data is saved in a tabular [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format.

* **Data storage format:**  The following example shows how two sensors _Rnd_ and _Rand 2_ both have a _time_ column associated with them. Please note (and appreciate) that even though every sensor has a individual time column, the reference time is identical.  
```FILE.csv
    time, Rnd, time, Rand 2  
    0.000006 , 0.631032, 0.000002 , 0.124725  
    0.001157 , 0.992647, 0.328444 , 0.293643  
    0.104696 , 0.711614, 0.830970 , 0.643257  
    0.207081 , 0.108123, 1.334370 , 0.354398  
    0.309923 , 0.518604, NA , NA  
    0.411372 , 0.809855, NA , NA  
    0.512407 , 0.558416, NA , NA  
    0.613994 , 0.660687, NA , NA  
```
* **Data _Not Available_:** When data is *not available* the string **NA** is used. This is the convention for to denote missing data in the **R** programming language. Consequently, this makes importing/plotting data remarkably simple.

* **Data processing example in R:** The file above can be plotted (and saved as a png) using **R** using very few lines:  

```R  
    csvFile = read.csv('path/to/FILE.csv', header=True) # Read file
    
    png(filename='path/to/FILE.png', width = 480, height = 480) # Save as png
    
    plot(csvFile$time, csvFile$Rnd, col="magenta", xlab="time", ylab="Random number", frame=FALSE, pch=1) # Create plot canvas
    points(csvFile$Time.1, csvFile$Rand.2, col="cyan", pch=19) # Add second plot to canvas
    legend("topleft", c("Rnd","Random"), pch=c(1,19), lty=c(NA,NA), col=c("magenta", "cyan"), bty="n") # Legend
    dev.off() # Produce plot output
    
    summary(csvFile) # Take a look at a statistical summary
```  
'''
# ================================ Class ==================================== #
class MasterClass(object):
    """
    This class is intended to keep track over objects 
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self):
        """
        """
        super(MasterClass, self).__init__()

    # ------------------------------- Method -------------------------------- #
    def InitialisationProcedure(self):
        """
        """
        print "Welcome to the FellesLab!"

    # ------------------------------- Method -------------------------------- #
    def TerminationProcedure(self):
        """
        """
        # Get data from sensors and equipment and write to file
        # Create backup
        print "Saving data and exiting..."

    # ------------------------------- Method -------------------------------- #
    def InitGUI(self):
        """
        TODO: Write a "window configuration file" such that the windows can be
              opened in the position they where closed before.
              
              This means that "FellesApp" needs a method for saving the window
              positions as well...
        """
        self.app = FellesApp(self)
        self.gui = {}
        for cls in FellesBaseClass.___refs___:
            if not self.gui.has_key( cls().__class__.__base__.__name__ ):
                print "Creating GUI frame for '%s'" %cls().__class__.__base__.__name__
                self.gui[cls().__class__.__base__.__name__] = cls().InitGUI()
        
        print "The following GUIs have been created: %s" %self.gui
        self.app.MainLoop()

    # ------------------------------- Method -------------------------------- #
    def StartSampling(self):
        """
        TODO: Can this be more clever?
        """
        self.T = time() # Reference time, is used in SaveData
        for cls in FellesBaseClass.___refs___:
            cls().StartSampling(self)
        print "Start Sampling"

    # ------------------------------- Method -------------------------------- #
    def PauseSampling(self):
        """
        TODO: Write
        """
        pass
    # ------------------------------- Method -------------------------------- #
    def StopSampling(self, sensor=None):
        """        
        * Gather ALL DataStorage objects and save the results in a file
        """
        Sensor.SAVE = False
        Equipment.SAVE = False

        for cls in FellesBaseClass.___refs___:
            cls().StopSampling(self)

        self.SaveData()
        print "Stop Sampling"

    # ------------------------------- Method -------------------------------- #
    def SaveData(self):
        """
        """
        # Check if the backup directory exists
        backup_dir = FILE_PATH + "FellesLab_Backup"
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)
            with open( backup_dir + "/README", 'w') as f:
                f.write(BACKUP_README)
            
            #cmd = "python -m markdown {dir}/README > {dir}/README.html".format(dir=backup_dir)
            #call([cmd])
        # Check if the Backup directory has a directory for "today"
        day = FILE_PATH + "FellesLab_Backup/" + dayStamp()
        if not os.path.isdir(day):
            os.mkdir(day)

        # Save data for all the sensors
        # TODO: Rewrite, difficult to follow...
        DATA = [ ] # This will become a list of lists, e.g.  
                   # [ [time, ...], [Temp1, ...], [time, ...], [Temp2, ...] ]
        for cls in FellesBaseClass.___refs___:
            dt = self.T - cls().t0 # Ensure that the time stamps are adjusted to the same reference.

            cls().data.File.seek(0) # Rewind file pointer

            F = csv.reader(cls().data.File, delimiter=',', quotechar='|')
            r = [[],[]]
            for row in F:
                for i,num in enumerate(row):
                    r[i].append(num)
                    if i > 1:
                        r[i].append(float(num) - dt )
            
            for j in r:
                DATA.append(j)
            cls().data.File.close()
        
        # Finally, write data file.
        with open( day + "/" + timeStamp() + '.csv', 'w') as f:
            csv.writer(f).writerows( it.izip_longest(*DATA, fillvalue='NA') )
