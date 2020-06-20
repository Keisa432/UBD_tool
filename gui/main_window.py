import sys
import os
from utils import log_msg
from .panda_table import PandasModel
from .change_widget import QChangeWidget
from .filter_label import FilterLabel
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.uic import loadUi

# Translate asset paths to useable format for PyInstaller
def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)

class UbdTool(QtWidgets.QMainWindow):
    csv_loaded = QtCore.pyqtSignal()

    def __init__(self, inventory, tracker):
        super(UbdTool, self).__init__()
        self._inventory = inventory
        self._tracker = tracker
        #abs_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        #ui_path = os.path.join(abs_path,"gui", "main_window.ui")
        loadUi(resource_path("./gui/main_window.ui"), self)
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
        self.actionSave.triggered.connect(self.save_file)
        self.actionPrint.triggered.connect(self.handle_print)
        self.actionPrint.setEnabled(False)

    def get_file(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load UBD file','','CSV (*.csv);;All Files (*);;')
        self._inventory.load_data(fname)
        self.csv_loaded.emit()

    def save_file(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save UBD file','','CSV (*.csv);;All Files (*);;')
        self._inventory.save_data(fname)

    def handle_print(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handle_paint_request(dialog.printer())

    def handle_paint_request(self, printer):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(0)
        tableFormat.setCellSpacing(16)
        table = cursor.insertTable(
            self.inventoryTable.model().number_rows(),
            self.inventoryTable.model().number_columns(),tableFormat)
        for row in range(table.rows()):
            for col in range(table.columns()):
                cursor.insertText(self.inventoryTable.model().item(row, col))
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)

    def populate_ui(self):
        self.init_inventory_table(self._inventory)
        mod = self.inventoryTable.model()
        mod.colors_enabled = self.colorBox.isChecked()
        mod.data_changed.connect(self.track_change)
        self.actionPrint.setEnabled(True)

    def init_filter_ui(self):
        self.lineEdit.returnPressed.connect(self.apply_filter)
        self.clear_filters.clicked.connect(self.reset_filters)
        self.colorBox.stateChanged.connect(self.toggle_colors)
        self.hFilterLayout.addStretch()
    
    def toggle_colors(self):
        try:
            model = self.inventoryTable.model()
            model.layoutAboutToBeChanged.emit()
            model.colors_enabled = not model.colors_enabled
            model.layoutChanged.emit()
        except Exception as e:
            log_msg(__name__, 2, e)

    def apply_filter(self):
        value = str(self.lineEdit.text())
        self.lineEdit.setText('')
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.filter_multiple([("", value)])
        filter_label = FilterLabel(value)
        filter_label.delete_filter.connect(self.delete_filter)
        self.hFilterLayout.insertWidget(self.hFilterLayout.count()-1, filter_label)
        mod.layoutChanged.emit()
    
    def delete_filter(self, value):
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.delete_filter(value)
        mod.layoutChanged.emit()

    def reset_filters(self):
        mod = self.inventoryTable.model()
        mod.layoutAboutToBeChanged.emit()
        mod._inventory.reset_filters()
        for i in reversed(range(self.hFilterLayout.count())):
            try:
                self.hFilterLayout.itemAt(i).widget().deleteLater()
            except:
                continue
        mod.layoutChanged.emit()
    
    def track_change(self):
       change = self._tracker.get_last_change()
       changeWidget = QChangeWidget(change.get_change())
       listWidget = QtWidgets.QListWidgetItem(self.changeListWidget)
       listWidget.setSizeHint(changeWidget.sizeHint())
       self.changeListWidget.addItem(listWidget)
       self.changeListWidget.setItemWidget(listWidget, changeWidget)

def run_main_app(inventory, tracker):
    app=QtWidgets.QApplication(sys.argv)
    widget= UbdTool(inventory, tracker)
    widget.show()
    sys.exit(app.exec_())
