#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

class AddConstraint(QWidget):
    def __init__(self, modApp):
        self.modApp = modApp
        self.NodeConstraints= []


"""
class AddConstraints(RFGraph_View, QWidget):
    def __init__(self, modApp):
        self.modApp = modApp
        super(AddConstraints, self).__init__(RFGraph_View)
        self.modApp.NodetoConstrain= []
        self.modApp.ButtonAjtCntrt= self.buttonAjtCntrt


    def addConstrainsts(self, event, radius=0.0005):
       # TODO Ajout de la contrainte aux noeuds
        for i in range(len(self.modApp.NodetoConstrain.pareto)):
            for j in range(len(self.modApp.NodetoConstrain.pareto[i])):
                i = i + 1
                if (len(self.modApp.NodetoConstrain.pareto[i])==2):
"""