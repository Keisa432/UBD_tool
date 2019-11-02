import sys
import os
from .panda_table import PandasModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class ObdTool(QtWidgets.QMainWindow):
    def __init__(self, inventory):
        super(ObdTool, self).__init__()
        self._inventory = inventory
        loadUi(r'./gui/main_window.ui', self)
        self.setWindowTitle('OBD Tool')
        self.init_toolbar_menu()
        #self.init_inventory_table(inventory)
        #self.init_filter_ui()

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
    
    def init_toolbar_menu(self):
        self.actionLoad.triggered.connect(self.get_file)

    def get_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self._inventory.load_data(fname[0])
        self.init_inventory_table(self._inventory)
        self.init_filter_ui()

    def init_filter_ui(self):
        self.add_filter.clicked.connect(self.apply_filter)
        self.clear_filters.clicked.connect(self.reset_filters)
    
    def apply_filter(self):
        value = str(self.lineEdit.text())
        self.lineEdit.setText('')
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.filter_multiple([("", value)])
        filter_label = QtWidgets.QLabel()
        filter_label.setText(value)
        self.active_filter_layout.addWidget(filter_label)
        mod.layoutChanged.emit()

    def reset_filters(self):
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.reset_filters()
        for i in reversed(range(self.active_filter_layout.count())): 
            self.active_filter_layout.itemAt(i).widget().deleteLater()
        mod.layoutChanged.emit()

def run_main_app(inventory):
    app=QtWidgets.QApplication(sys.argv)
    widget= ObdTool(inventory)
    widget.show()
    sys.exit(app.exec_())
