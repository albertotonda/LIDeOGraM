#-*- coding: utf-8
from Help import Help
from OptimisationCanvas import OptimisationCanvas
from ErrorConstraint import ErrorConstraint
from Network import Network
import numpy as np
from optimModGlobal import OptimModGlobal
import observers

class RFGraph_Controller(observers.Subject,observers.Observer):
    def __init__(self,modApp,vwApp):
        self.modApp=modApp
        self.vwApp=vwApp

    def clickHelp(self):
        self.modApp.help_params = Help.get_params()

    # TODO
    def clickFitness(self):
        print("clic fitness")
        self.modApp.ColorMode='Fit'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.drawEdges()
        self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        self.vwApp.buttonFitness.setStyleSheet("background-color: grey")
        self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        self.notifyObs({"click":"fitness"})

    # TODO
    def clickCompromis(self):
        print("clic Compr")
        self.modApp.ColorMode='Compr'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.drawEdges()
        self.vwApp.buttonCompromis.setStyleSheet("background-color: grey")
        self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        self.notifyObs({"click":"compromis"})



    # TODO
    def clickCmplx(self):
        print("clic Complx")
        self.modApp.ColorMode='Cmplx'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.drawEdges()
        self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        self.vwApp.buttonComplexite.setStyleSheet("background-color: grey")
        self.notifyObs({"click":"cmplx"})


    # TODO
    def clickOptmuGP(self):
        #self.modApp.opt_params = OptimisationCanvas.get_params()
        optModGlob = OptimModGlobal(self.modApp)
        optModGlob.startOptim()

    # TODO
    def clickHideModGlobal(self):
        self.modApp.showGlobalModel = False
        self.notifyObs({"click":"hideglobal"})


    # TODO Affiche le modèle d'équation global
    def clickShowModGlobal(self):
        self.modApp.showGlobalModel = True
        self.notifyObs({"click":"showglobal"})


    # TODO Enlève le lien entre les noeuds choisis
    def clickRemoveLink(self, event, radius=0.0005):
        self.modApp.mode_cntrt = True
        self.modApp.selectContrTxt="Select node 1"
        self.notifyObs({"click":"rmlink"})


    def clickChangeEq(self):
        pass

    def onPick(self,event):
        pass


    def onMove(self,event):
        print(event)
        if(event.button==1 and self.modApp.lastNodeClicked != ''):
            print(self.modApp.lastNodeClicked)
            old_pos=self.modApp.pos[self.modApp.lastNodeClicked]
            self.modApp.pos[self.modApp.lastNodeClicked]=(event.xdata,event.ydata)

            self.modApp.lpos[self.modApp.lastNodeClicked] = (self.modApp.lpos[self.modApp.lastNodeClicked][0] - old_pos[0] + event.xdata,
                                                        self.modApp.lpos[self.modApp.lastNodeClicked][1] - old_pos[1] + event.ydata)

            self.vwApp.networkGUI.network.axes.clear()
            self.vwApp.networkGUI.network.updateNodes()
            self.vwApp.networkGUI.network.updateLabels()
            self.vwApp.networkGUI.network.drawEdges()
        else:
            print(event)



    def onClick(self, event, radius=0.001):
        # TODO  affichage du nom du noeud selectionné + changer couleur
        (x, y) = (event.xdata, event.ydata)
        if not x or not y :
            return
        print("x=",x," y=",y)

        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
               self.modApp.pos]
        self.modApp.NodetoConstrain = []
        if len(list(filter(lambda x: x[0] < radius, dst))) == 0:
            self.higlight(None, self.modApp.lastNodeClicked)
            self.modApp.lastNodeClicked=""
            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()
            return
        nodeclicked = min(dst, key=(lambda x: x[0]))[1]


        if self.modApp.lastNodeClicked != "":
            pass
            # Change color back
        #self.modApp.lastNodeClicked = nodeclicked

        if self.modApp.lastNodeClicked != "":
            self.higlight(nodeclicked, self.modApp.lastNodeClicked)
            self.modApp.lastNodeClicked = nodeclicked
            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()
            self.vwApp.networkGUI.network.axes.clear()
            self.vwApp.networkGUI.network.updateNodes()
            self.vwApp.networkGUI.network.updateLabels()
            self.vwApp.networkGUI.network.drawEdges()
        else:
            self.higlight(nodeclicked,None)
            self.modApp.lastNodeClicked = nodeclicked
            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()
            self.vwApp.networkGUI.network.axes.clear()
            self.vwApp.networkGUI.network.updateNodes()
            self.vwApp.networkGUI.network.updateLabels()
            self.vwApp.networkGUI.network.drawEdges()

            #Change color back



        if (self.modApp.mode_cntrt == True):
            self.modApp.NodeConstraints.append(nodeclicked)
            self.atLeastOnce=[]
            self.notEvenOnce =[]
            for i in self.modApp.edgelist_inOrder:
                if i[0] not in self.atLeastOnce:
                    self.atLeastOnce.append(i[0])
            for i in self.modApp.edgelist_inOrder:
                if i[1] not in self.notEvenOnce:
                    self.notEvenOnce.append(i[1])
            if self.modApp.NodeConstraints[0] in self.atLeastOnce:
                self.modApp.selectContrTxt = "Select node 2"
                if (len(self.modApp.NodeConstraints) == 2):
                    if self.modApp.NodeConstraints[1] in self.notEvenOnce:
                        self.constraint = " - ".join(self.modApp.NodeConstraints)
                        self.modApp.scrolledList.append(self.constraint)
                        self.modApp.selectContrTxt=""
                        self.modApp.mode_cntrt = False
                        self.modApp.NodeConstraints = []
                        self.modApp.computeEdgeBold()
                        self.modApp.computeNxGraph()
                        self.vwApp.networkGUI.network.axes.clear()
                        self.vwApp.networkGUI.network.updateNodes()
                        self.vwApp.networkGUI.network.updateLabels()
                        self.vwApp.networkGUI.network.drawEdges()
                        self.vwApp.updateView()
                        self.notifyObs({"click": {"node": self.modApp.NodeConstraints}})

                    else:
                        self.modApp.selectContrTxt=""
                        self.modApp.mode_cntrt = False
                        self.modApp.NodeConstraints = []
                        #self.modApp.error_params = ErrorConstraint.get_params()
            else:
                self.modApp.selectContrTxt=""
                self.modApp.mode_cntrt = False
                self.modApp.NodeConstraints = []
                #self.modApp.error_params = ErrorConstraint.get_params()

        if (not self.modApp.mode_cntrt):
            self.notifyObs({"click": {"node": nodeclicked}})
            print('action:', nodeclicked)
            data_tmp = self.modApp.equacolO[np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3])]
            self.modApp.curr_tabl = self.modApp.equacolO[
                np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3, 4])]
            data = []
            for i in range(len(data_tmp)):
                data.append(data_tmp[i])
            self.modApp.data = data
            self.vwApp.eqTableGUI.updateView()

    # TODO Réintègre le lien sélectionné
    def clickReinstateLink (self):
        if self.vwApp.scrolledListBox.currentText() == "Select link to reinstate":
            return
        else:
            link = self.modApp.scrolledList.pop(self.vwApp.scrolledListBox.currentIndex())
            self.notifyObs({"click": {"node": link}})

            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()
            self.vwApp.networkGUI.network.axes.clear()
            self.vwApp.networkGUI.network.updateNodes()
            self.vwApp.networkGUI.network.updateLabels()
            self.vwApp.networkGUI.network.drawEdges()
            self.vwApp.updateView()

    # TODO Change la couleur et la densité des "edges" en fonction du déplacement des sliders
    def SliderMoved(self, value):
        if( self.modApp.adjThresholdVal!=self.vwApp.adjThreshold_slider.value() / 100.0):
            self.modApp.adjThresholdVal=self.vwApp.adjThreshold_slider.value() / 100.0
        if(self.modApp.comprFitCmplxVal != self.vwApp.comprFitCmplx_slider.value() / 100.0 ):
            self.modApp.comprFitCmplxVal=self.vwApp.comprFitCmplx_slider.value() / 100.0
            self.modApp.computeComprEdgeColor()
            self.modApp.computeEdgeBold()
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()

    # TODO Affiche la courbe de l'équation sélectionnée
    def tableClicked(self, cellClicked):
        self.modApp.clicked_line=cellClicked.row()
        self.vwApp.fitGUI.updateView()
        #self.vwApp.networkGUI.updateView()

    # TODO Crée le surlignage des noeuds
    def higlight(self, new_node: str, old_node: str = None):
        self.modApp.G.clear()
        if old_node:
            self.modApp.nodeColor[(self.modApp.varnames.tolist()).index(old_node)] = self.modApp.old_color
        if new_node:
            self.modApp.old_color = self.modApp.nodeColor[(self.modApp.varnames.tolist()).index(new_node)]
            self.modApp.nodeColor[(self.modApp.varnames.tolist()).index(new_node)] = (1.0, 0, 0)

        self.vwApp.networkGUI.network.updateNodes()

    def fileQuit(self):
        self.vwApp.close()


    def closeEvent(self, ce):
        self.fileQuit()

