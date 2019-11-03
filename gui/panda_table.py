from PyQt5 import QtCore
from PyQt5 import QtGui
from datastorage import Inventory
import pandas as pd

class PandasModel(QtCore.QAbstractTableModel):
    data_changed = QtCore.pyqtSignal()
    sled_bbd_offset = 5
    def __init__(self, inventory, parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._inventory = inventory
     

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._inventory.working_set.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._inventory.working_set.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.BackgroundRole:
            return self._check_date(index)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._inventory.working_set.iloc[index.row(), index.column()]))

    def _check_date(self, index):
        header = self._inventory.working_set.columns.tolist()[self.sled_bbd_offset]
        color = QtCore.QVariant()
        today = pd.to_datetime('today')
        difference = self._inventory.working_set.iloc[index.row(), self.sled_bbd_offset] - today
        if difference.days < 90:
            color = QtGui.QBrush(QtCore.Qt.red)
        elif difference.days < 365:
            color = QtGui.QBrush(QtCore.Qt.yellow)

        return color

    def setData(self, index, value, role):
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            pass
            # PySide gets an unicode
            #dtype = self._df[col].dtype
           # if dtype != object:
           #     value = None if value == '' else dtype.type(value)
        self._inventory.change_data_entry(index.row(), index.column(), value)
        self.data_changed.emit()
        return True

    def flags(self, index):
        return (QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._inventory.working_set.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._inventory.working_set.columns)

    def sort(self, column, order):
        if(column is not -1):
            colname = self._inventory.get_column_name(column)
            self.layoutAboutToBeChanged.emit()
            self._inventory.sort_by_category(colname, ascending=(order == QtCore.Qt.AscendingOrder))
            self.layoutChanged.emit()
