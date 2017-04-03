#-*- coding: utf-8
import logging

from RFGraph_View import RFGraph_View
from RFGraph_Model import RFGraph_Model
from RFGraph_Controller import RFGraph_Controller
from QtConnector import QtConnector
import sys
from PyQt4 import QtGui

logging.basicConfig(filename="LiDeOGrAm.log", level=logging.INFO)
logging.info("Program start")

modApp=RFGraph_Model()
qApp = QtGui.QApplication(sys.argv)
vwApp = RFGraph_View(modApp)
cntrApp=RFGraph_Controller(modApp,vwApp)
vwApp.cntrApp=cntrApp
vwApp.eqTableGUI.cntrApp=cntrApp
vwApp.updateMenuBar(cntrApp)
qtconnector=QtConnector(vwApp,cntrApp)
sys.exit(qApp.exec_())

logging.info("Program end")
