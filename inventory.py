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
    
    def load_data(self):
        """Load data farom csv
        """
        self.data = pd.read_csv(self._path_to_csv, self._sep)
        # convert timestampo string to date time
        self.data['SLED/BBD'] = pd.to_datetime(self.data ['SLED/BBD'])
        # drop last column with nan values
        self.data.dropna(axis=1, thresh=len(self.data) - 1, inplace=True)

    def filter_multiple(self, filters):
        """Apply a list of filters to the dataframe.
        The filters are linked logically with AND
        
        Arguments:
            df {Dataframe} -- source dataframe
            filters {List} -- list containig filter conditions
        
        Returns:
            Dataframe -- Filtered dataframe
        """
        f = self.data
        for filter in filters:
            f = self.filter_data(f, filter[0], filter[1])
        return f

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
        
# class debug
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 1000)

inv = Inventory(r'./Bestand_Material_15_10_2019.csv')
inv.load_data()
print(inv.data)




    