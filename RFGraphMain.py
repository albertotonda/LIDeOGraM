#-*- coding: utf-8
import sys
from PyQt4 import QtGui
from RFGraph_Model import RFGraph_Model

qApp = QtGui.QApplication(sys.argv)
modApp=RFGraph_Model()
sys.exit(qApp.exec_())
