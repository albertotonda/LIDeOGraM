from PyQt4 import QtGui
from Gene_View import Gene_View
from Gene_Model import Gene_Model
from Gene_Controller import Gene_Controller
from QtConnectorGene import QtConnectorGene
from paramView import paramView
import sys

class exec_main():
    def __init__(self,qApp):
        self.qApp = qApp
        self.mod=Gene_Model()
        self.vwstart=paramView(self.mod,self)

    def continueMain(self):
        self.mod.searchClusters()
        self.vw=Gene_View(self.mod)
        self.ctr=Gene_Controller(self.mod,self.vw)
        qtc=QtConnectorGene(self.vw,self.ctr)


qApp = QtGui.QApplication(sys.argv)
m=exec_main(qApp)
sys.exit(qApp.exec_())