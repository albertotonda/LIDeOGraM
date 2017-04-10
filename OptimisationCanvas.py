#-*- coding: utf-8
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog

# TODO
class OptimisationCanvas(QDialog):
    def __init__(self, parent=None):
        super(OptimisationCanvas, self).__init__(parent)
        self.setWindowTitle('Global Optimisation')
        self.icon = QtGui.QIcon("iconeLSN")
        self.setWindowIcon(self.icon)
        mainBoxLayout = QVBoxLayout(self)
        layout = QHBoxLayout()
        mainBoxLayout.addLayout(layout)
        s1 = QVBoxLayout()
        s2 = QVBoxLayout()

        popsize = QLineEdit()
        concurr = QLineEdit()

        s1.addWidget(QLabel("Pop size:"))
        s1.addWidget(popsize)

        s2.addWidget(QLabel("Concurrency:"))
        s2.addWidget(concurr)

        layout.addLayout(s1)
        layout.addLayout(s2)
        font = QFont('Liberation Sans Narrow')
        font.setPointSize(12)
        self.setFont(font)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        mainBoxLayout.addWidget(buttons)

    def params(self):
        return 0

    @staticmethod
    def get_params(Parent=None):
        dialog = OptimisationCanvas()
        result = dialog.exec_()
        params = dialog.params()
        return (result, params)






