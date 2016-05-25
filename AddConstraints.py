#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

class AddConstraint(QWidget):
    def __init__(self, modApp):
        self.modApp = modApp
        self.NodeConstraints= []

    def params(self):
        return 0

"""
from RFGraph_View import RFGraph_View
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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



           # TODO  Reconnaît les noeuds
        (x, y) = (event.xdata, event.ydata)
        print("x=", x, " y=", y)

        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
               self.modApp.pos]
        if len(list(filter(lambda x: x[0] < radius, dst))) == 0:
            return
        nodeclicked = min(dst, key=(lambda x: x[0]))[1]

            # TODO Change la couleur des 2 noeuds à contraindre
        self.modApp.NodetoConstrain.append(nodeclicked)

        if (len(self.modApp.NodetoConstrain.append(nodeclicked) ==1) or len(self.modApp.NodetoConstrain.append(nodeclicked)==2)):
            self.vwApp.networkGUI.network.higlight(nodeclicked, self.modApp.NodetoConstrain.append(nodeclicked))
        else:
            self.vwApp.networkGUI.network.higlight(nodeclicked, None)

        if (len(self.modApp.NodetoConstrain.append(nodeclicked) == 2):
            self.listeDeroulante.addItem(nodeclicked[1]"//" nodeclicked[2])
"""