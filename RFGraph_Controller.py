#-*- coding: utf-8
from Optimisation import Optimisation

class RFGraph_Controller:
    def __init__(self,modApp,vwApp):
        pass

    def clickFitness(self):
        pass

    def clickCompromis(self):
        pass

    def clickCmplx(self):
        pass

    def clickOptmuGP(self):
        opt_params = Optimisation.get_params()

    def clickModLocaux(self):
        pass

    def clickModGlobal(self):
        self.modApp.showGlobalModel = True

    def clickAjContrainte(self):
        if (not self.modApp.mode_cntrt):
            self.modApp.mode_cntrt = True
        else:
            self.modApp.mode_cntrt = False

    def clickChangeEq(self):
        pass

    def onClick(self, event, radius=0.005):
        # TODO  affichage du nom du noeud selectionné + changer couleur
        (x, y) = (event.xdata, event.ydata)

        dst = [(pow(x - self.RFG.pos[node][0], 2) + pow(y - self.RFG.pos[node][1], 2), node) for node in
               self.RFG.G.node]
        if len(list(filter(lambda x: x[0] < 0.0005, dst))) == 0:
            return
        nodeclicked = min(dst, key=(lambda x: x[0]))[1]

        if self.modApp.lastNodeClicked != "":
            pass
            # Change color back
        self.modApp.lastNodeClicked = nodeclicked

        if (not self.modApp.mode_cntrt):
            print('action:', nodeclicked)
            self.modApp.last_clicked = nodeclicked
            data_tmp = self.modApp.equacolOs[np.ix_(self.modApp.equacolOs[:, 2] == [nodeclicked], [0, 1, 3])]
            NetworkCanvas.curr_tabl = self.modApp.equacolOs[
                np.ix_(self.modApp.equacolOs[:, 2] == [nodeclicked], [0, 1, 3, 4])]
            data = []
            for i in range(len(data_tmp)):
                data.append(data_tmp[i])
            self.table.data = data
            self.table.setmydata()
            self.RFG.figure.canvas.draw()
            self.fitg.setCurrentTable(self.table)
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

    def SliderMoved(self, value):
        self.RFG.updateGraph(self.ts_slider.value() / 100.0, self.ds_slider.value() / 100.0)
        self.RFG.figure.canvas.draw()

    def tableClicked(self, cellClicked):
        print('tableclicked')
        self.fitg.fitplot(cellClicked.row())