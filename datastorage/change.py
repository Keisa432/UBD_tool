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

    def __str__(self):
        """Returns string representation of the change. For debugging purposes.
        
        Returns:
            String -- String representaion of the change
        """
        return f'Changed value in row {self.row.name}: {self.changed_column} {self.row.at[self.changed_column]} -> {self.change_value}'