from PyQt5 import QtCore, QtWidgets, QtGui


class QChangeWidget(QtWidgets.QWidget):

    def __init__(self, data, parent=None):
        super(QChangeWidget, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout()
        orig = data['original']
        changes = data['changes']
        index = 0
        for k, v in orig.items():
            self.layout.addWidget(QtWidgets.QLabel(k), index, 0)
            self.layout.addWidget(QtWidgets.QLabel(v), index, 1)
            if k in changes:
                self.layout.addWidget(QtWidgets.QLabel('--->'), index, 2)
                self.layout.addWidget(QtWidgets.QLabel(changes[k]), index, 3)
            index += 1
        self.setLayout(self.layout)
