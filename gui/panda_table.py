from PyQt5 import QtCore
from PyQt5 import QtGui
from datastorage import Inventory
import pandas as pd


class PandasModel(QtCore.QAbstractTableModel):
    data_changed = QtCore.pyqtSignal()
    sled_bbd_offset = 5
    sloc_offset = 3
    colors_enabled = False
    ROW_LOAD_COUNT = 15

    def __init__(self, inventory, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._inventory = inventory
        self._rows_loaded = PandasModel.ROW_LOAD_COUNT

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._inventory.working_set.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                return self._inventory.working_set.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.BackgroundRole and self.colors_enabled:
            return self._check_date(index)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(
            str(self._inventory.working_set.iloc[index.row(),
                                                 index.column()]))

    def _check_date(self, index):
        color = QtCore.QVariant()
        today = pd.to_datetime('today')
        difference = self._inventory.working_set.iloc[
            index.row(), self.sled_bbd_offset] - today
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
        self._inventory.change_data_entry(index.row(), index.column(), value)
        self.data_changed.emit()
        return True

    def flags(self, index):
        flags = (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

        if index.column() == PandasModel.sloc_offset:
            flags |= (QtCore.Qt.ItemIsEditable)
        return flags

    def rowCount(self, parent=QtCore.QModelIndex()):
        if len(self._inventory.working_set.index) <= self._rows_loaded:
            return len(self._inventory.working_set.index)
        else:
            return self._rows_loaded

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._inventory.working_set.columns)

    def canFetchMore(self, index=QtCore.QModelIndex):
        if len(self._inventory.working_set.index) > self._rows_loaded:
            return True
        else:
            return False

    def fetchMore(self, index=QtCore.QModelIndex):
        remainder = len(self._inventory.working_set.index) - self._rows_loaded
        itemNum = min(remainder, PandasModel.ROW_LOAD_COUNT)
        self.layoutAboutToBeChanged.emit()
        self.beginInsertRows(QtCore.QModelIndex(), self._rows_loaded,
                             self._rows_loaded + itemNum - 1)
        self._rows_loaded += itemNum
        self.endInsertRows()
        self.layoutChanged.emit()

    def sort(self, column, order):
        if (column is not -1):
            colname = self._inventory.get_column_name(column)
            self.layoutAboutToBeChanged.emit()
            self._inventory.sort_by_category(
                colname, ascending=(order == QtCore.Qt.AscendingOrder))
            self.layoutChanged.emit()

    def item(self, row, column):
        val = ""
        try:
            val = str(self._inventory.working_set.iloc[row, column])
        except:
            pass

        return val

    def number_rows(self):
        """Get number of entries in inventory table
        
        Returns:
            int -- Number of entries
        """
        try:
            return len(self._inventory.working_set.index)
        except:
            return 0

    def number_columns(self):
        """Get number of elements in inventory entry
        
        Returns:
            int -- number of elements
        """
        try:
            return len(self._inventory.working_set.columns)
        except:
            return 0
