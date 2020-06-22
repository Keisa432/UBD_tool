from PyQt5 import QtCore, QtWidgets, QtGui


class FilterLabel(QtWidgets.QLabel):
    delete_filter = QtCore.pyqtSignal(str)

    def __init__(self, text, parent=None):
        super(FilterLabel, self).__init__(parent)
        self._text = text
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(30, 30)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                           QtWidgets.QSizePolicy.Fixed)
        self.setText(self._text)
        self.adjustSize()
        self.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setAlignment(QtCore.Qt.AlignTop)

    def mousePressEvent(self, ev):
        self.delete_filter.emit(self._text)
        self.deleteLater()
