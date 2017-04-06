#-*- coding: utf-8

from classes.Window import Window
from classes.ClassGraph import ClassGraph
import sys
from PyQt4 import QtGui


qApp = QtGui.QApplication(sys.argv)
vwApp = Window(ClassGraph.readJson("test2"))
sys.exit(qApp.exec_())
