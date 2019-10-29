import pandas as pd

class Inventory:
    """Inventory class

    Class used to represent the inventory. Provides methods to
    filter and sort the data it stores. The data is loaded from
    as CSV file.
    
    Returns:
        Inventory -- Inventory class
    """
    def __init__(self, path_to_csv, sep=';'):
        """Inventory constructor

        Arguments:
            path_to_csv {string} -- Path of the csv file
            sep {string} -- seperator used in the csv file. default=";"   
        """
        self._path_to_csv = path_to_csv
        self._sep = sep
        self.data = None
        self.subset = None

    def load_data(self):
        """Load data farom csv
        """
        self.data = pd.read_csv(self._path_to_csv, self._sep)
        # convert timestampo string to date time
        self.data['SLED/BBD'] = pd.to_datetime(self.data ['SLED/BBD'])
        # drop last column with nan values
        self.data.dropna(axis=1, thresh=len(self.data) - 1, inplace=True)

    def filter_multiple(self, filters):
        """Filter data frame and create subset
        
        Apply a list of filters to the dataframe. The filters are linked 
        logically with AND. This function creates a subset and returns it. 
        The subset is also stored as property 'subset' of this class
        
        Arguments:
            df {Dataframe} -- source dataframe
            filters {List} -- list containig filter conditions
        
        Returns:
            Dataframe -- Filtered dataframe
        """
        self.subset = self.data
        for filter in filters:
            self.subset = self.filter_data(self.subset, filter[0], filter[1])
        return self.subset

    def filter_data(self, data, cat, val):
        """Filter Pandas dataframe for a given column value
        
        Arguments:
            data {Dataframe} -- source dataframe
            cat {String} -- column name
            val {Any} -- value to filter
        
        Returns:
            Dataframe -- Filtered dataframe
        """
        return data[data[cat] == val]
    
    def restore_orignal_order(self, subset=False):
        """Restore orignal order of columns
        
        Keyword Arguments:
            subset {bool} -- If True, the orignal order of the subset is restored (default: {False})
        """
        if(subset):
            self.subset.sort_index(ascending=True, inplace=True)
        else:
            self.data.sort_index(ascending=True, inplace=True)

    def sort_by_category(self, cat, subset=False, ascending=True):
        """Sort data by category
        
        Arguments:
            cat {String} -- Cartegory string to sort data by
        
        Keyword Arguments:
            subset {bool} -- If true sort subset (default: {False})
            ascending {bool} -- If True sort in ascending order (default: {True})
        """
        if(subset):
            self.subset.sort_values(cat, axis=0, ascending=ascending, inplace=True)
        else:
            self.data.sort_values(cat, axis=0, ascending=ascending, inplace=True)

    def change_asset_location(self, row_idx, new_loc):
        pass

# class debug
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 1000)

inv = Inventory(r'./Bestand_Material_15_10_2019.csv')
inv.load_data()
inv.sort_by_category('SLoc')
print(inv.data)
inv.restore_orignal_order()
print(inv.data)
