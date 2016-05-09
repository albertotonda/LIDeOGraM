#-*- coding: utf-8
from PyQt4.QtGui import *

class EqTable(QTableWidget):
    def __init__(self, modApp, *args):
        self.modApp = modApp
        QTableWidget.__init__(self)


    def updateView(self):
        self.clear()
        self.setRowCount(len(self.modApp.data))
        self.setColumnCount(3)
        for n  in range(len(self.modApp.data)):
            for m in range(len(self.modApp.data[n])):
                newitem = QTableWidgetItem(self.modApp.data[n][m])
                self.setItem(n,m,newitem)
        self.setHorizontalHeaderLabels(['Complexité','Fitness','Equation'])
        self.resizeColumnsToContents()
        self.resizeRowsToContents()