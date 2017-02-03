#-*- coding: utf-8
import sys
from collections import Counter

import pandas as pd
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pandas as pd

import re

# TODO remove vertical header

from PyQt4.QtGui import *

class IncMatrixCanvas(QTableWidget):
    def __init__(self, modApp, vwApp):
        self.modApp = modApp
        self.vwApp = vwApp
        QTableWidget.__init__(self)



        # initiate table
        self.setWindowTitle("Tableau de correspondance")
        self.setRowCount(len(self.modApp.dataIncMat.index))
        self.setColumnCount(len(self.modApp.dataIncMat.columns)+3)

        # set label
        self.setHorizontalHeaderLabels(["Fitness","Complexity","Name"]+self.modApp.dataIncMat.columns.values.tolist())
        #self.setVerticalHeaderLabels(self.modApp.dataIncMat.index.tolist())

        for i in range(self.modApp.shapeIncMat[0]):
            self.setRowHeight(i, 15)
            for j in range(self.modApp.shapeIncMat[1]+3):
                if j == 0:
                    self.setColumnWidth(j, 15)
                    color = QColor.fromRgb(0, 255, 0)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue
                if j == 1:
                    self.setColumnWidth(j, 15)
                    color = QColor.fromRgb(0, 255, 0)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue
                if j == 2:
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    self.setItem(i, j, cell)
                    continue
                self.setColumnWidth(j, 15)
                fnt = QFont()
                fnt.setPointSize(5)
                value = self.modApp.dataIncMat.ix[i, j-3]
                cell = QTableWidgetItem(value)
                cell.setFont(fnt)
                color = None
                if value == 1:
                    color = QColor.fromRgb(0, 255, 0)
                elif value == -1:
                    color = QColor.fromRgb(0, 0, 255)
                else:
                    color = QColor.fromRgb(255, 255, 255)
                cell.setBackgroundColor(color)
                cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                self.setItem(i, j, cell)

                # tooltip text
        #self.horizontalHeaderItem(0).setToolTip("Column 1 ")
#        self.horizontalHeaderItem(1).setToolTip("Column 2 ")

        # show table
        self.show()



    def updateView(self):
        best_ind = self.modApp.best_indv
        if best_ind == []: return
        tableOrder = self.modApp.dataIncMat.columns
        eqs = []
        for place, col in enumerate(tableOrder):
            if col == "Temperature": continue
            if col == "Age" : continue
            eqs.append(self.modApp.dataIncMat.index.tolist().index(col)+int(best_ind[col]))
        l = len(self.modApp.dataIncMat.index.tolist())
        gmodelSize = len(eqs)
        diff = set(range(l)) - set(eqs)
        others = list(sorted(list(diff)))
        for i in others:
            eqs.append(i)
        #eqs contiens maintenant normalement le nouvel ordonanamcement.
        nameOrder = []
        for i in eqs:
            nameOrder.append(self.modApp.dataIncMat.index.tolist()[i])

        #self.setVerticalHeaderLabels(nameOrder)

        for i,k in enumerate(eqs) : #range(self.modApp.shapeIncMat[0]):
            self.setRowHeight(i, 15)
            for j in range(self.modApp.shapeIncMat[1] + 3):
                if j == 0:
                    self.setColumnWidth(j, 15)
                    color = QColor.fromRgb(0, 255, 0)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue
                if j == 1:
                    self.setColumnWidth(j, 15)
                    color = QColor.fromRgb(0, 255, 0)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue
                if j == 2:
                    if i < gmodelSize:
                        t = [0, 0, 0]
                    else:
                        t = [125, 125, 125]
                    cell = QTableWidgetItem(nameOrder[i])
                    cell.setTextColor(QColor.fromRgb(*t))
                    self.setItem(i, j, cell)
                    continue
                self.setColumnWidth(j, 15)
                fnt = QFont()
                fnt.setPointSize(5)
                value = self.modApp.dataIncMat.iloc[k, j-3]
                cell = QTableWidgetItem(value)
                cell.setFont(fnt)

                #Si on depasse gmodelSize, nous ne somme plus dans le model global mais dans les restes, on attenu donc la couleurs
                if i < gmodelSize:
                    g = [0,255,0]
                    b = [0,0,255]
                else:
                    g = [200,225,200]
                    b = [200,200,225]
                if value == 1:
                    color = QColor.fromRgb(*g)
                elif value == -1:
                    color = QColor.fromRgb(*b)
                else:
                    color = QColor.fromRgb(255, 255, 255)
                cell.setBackgroundColor(color)
                cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                self.setItem(i, j, cell)

        self.show()



