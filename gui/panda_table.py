from PyQt5 import QtCore
from datastorage import Inventory

class PandasModel(QtCore.QAbstractTableModel): 
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
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._inventory.working_set.iloc[index.row(), index.column()]))

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
