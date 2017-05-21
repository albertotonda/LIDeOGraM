#-*- coding: utf-8

from classes.WindowClasses import WindowClasses
from classes.ClassGraph import ClassGraph
from classes.ClassesModel import ClassesModel
import sys
from PyQt4 import QtGui

cm = ClassesModel()
qApp = QtGui.QApplication(sys.argv)
vwApp = WindowClasses(cm.getGraph(), lambda x: print("Fin"))
#vwApp = Window(ClassGraph.readJson("test2"))
#vwApp = Window(cm.graph, lambda x: print("Fin"))
sys.exit(qApp.exec_())
