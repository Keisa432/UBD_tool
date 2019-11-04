from datastorage import Inventory
from datastorage import ChangeTracker
from gui import run_main_app
import pandas as pd

tracker = ChangeTracker()
inv = Inventory()
inv.attach(tracker)
run_main_app(inv, tracker)


