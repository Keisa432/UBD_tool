from .change import Change

class ChangeTracker:
    """Change tracker class

    Stores all changes done the the object it observes
    """
    def __init__(self):
        self._changes = []
    
    def __call__(self, change):
        """Track change
        
        Arguments:
            change {Change} -- Change made to observed object
        """
        self._changes.append(change)

    def remove_last_change(self):
        """Return last change

        This function removes the last change made and returns
        it.
        
        Returns:
            Change -- last change made
        """
        if len(self._changes) > 0:
            return self._changes.pop()
        else:
            return None

    def changes(self):
        for change in self._changes:
            yield change