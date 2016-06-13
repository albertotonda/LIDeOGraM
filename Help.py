#-*- coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

# TODO Crée la fenêtre d'aide
class Help(QDialog):
    def __init__(self, parent=None):
        super(Help, self).__init__(parent)
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        self.setWindowTitle('Help')
        self.icon = QtGui.QIcon("C:/Users/pault/Documents/RFGraph/icons/dessin_6-2.png")
        self.setWindowIcon(self.icon)
        scrollArea = QScrollArea(self)
        label = QLabel(open("C:/Users/pault/Documents/RFGraph/Help/help.txt").read())
        font = QFont('Comic Sans MS')
        font.setPointSize(20)
        label.setFont(font)
        scrollArea.setWidget(label)
        scrollArea.resize(800, 600)
        scrollArea.setAlignment(QtCore.Qt.AlignHCenter)

    def params(self):
        return 0

    @staticmethod
    def get_params():
        help = Help()
        tutorial = help.exec_()
        parameters = help.params()
        return (tutorial, parameters)