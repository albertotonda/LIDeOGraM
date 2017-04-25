#-*- coding: utf-8

from classes.Window import Window
from classes.ClassGraph import ClassGraph
from classes.ClassesModel import ClassesModel
import sys
from PyQt4 import QtGui

cm = ClassesModel()
cm.initGraph()
qApp = QtGui.QApplication(sys.argv)
#vwApp = Window(ClassGraph.readJson("test2"))
vwApp = Window(cm.graph, lambda: print("Fin"))
sys.exit(qApp.exec_())
