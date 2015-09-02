
# encoding: utf-8



from PyQt4 import QtGui, QtCore
# from PyQt4 import QtCore
from alicatPressureController import Ui_MainWindow

# from Debugging import message_logging
# from ui_ontology_design import Ui_MainWindow
# from variable_framework import VariableSpace, Units 
# from store_config_file import StoreAsConfigurationFiles
# from ui_physvar_impl import UI_PhysVarDialog
# from ui_equations_impl import UI_Equations
# from resources import EMPTY_EQ, NEW_EQ

# class PressureController(QMainWindow):
#     '''
#     Main window for the ontology design:
#     '''


#     def __init__(self):
#         '''
#         The editor has the structure of a wizard, thus goes through several steps to define the ontology.
#         - get the base ontology that provides the bootstrap procedure. 
#         - construct the index sets that are used in the definition of the different mathematical objects
#         - start building the ontology by defining the state variables
#         '''

#         # set up dialog window with new title
#         QMainWindow.__init__(self)
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.setWindowTitle('Alicat pressure controller')
  

if __name__ == "__main__":
    import sys
    a = QtGui.QApplication(sys.argv)
    # QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Ui_MainWindow()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
    
        
