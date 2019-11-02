from datastorage import Inventory
from datastorage import ChangeTracker
from gui import run_main_app
import pandas as pd

# class debug
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 1000)

tracker = ChangeTracker()
inv = Inventory(r'C:/Users/Dominik/python/panda_test/Bestand_Material_15_10_2019.csv')
inv.attach(tracker)
inv.load_data()
run_main_app(inv)


