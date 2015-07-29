

class FellesEquipment(object):
    """
    
    """
    def __init__(self):
        """
        Constructor
        """    

        self.manipumatedVariables = 0
        self.stateVariables = 0

        self.controlledVariables = 0
    
    def ManipulateVariable(self, var, val):
        """
        pump has manipulated variables
        """
        pass
    
    def On(self):
        pass

    def Off(self):
        pass
    
    def ShutDown(self):
        """
        turns all manipulated variables off, and turns pump off
        """
        pass
    

class Pump(FellesEquipment):
    """
    
    """
    def __init__(self, *args, **kwargs):
        pass    
    
    