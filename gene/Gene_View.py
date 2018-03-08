from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from NetworkGenes import NetworkGenes
from GeneExpressionCanvas import GeneExpressionCanvas
from Gene2DCanvas import Gene2DCanvas

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
        self.gridLayout.addWidget(self.networkGUI, 0, 0, 5, 1)

        self.searchTxt = QtGui.QLineEdit()
        self.searchButton = QtGui.QPushButton("Search Gene")
        self.gridLayout.addWidget(self.searchTxt, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.searchButton, 0, 2, 1, 1)

        self.geneExpCanv=GeneExpressionCanvas(self.modGene,self)
        self.gridLayout.addWidget(self.geneExpCanv,2,1,1,1)

        self.zoomWidget=QtGui.QWidget(self)
        self.hLayoutzoom = QtGui.QHBoxLayout(self.zoomWidget)
        self.cbZoom = QtGui.QCheckBox()
        self.cbZoom.setChecked(False)
        self.modGene.isZoom = self.cbZoom.isChecked()
        self.labZoom = QtGui.QLabel('Activate zoom')
        self.hLayoutzoom.addWidget(self.cbZoom)
        self.hLayoutzoom.addWidget(self.labZoom)
        self.gridLayout.addWidget(self.zoomWidget,3,1,1,1)




        self.gene2DCanv=Gene2DCanvas(self.modGene,self)
        self.gridLayout.addWidget(self.gene2DCanv,4,1,1,1)

        self.condWidget=QtGui.QWidget(self)
        self.hLayoutconds=QtGui.QHBoxLayout(self.condWidget)
        self.cond22h0Lab = QtGui.QLabel('22C 0h stationary phase:')
        self.cond22h0CB = QtGui.QCheckBox()
        c=0 in self.modGene.activCond
        self.cond22h0CB.setChecked(c)
        self.hLayoutconds.addWidget(self.cond22h0Lab)
        self.hLayoutconds.addWidget(self.cond22h0CB)

        self.cond22h6Lab = QtGui.QLabel('22C 6h stationary phase:')
        self.cond22h6CB = QtGui.QCheckBox()
        c = 3 in self.modGene.activCond
        self.cond22h6CB.setChecked(c)
        self.hLayoutconds.addWidget(self.cond22h6Lab)
        self.hLayoutconds.addWidget(self.cond22h6CB)

        self.cond30h0Lab = QtGui.QLabel('30C 0h stationary phase:')
        self.cond30h0CB = QtGui.QCheckBox()
        c = 6 in self.modGene.activCond
        self.cond30h0CB.setChecked(c)
        self.hLayoutconds.addWidget(self.cond30h0Lab)
        self.hLayoutconds.addWidget(self.cond30h0CB)

        self.cond30h6Lab = QtGui.QLabel('30C 6h stationary phase:')
        self.cond30h6CB = QtGui.QCheckBox()
        c = 9 in self.modGene.activCond
        self.cond30h6CB.setChecked(c)
        self.hLayoutconds.addWidget(self.cond30h6Lab)
        self.hLayoutconds.addWidget(self.cond30h6CB)

        self.gridLayout.addWidget(self.condWidget,1,1,1,2)

        self.currClustWidget = QtGui.QWidget(self)
        self.vLayoutCurrClust = QtGui.QVBoxLayout(self.currClustWidget)
        self.geneCurrClustLab = QtGui.QLabel("Genes in current cluster :")
        self.vLayoutCurrClust.addWidget(self.geneCurrClustLab)
        self.geneCurrClustList  = QtGui.QListWidget()
        self.vLayoutCurrClust.addWidget(self.geneCurrClustList)


        palette = self.geneCurrClustList.palette()
        palette.setColor(QtGui.QPalette.Highlight, Qt.white)
        self.geneCurrClustList.setPalette(palette)

        self.geneCurrClustList.setStyleSheet("QListView::item:selected { color: white; background: black  } QListView::item:hover { text-color: blue; background: grey  }")

        self.gridLayout.addWidget(self.currClustWidget,0,3,5,1)

        self.moveGeneWidget = QtGui.QWidget(self)
        self.vLayoutMoveButton = QtGui.QVBoxLayout(self.moveGeneWidget)
        self.removeGeneButton=QtGui.QPushButton(" > ")
        self.vLayoutMoveButton.addWidget(self.removeGeneButton)
        self.addGeneButton = QtGui.QPushButton(" < ")
        self.vLayoutMoveButton.addWidget(self.addGeneButton)
        self.gridLayout.addWidget(self.moveGeneWidget,0,4,5,1)


        self.notAssignedGeneWidget = QtGui.QWidget(self)
        self.vLayoutNotAssignedGene = QtGui.QVBoxLayout(self.notAssignedGeneWidget)
        self.geneNotAssignedLab = QtGui.QLabel("Genes not assigned:")
        self.vLayoutNotAssignedGene.addWidget(self.geneNotAssignedLab)
        self.geneNotAssignedList = QtGui.QListWidget()
        self.vLayoutNotAssignedGene.addWidget(self.geneNotAssignedList)

        self.gridLayout.addWidget(self.notAssignedGeneWidget, 0, 5, 5, 1)




        self.setCentralWidget(self.main_widget)
        self.networkGUI.updateView()
        self.show()

    def updateView(self):
        pass
        #self.networkGUI.updateView()