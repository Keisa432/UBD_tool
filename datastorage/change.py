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
        l = {}
        o = l['original'] = {}
        str_row = self.row.apply(str)

        for col in self.row.index.tolist():
                o[col] = str_row.at[col]

        c = l['changes'] = {}
        c[self.changed_column] = self.change_value

        return l
    
    def __str__(self):
        print_row = self.row
        print_row["new " + self.changed_column] = self.change_value
       
        return str(print_row)