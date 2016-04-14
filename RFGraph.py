#-*- coding: utf-8

from PyQt4 import QtGui
import ui
import sys


qApp = QtGui.QApplication(sys.argv)
aw = ui.ApplicationWindow()
aw.setWindowTitle('RFGraph')
aw.show()
sys.exit(qApp.exec_())

