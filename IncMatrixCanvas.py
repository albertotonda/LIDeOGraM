#-*- coding: utf-8
import sys
from collections import Counter

import pandas as pd
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pandas as pd

import re

from PyQt4.QtGui import *

class IncMatrixCanvas(QTableWidget):
    def __init__(self, modApp, vwApp):
        self.modApp = modApp
        self.vwApp = vwApp
        QTableWidget.__init__(self)



        # initiate table
        self.setWindowTitle("Tableau de correspondance")
        self.resize(*self.modApp.shapeIncMat)
        self.setRowCount(len(self.modApp.dataIncMat.index))
        self.setColumnCount(len(self.modApp.dataIncMat.columns))

        # set label
        self.setHorizontalHeaderLabels(self.modApp.dataIncMat.columns.values)
        self.setVerticalHeaderLabels(self.modApp.dataIncMat.index.tolist())

        for i in range(self.modApp.shapeIncMat[0]):
            self.setRowHeight(i, 15)
            for j in range(self.modApp.shapeIncMat[1]):
                self.setColumnWidth(j, 15)
                fnt = QFont()
                fnt.setPointSize(5)
                value = self.modApp.dataIncMat.ix[i, j]
                cell = QTableWidgetItem(value)
                cell.setFont(fnt)
                color = None
                if value == 1:
                    color = QColor.fromRgb(255, 0, 0)
                elif value == -1:
                    color = QColor.fromRgb(0, 0, 255)
                else:
                    color = QColor.fromRgb(255, 255, 255)
                cell.setBackgroundColor(color)
                cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                self.setItem(i, j, cell)

                # tooltip text
        self.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.horizontalHeaderItem(1).setToolTip("Column 2 ")

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
            kck = best_ind[col]
            print(kck)
            print(col)
            print(type(kck))
            print(self.modApp.dataIncMat.index.tolist().index(col))
            eqs.append(self.modApp.dataIncMat.index.tolist().index(col)+int(best_ind[col]))
        l = len(self.modApp.dataIncMat.index.tolist())
        diff = set(range(l)) - set(eqs)
        others = list(sorted(list(diff)))
        for i in others:
            eqs.append(i)
        #eqs contiens maintenant normalement le nouvel ordonanamcement.

        for i,k in enumerate(eqs) : #range(self.modApp.shapeIncMat[0]):
            self.setRowHeight(i, 15)
            for j in range(self.modApp.shapeIncMat[0]):
                self.setColumnWidth(j, 15)
                fnt = QFont()
                fnt.setPointSize(5)
                value = self.modApp.dataIncMat.ix[j, k]
                cell = QTableWidgetItem(value)
                cell.setFont(fnt)
                color = None
                if value == 1:
                    color = QColor.fromRgb(255, 0, 0)
                elif value == -1:
                    color = QColor.fromRgb(0, 0, 255)
                else:
                    color = QColor.fromRgb(255, 255, 255)
                cell.setBackgroundColor(color)
                cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                self.setItem(j, i, cell)

                # tooltip text
        self.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.horizontalHeaderItem(1).setToolTip("Column 2 ")

        # show table
        self.show()



