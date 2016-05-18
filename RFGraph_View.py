#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from NetworkCanvas import NetworkCanvas
from EqTableCanvas import EqTableCanvas
from FitCanvas import FitCanvas


class RFGraph_View(QtGui.QMainWindow):

    def __init__(self,modApp):

        self.modApp=modApp

        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("RFGraph")

        self.main_widget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)
        self.networkGUI = NetworkCanvas(self.modApp)
        self.gridLayout.addWidget(self.networkGUI, 0, 0, 8, 60)

        self.adjThreshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.adjThreshold_slider.setValue(self.modApp.adjThresholdVal * 100)

        self.adjThreshold_lab = QtGui.QLabel('Importance des arcs : ')
        self.gridLayout.addWidget(self.adjThreshold_lab, 7, 0, 1, 2)
        self.gridLayout.addWidget(self.adjThreshold_slider, 7, 2, 1, 57)

        self.comprFitCmplx_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.comprFitCmplx_slider.setValue(self.modApp.comprFitCmplxVal * 100)
        self.comprFitCmplx_lab = QtGui.QLabel('Compromis : ')
        self.gridLayout.addWidget(self.comprFitCmplx_lab, 8, 0)
        self.comprFitCmplx_lab_cmplx = QtGui.QLabel('Complexité')
        self.gridLayout.addWidget(self.comprFitCmplx_lab_cmplx, 8, 1)
        self.gridLayout.addWidget(self.comprFitCmplx_slider, 8, 2, 1, 57)
        self.comprFitCmplx_lab_fit = QtGui.QLabel('Fitness')
        self.gridLayout.addWidget(self.comprFitCmplx_lab_fit, 8, 59, 1, 1)

        self.eqTableGUI = EqTableCanvas(self.modApp)

        self.gridLayout.addWidget(self.eqTableGUI, 0, 60, 6, 60)

        self.fitGUI = FitCanvas(self.modApp)
        self.gridLayout.addWidget(self.fitGUI, 6, 60, 6, 60)

        self.buttonCompromis = QtGui.QPushButton('Compromis', self)
        self.buttonFitness = QtGui.QPushButton('Fitness', self)
        self.buttonComplexite = QtGui.QPushButton('Complexité', self)
        self.buttonOptUgp3 = QtGui.QPushButton('Optimisation µGP', self)
        self.buttonModLocal = QtGui.QPushButton('Modeles Locaux', self)
        self.buttonModGlobal = QtGui.QPushButton('Modele Global', self)
        self.buttonAjtCntrt = QtGui.QPushButton('Ajout contrainte', self)
        self.buttonChangerEq = QtGui.QPushButton('Changer d\'equation', self)

        self.gridLayout.addWidget(self.buttonCompromis, 9, 0, 1, 15)
        self.gridLayout.addWidget(self.buttonFitness, 9, 15, 1, 15)
        self.gridLayout.addWidget(self.buttonComplexite, 9, 30, 1, 15)
        self.gridLayout.addWidget(self.buttonOptUgp3, 9, 45, 1, 15)
        self.gridLayout.addWidget(self.buttonModLocal, 10, 0, 1, 30)
        self.gridLayout.addWidget(self.buttonModGlobal, 10, 30, 1, 30)
        self.gridLayout.addWidget(self.buttonAjtCntrt, 11, 0, 1, 30)
        self.gridLayout.addWidget(self.buttonChangerEq, 11, 30, 1, 30)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle('RFGraph')
        self.show()
        self.updateView()




    def updateView(self):
        self.networkGUI.updateView()
        self.fitGUI.updateView()
        self.eqTableGUI.updateView()




