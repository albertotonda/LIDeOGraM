from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from NetworkGenes import NetworkGenes
class Gene_View(QtGui.QMainWindow):

    def __init__(self,modGene):
        self.modGene=modGene

        QtGui.QMainWindow.__init__(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("LIDeoGraM-Genomics")
        self.icon = QtGui.QIcon("../Icone.png")
        self.setWindowIcon(self.icon)

        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.main_widget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)

        self.networkGUI= NetworkGenes(self.modGene,self)
        self.gridLayout.addWidget(self.networkGUI, 0, 0, 1, 2)

        self.searchTxt = QtGui.QLineEdit()
        self.searchButton = QtGui.QPushButton("Search Gene")
        self.gridLayout.addWidget(self.searchTxt, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.searchButton, 2, 0, 1, 1)

        self.setCentralWidget(self.main_widget)
        self.updateView()
        self.show()

    def updateView(self):
        self.networkGUI.updateView()