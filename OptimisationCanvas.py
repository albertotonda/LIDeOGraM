#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

class OptimisationCanvas(QDialog):
    def __init__(self,parent=None):
        super(OptimisationCanvas,self).__init__(parent)
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

#class Parameters:
#    def __init__(self):
#        self.mode_global = False
#        self.lastNodeClicked = ''
#        self.mode_cntrt = False
#        self.click1 = ''
#        self.click2 = ''




