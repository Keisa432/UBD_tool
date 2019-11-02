import sys
import os
from .panda_table import PandasModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class ObdTool(QtWidgets.QDialog):
    def __init__(self, inventory):
        super(ObdTool, self).__init__()
        loadUi(r'./gui/main_window.ui', self)
        self.setWindowTitle('OBD Tool')
        self.init_inventory_table(inventory)
        self.init_filter_ui()

    def init_inventory_table(self, inventory):
        self.inventoryTable.setSortingEnabled(True)
        self.inventoryTable.setModel(PandasModel(inventory))
        self.inventoryTable.resize
        self.inventoryTable.resizeColumnsToContents()
        header = self.inventoryTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        btn = self.inventoryTable.findChild(QtWidgets.QAbstractButton)
        if btn:
            btn.disconnect()
            btn.clicked.connect(self.disable_sort)

    def disable_sort(self):
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.restore_orignal_order()
        self.inventoryTable.horizontalHeader().setSortIndicator(-1, 0)
        mod.layoutChanged.emit()

    def init_filter_ui(self):
        mod = self.inventoryTable.model()
        headers = mod._inventory.working_set.columns.tolist()
        self.comboBox.clear()
        self.comboBox.addItems(headers)
        width = self.comboBox.minimumSizeHint().width()
        self.comboBox.view().setMinimumWidth(width)
        self.add_filter.clicked.connect(self.apply_filter)
        self.clear_filters.clicked.connect(self.reset_filters)
    
    def apply_filter(self):
        column = str(self.comboBox.currentText())
        value = str(self.lineEdit.text())
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.filter_multiple([(column, value)])
        mod.layoutChanged.emit()

    def reset_filters(self):
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.reset_filters()
        mod.layoutChanged.emit()

def run_main_app(inventory):
    app=QtWidgets.QApplication(sys.argv)
    widget= ObdTool(inventory)
    widget.show()
    sys.exit(app.exec_())
