#-*- coding: utf-8
import numpy as np

from PyQt4 import QtGui, QtCore
from NetworkCanvas import NetworkCanvas
from MyTable import MyTable
from Optimisation import Optimisation
from FitCanvas import FitCanvas


class RFGraph_View(QtGui.QMainWindow):

    # self.modApp : Modèle MVC

    def __init__(self,modApp):

        self.modApp=modApp

        QtGui.QMainWindow.__init__(self)
        # TODO : Que fait la ligne d'en dessous ?
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("RFGraph")

        #self.flash = Parameters()
        #self.flash.mode_global = ...

        self.main_widget = QtGui.QWidget(self)

        self.grid = QtGui.QGridLayout(self.main_widget)
        self.grid.setSpacing(5)
        #self.RFG = NetworkCanvas(self.modApp, self.main_widget)
        self.RFG = NetworkCanvas(self.modApp)
        self.grid.addWidget(self.RFG,0,0,8,60)

        self.ts_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.ts_slider.setValue(50)
        ts_lab = QtGui.QLabel('Importance des arcs : ')
        self.grid.addWidget(ts_lab,7,0,1,2)
        self.grid.addWidget(self.ts_slider,7,2,1,57)

        self.ds_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.ds_slider.setValue(50)
        ds_lab = QtGui.QLabel('Compromis : ')
        self.grid.addWidget(ds_lab,8,0)
        ds_lab_cmplx = QtGui.QLabel('Complexité')
        self.grid.addWidget(ds_lab_cmplx,8,1)
        self.grid.addWidget(self.ds_slider,8,2,1,57)
        ds_lab_fitness = QtGui.QLabel('Fitness')
        self.grid.addWidget(ds_lab_fitness, 8, 59,1,1)

        #Charge la base de données d'équations à afficher après chargement
        #TODO: Base de données d'équations à changer
        data_tmp=self.modApp.equacolPOs[:,np.ix_([0,1,4])]
        data=[]
        for i in range(len(data_tmp)):
            data.append(data_tmp[i][0])

        # Test coloration ligne selectioné dans le tableau d'équation
        #for i in range(len(data[5])):
        #    self.table.item(5,i).setBackground(QtGui.QColor(150,150,150))

        self.table = MyTable(data, len(data), 3)

        self.grid.addWidget(self.table, 0, 60, 6, 60)

        #self.fitg = FitCanvas(self.main_widget)
        self.fitg = FitCanvas()
        self.grid.addWidget(self.fitg,6,60,6,60)

        self.buttonCompromis = QtGui.QPushButton('Compromis', self)
        self.buttonFitness = QtGui.QPushButton('Fitness', self)
        self.buttonComplexite = QtGui.QPushButton('Complexité', self)
        self.buttonOptUgp3 = QtGui.QPushButton('Optimisation µGP', self)
        self.buttonModLocal = QtGui.QPushButton('Modeles Locaux', self)
        self.buttonModGlobal = QtGui.QPushButton('Modele Global', self)
        self.buttonAjtCntrt = QtGui.QPushButton('Ajout contrainte', self)
        self.buttonChangerEq = QtGui.QPushButton('Changer d\'equation', self)

        self.grid.addWidget(self.buttonCompromis, 9, 0, 1, 15)
        self.grid.addWidget(self.buttonFitness, 9, 15, 1, 15)
        self.grid.addWidget(self.buttonComplexite, 9, 30, 1, 15)
        self.grid.addWidget(self.buttonOptUgp3, 9, 45, 1, 15)
        self.grid.addWidget(self.buttonModLocal, 10, 0, 1, 30)
        self.grid.addWidget(self.buttonModGlobal, 10, 30, 1, 30)
        self.grid.addWidget(self.buttonAjtCntrt, 11, 0, 1, 30)
        self.grid.addWidget(self.buttonChangerEq, 11, 30, 1, 30)



        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle('RFGraph')
        self.show()




    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()