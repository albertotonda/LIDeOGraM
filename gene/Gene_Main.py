from PyQt4 import QtGui
from Gene_View import Gene_View
from Gene_Model import Gene_Model
from Gene_Controller import Gene_Controller
from QtConnectorGene import QtConnectorGene
import sys

qApp = QtGui.QApplication(sys.argv)
mod=Gene_Model()
vw=Gene_View(mod)
ctr=Gene_Controller(mod,vw)
qtc=QtConnectorGene(vw,ctr)
sys.exit(qApp.exec_())
a=4