from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *


class paramView(QtGui.QMainWindow):

    def __init__(self,modGene,execmain):
        self.modGene=modGene
        self.execmain=execmain

        QtGui.QMainWindow.__init__(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("LIDeoGraM-Genomics")
        self.icon = QtGui.QIcon("../Icone.png")
        self.setWindowIcon(self.icon)

        #self.setWindowState(QtCore.Qt.WindowMaximized)

        self.main_widget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)

        self.thresholdLab=QtGui.QLabel('Variance threshold on genes (0-∞):')
        self.thresholdTxt=QtGui.QLineEdit()
        self.gridLayout.addWidget(self.thresholdLab,0,0,1,1)
        self.gridLayout.addWidget(self.thresholdTxt,0,1,1,1)

        self.clusterSizeLab=QtGui.QLabel('Min cluster size (2-∞):')
        self.clusterSizeTxt = QtGui.QLineEdit()
        self.gridLayout.addWidget(self.clusterSizeLab,1,0,1,1)
        self.gridLayout.addWidget(self.clusterSizeTxt,1,1,1,1)

        self.cond22h0Lab = QtGui.QLabel('22C 0h stationary phase:')
        self.cond22h0CB=QtGui.QCheckBox()
        self.cond22h0CB.setChecked(True)
        self.gridLayout.addWidget(self.cond22h0Lab,2,0,1,1)
        self.gridLayout.addWidget(self.cond22h0CB,2,1,1,1)

        self.cond22h6Lab = QtGui.QLabel('22C 6h stationary phase:')
        self.cond22h6CB = QtGui.QCheckBox()
        self.cond22h6CB.setChecked(True)
        self.gridLayout.addWidget(self.cond22h6Lab,3,0,1,1)
        self.gridLayout.addWidget(self.cond22h6CB,3,1,1,1)

        self.cond30h0Lab = QtGui.QLabel('30C 0h stationary phase:')
        self.cond30h0CB = QtGui.QCheckBox()
        self.cond30h0CB.setChecked(True)
        self.gridLayout.addWidget(self.cond30h0Lab,4,0,1,1)
        self.gridLayout.addWidget(self.cond30h0CB,4,1,1,1)

        self.cond30h6Lab = QtGui.QLabel('30C 6h stationary phase:')
        self.cond30h6CB = QtGui.QCheckBox()
        self.cond30h6CB.setChecked(True)
        self.gridLayout.addWidget(self.cond30h6Lab,5,0,1,1)
        self.gridLayout.addWidget(self.cond30h6CB,5,1,1,1)

        self.validateButton = QtGui.QPushButton("Start clustering")
        self.gridLayout.addWidget(self.validateButton, 6, 0, 1, 2)





        # self.networkGUI= NetworkGenes(self.modGene,self)
        # self.gridLayout.addWidget(self.networkGUI, 0, 0, 3, 1)
        #
        # self.searchTxt = QtGui.QLineEdit()
        # self.searchButton = QtGui.QPushButton("Search Gene")
        # self.gridLayout.addWidget(self.searchTxt, 0, 1, 1, 1)
        # self.gridLayout.addWidget(self.searchButton, 0, 2, 1, 1)
        #
        # self.geneExpCanv=GeneExpressionCanvas(self.modGene,self)
        # self.gridLayout.addWidget(self.geneExpCanv,1,1,1,1)
        #
        # self.gene2DCanv=Gene2DCanvas(self.modGene,self)
        # self.gridLayout.addWidget(self.gene2DCanv,2,1,1,1)



        self.setCentralWidget(self.main_widget)
        self.validateButton.clicked.connect(self.vwstartClicked)

        self.show()

    def vwstartClicked(self):
        self.modGene.thresholdVar = float(self.thresholdTxt.text())
        self.modGene.minClusterSize = int(self.clusterSizeTxt.text())
        self.modGene.activCond = []
        self.modGene.activCondShow = []
        if (self.cond22h0CB.checkState()):
            self.modGene.activCond.extend([0,1,2])
            self.modGene.activCondShow.extend([0, 1,2])
        if (self.cond22h6CB.checkState()):
            self.modGene.activCond.extend([3,4,5])
            self.modGene.activCondShow.extend([3,4,5])
        if (self.cond30h0CB.checkState()):
            self.modGene.activCond.extend([6,7,8])
            self.modGene.activCondShow.extend([6,7,8])
        if (self.cond30h6CB.checkState()):
            self.modGene.activCond.extend([9,10,11])
            self.modGene.activCondShow.extend([9,10,11])
        self.execmain.continueMain()
