# TODO Connecte les "clics" et les fonctions correspondantes
import sys
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from types import *

class QtConnector:
    def __init__(self,vwApp,cntrApp):
        self.vwApp=vwApp
        self.cntrApp=cntrApp
        self.vwApp.eqTableGUI.itemClicked.connect(self.cntrApp.eqTableClicked)
        #self.vwApp.adjThreshold_slider.valueChanged.connect(self.cntrApp.SliderMoved)

        #self.vwApp.comprFitCmplx_slider.valueChanged.connect(self.cntrApp.SliderMoved)
        #self.vwApp.buttonFitness.clicked.connect(self.cntrApp.clickFitness)
        #self.vwApp.buttonComplexite.clicked.connect(self.cntrApp.clickCmplx)
        #self.vwApp.buttonCompromis.clicked.connect(self.cntrApp.clickCompromis)
        #self.vwApp.buttonShowModGlobal.clicked.connect(self.cntrApp.clickShowModGlobal)
        #self.vwApp.buttonHideModGlobal.clicked.connect(self.cntrApp.clickHideModGlobal)
        #self.vwApp.buttonOptUgp3.clicked.connect(self.cntrApp.clickOptmuGP)
        #self.vwApp.buttonRemoveLink.clicked.connect(self.cntrApp.clickRemoveLink)
        #self.vwApp.buttonReinstateLink.clicked.connect(self.cntrApp.clickReinstateLink)
#        self.vwApp.buttonHelp.clicked.connect(self.cntrApp.clickHelp)
#        self.vwApp.buttonChangerEq.clicked.connect(self.cntrApp.clickChangeEq)
        self.vwApp.uncertaintyModifButton.clicked.connect(self.cntrApp.clickUncertaintyButton)
        self.vwApp.networkGUI.fig.canvas.mpl_connect('button_press_event', self.cntrApp.onClick)
        self.vwApp.networkGUI.fig.canvas.mpl_connect('motion_notify_event',self.cntrApp.onMove3)
        self.vwApp.incMatGUI.itemClicked.connect(self.cntrApp.incMatClicked)

        #self.vwApp.networkGUI.fig.canvas.mpl_connect('pick_event', self.cntrApp.onPick)
        self.vwApp.closeEvent = self.cntrApp.closeEvent
        self.vwApp.setAttribute(Qt.WA_AcceptTouchEvents)
        self.vwApp.main_widget.setAttribute(Qt.WA_AcceptTouchEvents)
        self.vwApp.main_widget.event = self.cntrApp.testmultitouch
        self.vwApp.networkGUI.setAttribute(Qt.WA_AcceptTouchEvents)
        self.vwApp.networkGUI.event = self.cntrApp.testmultitouch2
        #self.vwApp.eqTableGUI.setAttribute(Qt.WA_AcceptTouchEvents)
        #self.vwApp.eqTableGUI.event = self.cntrApp.testmultitouch2
        self.vwApp.show()
