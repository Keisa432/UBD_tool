from datastorage import Inventory
import pandas as pd

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

