#-*- coding: utf-8
from OptimisationCanvas import OptimisationCanvas
import numpy as np

class RFGraph_Controller:
    def __init__(self,modApp,vwApp):
        self.modApp=modApp
        self.vwApp=vwApp

    def clickFitness(self):
        pass

    def clickCompromis(self):
        pass

    def clickCmplx(self):
        pass

    def clickOptmuGP(self):
        self.modApp.opt_params = OptimisationCanvas.get_params()

    def clickModLocaux(self):
        pass

    def clickModGlobal(self):
        self.modApp.showGlobalModel = True

    def clickAjContrainte(self):
        if (not self.modApp.mode_cntrt):
            self.modApp.mode_cntrt = True
            self.vwApp.buttonAjtCntrt.setDown(True)
        else:
            self.modApp.mode_cntrt = False
            self.vwApp.buttonAjtCntrt.setDown(False)

    def clickChangeEq(self):
        pass

    def onClick(self, event, radius=0.0005):
        # TODO  affichage du nom du noeud selectionné + changer couleur
        (x, y) = (event.xdata, event.ydata)
        print("x=",x," y=",y)

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
            self.vwApp.networkGUI.network.higlight(nodeclicked,None)

            #Change color back
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

    def SliderMoved(self, value):
        self.modApp.adjThresholdVal=self.vwApp.adjThreshold_slider.value() / 100.0
        self.modApp.comprFitCmplxVal=self.vwApp.comprFitCmplx_slider.value() / 100.0
        self.vwApp.networkGUI.updateView()


    def tableClicked(self, cellClicked):
        self.modApp.clicked_line=cellClicked.row()
        self.vwApp.fitGUI.updateView()
        self.vwApp.networkGUI.updateView()

    def fileQuit(self):
        self.vwApp.close()


    def closeEvent(self, ce):
        self.fileQuit()

