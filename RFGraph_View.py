#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from NetworkCanvas import NetworkCanvas
from EqTableCanvas import EqTableCanvas
from FitCanvas import FitCanvas
from QtConnector import QtConnector

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
        self.gridLayout.addWidget(self.networkGUI, 1, 0, 8, 60)

        self.adjThreshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.adjThreshold_slider.setValue(self.modApp.adjThresholdVal * 100)

        self.adjThreshold_lab = QtGui.QLabel('Edges importance : ')
        self.gridLayout.addWidget(self.adjThreshold_lab, 8, 0, 1, 2)
        self.gridLayout.addWidget(self.adjThreshold_slider, 8, 2, 1, 57)

        self.comprFitCmplx_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.comprFitCmplx_slider.setValue(self.modApp.comprFitCmplxVal * 100)
        self.comprFitCmplx_lab = QtGui.QLabel('Compromise : ')
        self.gridLayout.addWidget(self.comprFitCmplx_lab, 9, 0)
        self.comprFitCmplx_lab_cmplx = QtGui.QLabel('Complexity')
        self.gridLayout.addWidget(self.comprFitCmplx_lab_cmplx, 9, 1)
        self.gridLayout.addWidget(self.comprFitCmplx_slider, 9, 2, 1, 57)
        self.comprFitCmplx_lab_fit = QtGui.QLabel('Fitness')
        self.gridLayout.addWidget(self.comprFitCmplx_lab_fit, 9, 59, 1, 1)

        self.eqTableGUI = EqTableCanvas(self.modApp)

        self.gridLayout.addWidget(self.eqTableGUI, 1, 60, 6, 60)

        self.fitGUI = FitCanvas(self.modApp)
        self.gridLayout.addWidget(self.fitGUI, 7, 60, 6, 60)

        self.buttonCompromis = QtGui.QPushButton('Compromise', self)
        self.buttonFitness = QtGui.QPushButton('Fitness', self)
        self.buttonComplexite = QtGui.QPushButton('Complexity', self)
        self.buttonOptUgp3 = QtGui.QPushButton('µGP Optimisation', self)
        self.buttonModLocal = QtGui.QPushButton('Locals Models', self)
        self.buttonModGlobal = QtGui.QPushButton('Global Model', self)
        self.buttonAjtCntrt = QtGui.QPushButton('Add constraints', self)
        self.buttonChangerEq = QtGui.QPushButton('Change equation', self)
        self.buttonRemoveConstraint = QtGui.QPushButton('Remove', self)

        self.gridLayout.addWidget(self.buttonCompromis, 10, 0, 1, 15)
        self.gridLayout.addWidget(self.buttonFitness, 10, 15, 1, 15)
        self.gridLayout.addWidget(self.buttonComplexite, 10, 30, 1, 15)
        self.gridLayout.addWidget(self.buttonOptUgp3, 10, 45, 1, 15)
        self.gridLayout.addWidget(self.buttonModLocal, 11, 0, 1, 30)
        self.gridLayout.addWidget(self.buttonModGlobal, 11, 30, 1, 30)
        self.gridLayout.addWidget(self.buttonAjtCntrt, 12, 0, 1, 30)
        self.gridLayout.addWidget(self.buttonChangerEq, 12, 30, 1, 30)
        self.gridLayout.addWidget(self.buttonRemoveConstraint, 0, 12, 2, 12)

        # TODO  Ajout de la liste déroulante
        self.listeDeroulante = QtGui.QComboBox(self)
        self.gridLayout.addWidget(self.listeDeroulante, 0, 0, 2, 12 )
        self.listeDeroulante.addItem("Select constraint to remove")

        self.advContr = QtGui.QLabel('')
        self.gridLayout.addWidget(self.advContr, 0, 25, 2, 12)


        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle('RFGraph')
        self.show()
        self.updateView()




    def updateView(self):
        self.networkGUI.updateView()
        self.fitGUI.updateView()
        self.eqTableGUI.updateView()




