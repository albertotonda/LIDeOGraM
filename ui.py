#-*- coding: utf-8
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from math import *
import data as fdata
import graphs
import numpy as np


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
                #print('n:',n,' m:',m,' case:',self.data[n][m])
                newitem = QTableWidgetItem(self.data[n][m])
                self.setItem(n,m,newitem)
        self.setHorizontalHeaderLabels(['Complexité','Fitness','Equation'])

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("RFGraph")

        self.mg = False

        self.click1 = ''
        self.click2 = ''
        self.main_widget = QtGui.QWidget(self)


        #l = QtGui.QVBoxLayout(self.main_widget)
        grid = QtGui.QGridLayout(self.main_widget)
        self.RFG = graphs.RFGraphCanvas(self.main_widget, width=37, height=30, dpi=200)
        self.ts_slider = QtGui.QSlider(QtCore.Qt.Horizontal,self.main_widget)
        self.ds_slider = QtGui.QSlider(QtCore.Qt.Horizontal,self.main_widget)
        self.ts_slider.setValue(50)
        self.ds_slider.setValue(50)
        self.forbidden_edge=[]
        #l.addWidget(self.RFG)
        #grid_w=QtGui.QWidget(self.main_widget)
        #grid=QtGui.QGridLayout(grid_w)
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


        #data = {'col1': ['1', '2', '3'], 'col2': ['4', '5', '6'], 'col3': ['7', '8', '9'],'col4':['1','2','3'], 'col5':['4','5','6'], 'col6':['7','8','9'],'col1156146516':['1','2','3'], 'col23':['4','5','6'], 'col38':['7','8','9']}
        #data={}
        data_tmp=fdata.equacolPOs[:,np.ix_([0,1,4])]
        data=[]
        for i in range(len(data_tmp)):
            data.append(data_tmp[i][0])
        self.table = MyTable(data,len(data),3)
        for i in range(len(data[5])):
            self.table.item(5,i).setBackground(QtGui.QColor(150,150,150))

        self.table.itemClicked.connect(self.tableClicked)
        #self.table.connect(self.tableClicked)
        grid.addWidget(self.table, 0, 60, 6, 60)

        self.fitg = graphs.FitCanvas(self.main_widget, width=37, height=30, dpi=200)
        grid.addWidget(self.fitg,6,60,6,60)

        self.button1=QtGui.QPushButton('Compromis', self)
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

        #eq=QtGui.QTextEdit()
        #grid.addWidget(eq,1,8,7,40)


        #l.addWidget(grid_w)

        #ts_w=QtGui.QWidget(self.main_widget)
        #ts_l=QtGui.QHBoxLayout(ts_w)
        #ts_lab=QtGui.QLabel('Importance des arcs : ')
        #ts_l.addWidget(ts_lab)
        #ts_l.addWidget(self.ts_slider)
        #l.addWidget(ts_w)


        #ds_w=QtGui.QWidget(self.main_widget)
        #ds_l = QtGui.QHBoxLayout(ds_w)
        #ds_lab = QtGui.QLabel('Compromis : ')
        #ds_l.addWidget(ds_lab)
        #ds_l.addWidget(self.ds_slider)
        #l.addWidget(ds_w)

        self.ts_slider.valueChanged.connect(self.SliderMoved)
        self.ds_slider.valueChanged.connect(self.SliderMoved)

        self.button6.clicked.connect(self.clickModGlobal)

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
        pass

    def clickModLocaux(self):
        pass

    def clickModGlobal(self):
        self.fitg.mg = True

    def clickAjContrainte(self):
        global mode_cntrt
        mode_cntrt = True

    def clickChangeEq(self):
        pass

    def onClick(self, event, radius=0.005):
        global last_clicked
        global curr_tabl
        global mode_cntrt
        (x, y) = (event.xdata, event.ydata)

        print('clicked', event.xdata)
        candidates = []

        for i in self.RFG.G.node:
            node = self.RFG.pos[i]
            distance = pow(x - node[0], 2) + pow(y - node[1], 2)
            if distance < radius:
                candidates.append(i)
                # print(i)

        print('list:', candidates)
        if (len(candidates) > 1):
            self.onClick(event, radius / 2)
        elif (len(candidates) == 0):

            return
        else:
            if (mode_cntrt == False):
                print('action:', candidates, ' ', candidates[0])
                last_clicked = candidates[0]
                # print('last_clicked_affected_to:',last_clicked)
                data_tmp = fdata.equacolOs[np.ix_(fdata.equacolOs[:, 2] == candidates, [0, 1, 3])]
                curr_tabl = fdata.equacolOs[np.ix_(fdata.equacolOs[:, 2] == candidates, [0, 1, 3, 4])]
                data = []
                for i in range(len(data_tmp)):
                    data.append(data_tmp[i])
                # print(data)
                self.table.data = data
                self.table.setmydata()
                self.RFG.figure.canvas.draw()
                self.fitg.setCurrentTable(self.table)
            else:
                if (self.click1 == ''):
                    self.click1 = candidates[0]
                elif (self.click2 == ''):
                    self.click2 = candidates[0]
                else:
                    print('click1:', self.click1, ' click2:', self.click2)
                    self.click1 = ''
                    self.click2 = ''
                    mode_cntrt = False


            # refreshGraph()

    def onpick(self, event):
        """Deal with pick events"""
        print("You picked {:s}, which has color={:s} and linewidth={:f}".format(event.artist,
                                                                                event.artist.get_color(),
                                                                                event.artist.get_linewidth()))
        new_color = 'r' if event.artist.get_color() == 'k' else 'k'
        print("I will change the color to color={:s}".format(new_color))
        event.artist.set_color(new_color)
        plt.draw()
        print("A pick-event has access to the mouse event: to prove it, I pass it to 'onclick'")
        self.onClick(event.mouseevent)
        print("----> That was actually from within 'onpick'!")

    def SliderMoved(self, value):
        #print('ts=',self.ts_slider.value())
        #print('ds=', self.ds_slider.value())
        self.RFG.updateGraph(self.ts_slider.value()/100.0,self.ds_slider.value()/100.0)
        self.RFG.figure.canvas.draw()
    def tableClicked(self,cellClicked):
        self.fitg.fitplot(cellClicked.row())



    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

