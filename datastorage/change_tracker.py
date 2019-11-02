from .change import Change

class ChangeTracker:
    """Change tracker class

    Stores all changes done the the object it observes
    """
    def __init__(self):
        self.changes = []
    
    def __call__(self, change):
        """Track change
        
        Arguments:
            change {Change} -- Change made to observed object
        """
        self.changes.append(change)