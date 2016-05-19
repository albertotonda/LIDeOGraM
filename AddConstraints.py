#-*- coding: utf- 8

from PyQt4 import QtGui

def __init__(self):
    self.node_one=
    self.node_two=
    self.link= i


def onClick(self, event, radius=0.0005):
    # TODO  affichage du nom du noeud selectionné + changer couleur
    (x, y) = (event.xdata, event.ydata)
    print("x=", x, " y=", y)

    dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
           self.modApp.pos]
    if len(list(filter(lambda x: x[0] < radius, dst))) == 0:
        return
    nodeclicked = min(dst, key=(lambda x: x[0]))[1]

    if self.modApp.lastNodeClicked != "":
        pass
        # Change color back
    self.modApp.lastNodeClicked = nodeclicked

    if self.modApp.lastNodeClicked != "":
        self.vwApp.networkGUI.network.higlight(nodeclicked, self.modApp.lastNodeClicked)
    else:
        self.vwApp.networkGUI.network.higlight(nodeclicked, None)

        # Change color back
    self.lastNodeClicked = nodeclicked

    if (not self.modApp.mode_cntrt):
        print('action:', nodeclicked)
        self.modApp.last_clicked = nodeclicked
        data_tmp = self.modApp.equacolOs[np.ix_(self.modApp.equacolOs[:, 2] == [nodeclicked], [0, 1, 3])]
        self.modApp.curr_tabl = self.modApp.equacolOs[
            np.ix_(self.modApp.equacolOs[:, 2] == [nodeclicked], [0, 1, 3, 4])]
        data = []
        for i in range(len(data_tmp)):
            data.append(data_tmp[i])
        self.modApp.data = data
        self.vwApp.eqTableGUI.updateView()
    else:
        pass
        # if (self.click1 == ''):
        #    self.click1 = candidates[0]
        # elif (self.click2 == ''):
        #    self.click2 = candidates[0]
        # else:
        #    print('click1:', self.click1, ' click2:', self.click2)
        #    self.click1 = ''
        #    self.click2 = ''
        #    mode_cntrt = False



class AddConstraints:
    pass