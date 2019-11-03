import pandas as pd

class Change:
    """Change class
    
    Stores the a change. It keeps the original as well as the column that
    was change and its new value as propteries
    Returns:
        Change -- Change class instance
    """
    def __init__(self, row, changed_column, changed_value):
        self.row = row
        self.changed_column = changed_column
        self.change_value = changed_value

    def get_change(self):
        """Returns string representation of the change. For debugging purposes.
        
        Returns:
            String -- String representaion of the change
        """
        l = []
        str_row = self.row.apply(str)
        for col in self.row.index.tolist():
            if col != self.changed_column:
                l.append(str_row[col])
        l.append(str_row.at[self.changed_column])
        l.append(self.change_value)
        return l