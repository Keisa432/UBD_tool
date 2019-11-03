import pandas as pd
from .change import Change

class Inventory:
    """Inventory class

    Class used to represent the inventory. Provides methods to
    filter and sort the data it stores. The data is loaded from
    as CSV file.
    
    Returns:
        Inventory -- Inventory class
    """
    def __init__(self, sep=';'):
        """Inventory constructor

        Arguments:
            path_to_csv {string} -- Path of the csv file
            sep {string} -- seperator used in the csv file. default=";"
        """
        self._sep = sep
        self.original_data = None
        self.working_set = None
        self.observers = []

    def attach(self, observer):
        """Add observer
        
        This function registers the observer. It will be notified
        any time a change to the data stored is made.

        Arguments:
            observer {Any} -- Observer
        """
        self.observers.append(observer)

    def notify(self, data):
        """Notify all registered observers
        
        Call all registered observers. Notifing them that
        something in the inventory changed.

        Arguments:
            data {[type]} -- Contains the change made as well as the old value
        """
        for observer in self.observers:
            observer(data)

    def load_data(self, path):
        """Load data farom csv
        """
        try:
            self.original_data = pd.read_csv(path, self._sep)
            # convert timestamp string to date time
            self.original_data['SLED/BBD'] = pd.to_datetime(self.original_data ['SLED/BBD'])
            # drop last column with nan values
            self.original_data.dropna(axis=1, thresh=len(self.original_data) - 1, inplace=True)
            #set working set to original data
            self.working_set = self.original_data
        except Exception as e:
            print(e)
    def save_data(self, path):
        try:
            self.original_data.to_csv(path, sep=self._sep, index=False)
        except Exception as e:
            print(e)
    def get_column_name(self, column):
        return self.working_set.columns.tolist()[column]
 
    def reset_filters(self):
        """Reset filters
        
        This function restores the originally loaded data
        """
        self.working_set = self.original_data

    def filter_multiple(self, filters):
        """Filter data frame and create subset
        
        Apply a list of filters to the dataframe. The filters are linked 
        logically with AND.
        
        Arguments:
            df {Dataframe} -- source dataframe
            filters {List} -- list containig filter conditions
        
        Returns:
            Dataframe -- Filtered dataframe
        """
        for filter in filters:
            self.working_set = self.filter_data(self.working_set, filter[0], filter[1])
        return self.working_set

    def filter_data(self, data, cat, val):
        """Filter Pandas dataframe for a given column value
        
        Arguments:
            data {Dataframe} -- source dataframe
            cat {String} -- column name
            val {Any} -- value to filter
        
        Returns:
            Dataframe -- Filtered dataframe
        """
        try:
            return data[data.apply(lambda row: row.astype(str).
                        str.contains(val, case=False).any(), axis=1)]
        except Exception as e:
            print(e)

    def restore_orignal_order(self):
        """Restore orignal order of columns
        
        """
        self.working_set.sort_index(ascending=True, inplace=True)

    def sort_by_category(self, cat, ascending=True):
        """Sort data by category
        
        Arguments:
            cat {String} -- Cartegory string to sort data by
        
        Keyword Arguments:
            ascending {bool} -- If True sort in ascending order (default: {True})
        """
        try:
            self.working_set.sort_values(cat, axis=0, ascending=ascending, inplace=True)
        except Exception as e:
            print(e)

    def change_data_entry(self, row_idx, column, new_data):
        """Change value of entry identified by row_idx and
        column
        
        Arguments:
            row_idx {Number} -- Index of row
            column {String} -- Column of row
            new_data {Any} -- new value
        """
        try:
            row = self.working_set.iloc[row_idx]
            col_name = self.working_set.columns.tolist()[column]
            self.notify(Change(row, col_name, new_data))
            self.working_set.iloc[row_idx, column] = new_data
            self.original_data.iloc[row_idx, column] = new_data
        except Exception as e:
            print(e)

    def replace_row(self, row):
        """Replace row with same name as row
        
        Arguments:
            row {Dataframe} -- new row to insert
        """
        try:
            self.working_set.loc[row.name] = row
            self.original_data.loc[row.name] = row
        except:
            pass