#-*- coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

# TODO Crée la fenêtre d'aide
class Help(QDialog):
    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.setMaximumHeight(10)
        self.setMaximumWidth(10)
        self.setWindowTitle('Help')
        self.icon = QtGui.QIcon("C:/Users/pault/Documents/RFGraph/icons/etoile.png")
        self.setWindowIcon(self.icon)
        mainBox = QVBoxLayout(self)
        boxlayout = QHBoxLayout()
        mainBox.addLayout(boxlayout)
        m1 = QVBoxLayout()
        m1.addWidget(QLabel(open("C:/Users/pault/Documents/RFGraph/help/help.txt").read()))
        boxlayout.addLayout(m1)


    def params(self):
        return 0

    @staticmethod
    def get_params():
        tutorial = Help()
        tuto = tutorial.exec_()
        parameters = tutorial.params()
        return (tuto, parameters)