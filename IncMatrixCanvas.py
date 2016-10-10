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
            self.setRowHeight(i, 5)
            for j in range(self.modApp.shapeIncMat[1]):
                self.setColumnWidth(j, 5)
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
                cell.setToolTip(self.modApp.datumIncMat.irow(i)[3])
                self.setItem(i, j, cell)

                # tooltip text
        self.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.horizontalHeaderItem(1).setToolTip("Column 2 ")

        # show table
        self.show()


