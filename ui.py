#-*- coding: utf-8
from math import *

import numpy as np
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

import data as fdata
import graphs




class MyTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data

        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setmydata(self):
        self.clear()
        for n  in range(len(self.data)):
            for m in range(len(self.data[n])):
                newitem = QTableWidgetItem(self.data[n][m])
                self.setItem(n,m,newitem)
        self.setHorizontalHeaderLabels(['Complexité','Fitness','Equation'])

class Optimisation(QDialog):
    def __init__(self,parent=None):
        super(Optimisation,self).__init__(parent)
        god = QVBoxLayout(self)
        layout = QHBoxLayout()
        god.addLayout(layout)
        s1 = QVBoxLayout()
        s2 = QVBoxLayout()

        popsize = QLineEdit()
        concurr = QLineEdit()

        s1.addWidget(QLabel("Pop size:"))
        s1.addWidget(popsize)

        s2.addWidget(QLabel("Concurrency:"))
        s2.addWidget(concurr)


        layout.addLayout(s1)
        layout.addLayout(s2)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        god.addWidget(buttons)

    def params(self):
        return 0


    @staticmethod
    def get_params(Parent=None):
        dialog = Optimisation()
        result = dialog.exec_()
        params = dialog.params()
        return (result, params)

#class Parameters:
#    def __init__(self):
#        self.mode_global = False
#        self.lastNodeClicked = ''
#        self.mode_cntrt = False
#        self.click1 = ''
#        self.click2 = ''


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("RFGraph")

        #self.flash = Parameters()
        #self.flash.mode_global = ...

        self.mg = False
        self.lastNodeClicked=""
        self.mode_cntrt = False
        self.click1 = ''
        self.click2 = ''


        self.main_widget = QtGui.QWidget(self)


        grid = QtGui.QGridLayout(self.main_widget)
        self.RFG = graphs.RFGraphCanvas(self.main_widget, width=37, height=30, dpi=200)
        self.ts_slider = QtGui.QSlider(QtCore.Qt.Horizontal,self.main_widget)
        self.ds_slider = QtGui.QSlider(QtCore.Qt.Horizontal,self.main_widget)
        self.ts_slider.setValue(50)
        self.ds_slider.setValue(50)
        self.forbidden_edge=[]
        grid.setSpacing(10)

        grid.addWidget(self.RFG,0,0,8,60)


        ts_lab = QtGui.QLabel('Importance des arcs : ')
        grid.addWidget(ts_lab,7,0,1,2)
        grid.addWidget(self.ts_slider,7,2,1,57)

        ds_lab = QtGui.QLabel('Compromis : ')
        ds_lab_cmplx = QtGui.QLabel('Complexité')
        ds_lab_fitness = QtGui.QLabel('Fitness')
        grid.addWidget(ds_lab,8,0)
        grid.addWidget(ds_lab_cmplx,8,1)
        grid.addWidget(self.ds_slider,8,2,1,57)
        grid.addWidget(ds_lab_fitness, 8, 59,1,1)


        data_tmp=fdata.equacolPOs[:,np.ix_([0,1,4])]
        data=[]
        for i in range(len(data_tmp)):
            data.append(data_tmp[i][0])

        self.table = MyTable(data,len(data),3)
        for i in range(len(data[5])):
            self.table.item(5,i).setBackground(QtGui.QColor(150,150,150))

        self.table.itemClicked.connect(self.tableClicked)
        grid.addWidget(self.table, 0, 60, 6, 60)

        self.fitg = graphs.FitCanvas(self.main_widget, width=37, height=30, dpi=200)
        grid.addWidget(self.fitg,6,60,6,60)

        self.button1 = QtGui.QPushButton('Compromis', self)
        self.button2 = QtGui.QPushButton('Fitness', self)
        self.button3 = QtGui.QPushButton('Complexité', self)
        self.button4 = QtGui.QPushButton('Optimisation µGP', self)
        self.button5 = QtGui.QPushButton('Modeles Locaux', self)
        self.button6 = QtGui.QPushButton('Modele Global', self)
        self.button7 = QtGui.QPushButton('Ajout contrainte', self)
        self.button8 = QtGui.QPushButton('Changer d\'equation', self)

        self.button7.clicked.connect(self.clickAjContrainte)

        grid.addWidget(self.button1,9,0,1,15)
        grid.addWidget(self.button2, 9, 15,1,15)
        grid.addWidget(self.button3, 9, 30,1,15)
        grid.addWidget(self.button4, 9, 45,1,15)
        grid.addWidget(self.button5, 10, 0, 1, 30)
        grid.addWidget(self.button6, 10, 30, 1, 30)
        grid.addWidget(self.button7, 11, 0, 1, 30)
        grid.addWidget(self.button8, 11, 30, 1, 30)



        self.ts_slider.valueChanged.connect(self.SliderMoved)
        self.ds_slider.valueChanged.connect(self.SliderMoved)

        self.button6.clicked.connect(self.clickModGlobal)
        self.button4.clicked.connect(self.clickOptmuGP)

        self.RFG.fig.canvas.mpl_connect('button_press_event', self.onClick)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def clickFitness(self):
        pass

    def clickCompromis(self):
        pass

    def clickCmplx(self):
        pass

    def clickOptmuGP(self):
        opt_params = Optimisation.get_params()

    def clickModLocaux(self):
        pass

    def clickModGlobal(self):
        self.fitg.mg = True

    def clickAjContrainte(self):
        if (not self.mode_cntrt):
            self.mode_cntrt = True
        else:
            self.mode_cntrt = False

    def clickChangeEq(self):
        pass

    def onClick(self, event, radius=0.005):
        #TODO  affichage du nom du noeud selectionné + changer couleur
        (x, y) = (event.xdata, event.ydata)


        dst = [(pow(x - self.RFG.pos[node][0], 2) + pow(y - self.RFG.pos[node][1], 2),node) for node in self.RFG.G.node]
        if len(list(filter(lambda x: x[0] < 0.0005, dst))) == 0 :
            return
        nodeclicked = min(dst,key=(lambda x: x[0]))[1]


        if self.lastNodeClicked != "":
            pass
            #Change color back
        self.lastNodeClicked = nodeclicked


        if (not self.mode_cntrt):
            #Ceci est un test pour le merge
            print('action:', nodeclicked)
            self.fitg.last_clicked = nodeclicked
            data_tmp = fdata.equacolOs[np.ix_(fdata.equacolOs[:, 2] == [nodeclicked], [0, 1, 3])]
            graphs.curr_tabl = fdata.equacolOs[np.ix_(fdata.equacolOs[:, 2] == [nodeclicked], [0, 1, 3, 4])]
            data = []
            for i in range(len(data_tmp)):
                data.append(data_tmp[i])
            self.table.data = data
            self.table.setmydata()
            self.RFG.figure.canvas.draw()
            self.fitg.setCurrentTable(self.table)
        else:
            pass
            #if (self.click1 == ''):
            #    self.click1 = candidates[0]
            #elif (self.click2 == ''):
            #    self.click2 = candidates[0]
            #else:
            #    print('click1:', self.click1, ' click2:', self.click2)
            #    self.click1 = ''
            #    self.click2 = ''
            #    mode_cntrt = False



    def SliderMoved(self, value):
        self.RFG.updateGraph(self.ts_slider.value()/100.0,self.ds_slider.value()/100.0)
        self.RFG.figure.canvas.draw()


    def tableClicked(self,cellClicked):
        self.fitg.fitplot(cellClicked.row())


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

