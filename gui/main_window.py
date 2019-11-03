import sys
import os
from .panda_table import PandasModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class UbdTool(QtWidgets.QMainWindow):
    csv_loaded = QtCore.pyqtSignal()

    def __init__(self, inventory, tracker):
        super(UbdTool, self).__init__()
        self._inventory = inventory
        self._tracker = tracker
        loadUi(r'./gui/main_window.ui', self)
        self.setWindowTitle('UBD Tool')
        self.init_toolbar_menu()
        self.init_filter_ui()
        self.csv_loaded.connect(self.populate_ui)

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
        self.csv_loaded.emit()

    def populate_ui(self):
        self.init_inventory_table(self._inventory)
        mod = self.inventoryTable.model()
        mod.data_changed.connect(self.print_change)

    def init_filter_ui(self):
        self.add_filter.clicked.connect(self.apply_filter)
        self.clear_filters.clicked.connect(self.reset_filters)
        self.colorBox.stateChanged.connect(self.toggle_colors)
    
    def toggle_colors(self):
        model = self.inventoryTable.model()
        model.layoutAboutToBeChanged.emit()
        model.colors_enabled = not model.colors_enabled
        model.layoutChanged.emit()

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
    
    def print_change(self):
       change = self._tracker.get_last_change()
       headers = change.row.index.tolist()
       headers.append(" ")
       headers.append("new")
       #self.changeTableWidget.setHorizontalHeaderLabels(headers)
       #count = self.changeTableWidget.rowCount()
       #self.changeTableWidget.insertRow(count, change.get_change())
       #self.changeTabWidget.addItem(str(change))

def run_main_app(inventory, tracker):
    app=QtWidgets.QApplication(sys.argv)
    widget= UbdTool(inventory, tracker)
    widget.show()
    sys.exit(app.exec_())
