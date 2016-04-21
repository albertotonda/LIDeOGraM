#-*- coding: utf-8

from PyQt4 import QtGui
import Optimisation
import RFGraph_View as vw
import sys


qApp = QtGui.QApplication(sys.argv)
aw = vw.ApplicationWindow()
aw.setWindowTitle('RFGraph')
aw.show()
sys.exit(qApp.exec_())

