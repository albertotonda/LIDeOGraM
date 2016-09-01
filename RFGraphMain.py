#-*- coding: utf-8
from RFGraph_View import RFGraph_View
from RFGraph_Model import RFGraph_Model
from RFGraph_Controller import RFGraph_Controller
from QtConnector import QtConnector
import sys
from PyQt4 import QtGui
import observers

modApp=RFGraph_Model()
qApp = QtGui.QApplication(sys.argv)
vwApp = RFGraph_View(modApp)
o = observers.Observer()
cntrApp=RFGraph_Controller(modApp,vwApp)
cntrApp.registerObs(o)
qtconnector=QtConnector(vwApp,cntrApp)

sys.exit(qApp.exec_())