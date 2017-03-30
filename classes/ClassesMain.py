#-*- coding: utf-8

from classes.Window import Window
#from ClassesView import ClassesView
from classes.ClassesModel import ClassesModel
from RFGraph_Controller import RFGraph_Controller
from QtConnector import QtConnector
import sys
from PyQt4 import QtGui


modApp=ClassesModel()
qApp = QtGui.QApplication(sys.argv)
vwApp = Window(modApp.G, ["x", "y", "z"])
cntrApp=RFGraph_Controller(modApp,vwApp)
vwApp.cntrApp=cntrApp
#vwApp.eqTableGUI.cntrApp=cntrApp
#vwApp.updateMenuBar(cntrApp)
#QtConnector(vwApp, cntrApp)
sys.exit(qApp.exec_())
