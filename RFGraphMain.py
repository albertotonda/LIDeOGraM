#-*- coding: utf-8
import sys

from PyQt4 import QtGui

from QtConnector import QtConnector
from RFGraph_Controller import RFGraph_Controller
from RFGraph_Model import RFGraph_Model
from RFGraph_View import RFGraph_View

qApp = QtGui.QApplication(sys.argv)
modApp=RFGraph_Model()
#vwApp = RFGraph_View(modApp)
#cntrApp=RFGraph_Controller(modApp,vwApp)
#vwApp.cntrApp=cntrApp
#vwApp.eqTableGUI.cntrApp=cntrApp
#vwApp.updateMenuBar(cntrApp)
#qtconnector=QtConnector(vwApp,cntrApp)
sys.exit(qApp.exec_())
