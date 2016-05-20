import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class AddConstraints(QWidget):
    def __init__(self):
        self.modApp.NodetoConstrain= []

    def addConstrainsts(self, event, radius=0.0005):
        # TODO  Ajout de la contrainte entre les noeuds
        (x, y) = (event.xdata, event.ydata)
        print("x=", x, " y=", y)

        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
               self.modApp.pos]
        if len(list(filter(lambda x: x[0] < radius, dst))) == 0:
            return
        nodeclicked = min(dst, key=(lambda x: x[0]))[1]

            # Change color back
        self.modApp.NodetoConstrain.append(nodeclicked)

        if (len(self.modApp.NodetoConstrain.append(nodeclicked) == 2)):
            self.vwApp.networkGUI.network.higlight(nodeclicked, self.modApp.lastNodeClicked)
        else:
            self.vwApp.networkGUI.network.higlight(nodeclicked, None)

            # Change color back
        self.lastNodeClicked = node

        if (not self.modApp.mode_cntrt):
            print('action:', nodeclicked)
            self.modApp.last_clicked = node
            data_tmp = self.modApp.equacolOs[np.ix_(self.modApp.equacolOs[:, 2] == [node], [0, 1, 3])]
            self.modApp.curr_tabl = self.modApp.equacolOs[
                np.ix_(self.modApp.equacolOs[:, 2] == [node], [0, 1, 3, 4])]
            data = []
            for i in range(len(data_tmp)):
                data.append(data_tmp[i])
            self.modApp.data = data
            self.vwApp.eqTableGUI.updateView()