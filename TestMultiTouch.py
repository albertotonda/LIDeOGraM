from PyQt4 import QtGui, QtCore
import sys
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from types import *


# TODO Crée tout les boutons (or graphes + équations)
class RFGraph_View(QtGui.QMainWindow,QtGui.QGraphicsItem):

    def __init__(self):


        QtGui.QMainWindow.__init__(self)
        QtGui.QGraphicsItem.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("LIDeoGraM")
        self.icon = QtGui.QIcon("Icone.png")
        self.setWindowIcon(self.icon)
        self.main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.main_widget)
        #self.setWindowState(QtCore.Qt.WindowMaximized)
        #self.show()

    def testEvent(self,event):
        print('It works ! ' + str(event.type()))
        return True

    def testEvent2(self,event):
        print('It works 2 ! ' + str(event.type()))
        return True
    def testEvent3(self,event):
        print('It works 3 ! ' + str(event.type()))
        return True
    def testEvent4(self,event):
        print('It works 4 ! ' + str(event.type()))
        return True


qApp = QtGui.QApplication(sys.argv)
vwApp = RFGraph_View()
vwApp.setAttribute(Qt.WA_AcceptTouchEvents)
vwApp.event = vwApp.testEvent
vwApp.sceneEvent = vwApp.testEvent2
vwApp.main_widget.setAttribute(Qt.WA_AcceptTouchEvents)
vwApp.main_widget.event = vwApp.testEvent3
vwApp.main_widget.sceneEvent = vwApp.testEvent4
vwApp.show()
sys.exit(qApp.exec_())

#sys.exit(qApp.exec_())