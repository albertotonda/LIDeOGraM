#-*- coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

# TODO Crée la fenêtre d'aide
class Help(QDialog):
    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.setMaximumHeight(500)
        self.setMaximumWidth(500)
        self.setWindowTitle('Help')
        self.icon = QtGui.QIcon("C:/Users/pault/Documents/RFGraph/icons/etoile.png")
        self.setWindowIcon(self.icon)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        label = QLabel(open("C:/Users/pault/Documents/RFGraph/Help/help.txt").read())
        self.scrollArea.setWidget(label)
        self.scrollArea.ensureWidgetVisible(label, 150, 150)

    def params(self):
        return 0

    @staticmethod
    def get_params():
        tutorial = Help()
        tuto = tutorial.exec_()
        parameters = tutorial.params()
        return (tuto, parameters)