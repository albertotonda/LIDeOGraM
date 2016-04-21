from PyQt4.QtGui import *

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