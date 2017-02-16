#-*- coding: utf-8
from Help import Help
from PyQt4.QtCore import QCoreApplication
from OptimisationCanvas import OptimisationCanvas
from ErrorConstraint import ErrorConstraint
from Network import Network
import numpy as np
from OptimModGlobal import OptimModGlobal
import threading

class RFGraph_Controller:
    def __init__(self,modApp,vwApp):
        self.modApp=modApp
        self.vwApp=vwApp
        self.onMoveMutex = threading.Lock()

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

    # TODO
    def clickCompromis(self):
        print("clic Compr")
        self.modApp.ColorMode='Compr'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.drawEdges()
        self.vwApp.buttonCompromis.setStyleSheet("background-color: grey")
        self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        self.vwApp.buttonComplexite.setStyleSheet("background-color: None")


    # TODO
    def clickCmplx(self):
        print("clic Complx")
        self.modApp.ColorMode='Cmplx'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.drawEdges()
        self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        self.vwApp.buttonComplexite.setStyleSheet("background-color: grey")

    # TODO
    def clickOptmuGP(self):
        #self.modApp.opt_params = OptimisationCanvas.get_params()
        optModGlob = OptimModGlobal(self.modApp)
        self.modApp.showGlobalModel=True
        self.modApp.best_indv=optModGlob.startOptim()
        self.modApp.globalModelView=True
        self.modApp.bestindvToSelectedEq()
        self.modApp.computeGlobalView()
        self.vwApp.updateView()

    # TODO
    def clickHideModGlobal(self):
        self.modApp.showGlobalModel = False

    # TODO Affiche le modèle d'équation global
    def clickShowModGlobal(self):
        self.modApp.showGlobalModel = True

    # TODO Enlève le lien entre les noeuds choisis
    def clickRemoveLink(self, event, radius=0.0005):
        self.modApp.mode_cntrt = True
        self.modApp.selectContrTxt="Select node 1"

    def clickChangeEq(self):
        print("clickChangeEq")
        self.modApp.mode_changeEq=True

    def onPick(self,event):
        pass


    def onMove(self,event):
        #print(event)

        if(event.button==1 and self.modApp.lastNodeClicked != ''):
            if (self.onMoveMutex.locked() or event.inaxes == None):
                return
            self.onMoveMutex.acquire()
            old_pos = self.modApp.pos[self.modApp.lastNodeClicked]
            self.modApp.pos[self.modApp.lastNodeClicked] = (event.xdata, event.ydata)

            self.modApp.lpos[self.modApp.lastNodeClicked] = (
                self.modApp.lpos[self.modApp.lastNodeClicked][0] - old_pos[0] + event.xdata,
                self.modApp.lpos[self.modApp.lastNodeClicked][1] - old_pos[1] + event.ydata)
            #print("old_pos:"+str(old_pos))
            self.modApp.fpos[self.modApp.lastNodeClicked] = (
                self.modApp.fpos[self.modApp.lastNodeClicked][0] - old_pos[0] + event.xdata,
                self.modApp.fpos[self.modApp.lastNodeClicked][1] - old_pos[1] + event.ydata)

            if (self.modApp.globalModelView):
                self.vwApp.updateView()
            else:
                self.vwApp.networkGUI.network.axes.clear()
                self.vwApp.networkGUI.network.updateNodes()
                self.vwApp.networkGUI.network.updateLabels()
                self.vwApp.networkGUI.network.drawEdges()
                self.vwApp.networkGUI.fig.canvas.draw()
            QCoreApplication.processEvents()
            self.onMoveMutex.release()
        else:
            pass
            #print(event)


    def onClick(self, event, radius=0.001):
        # TODO  affichage du nom du noeud selectionné + changer couleur
        print("clicked")
        (x, y) = (event.xdata, event.ydata)
        if  x == None or y == None :
            return
        print("x=",x," y=",y)

        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
               self.modApp.pos]
        self.modApp.NodetoConstrain = []
        if len(list(filter(lambda x: x[0] < radius, dst))) == 0:
            self.higlight(None, self.modApp.lastNodeClicked)
            self.modApp.lastNodeClicked=""
            self.modApp.clicked_line=-1
            self.modApp.computeEdgeBold()
            if(not self.modApp.globalModelView):
                self.modApp.computeNxGraph()
            self.vwApp.networkGUI.fig.canvas.draw()
            self.modApp.data=[]
            self.vwApp.eqTableGUI.updateView()
            self.vwApp.fitGUI.updateView()
            self.vwApp.clickedNodeLab.setText(self.modApp.lastNodeClicked)
            QCoreApplication.processEvents()
            return
        nodeclicked = min(dst, key=(lambda x: x[0]))[1]

        if self.modApp.lastNodeClicked != "":
            pass
            # Change color back
        #self.modApp.lastNodeClicked = nodeclicked

        if self.modApp.lastNodeClicked != "":
            self.higlight(nodeclicked, self.modApp.lastNodeClicked)
            self.modApp.lastNodeClicked = nodeclicked
            self.modApp.clicked_line = -1
            if(self.modApp.globalModelView):
                self.vwApp.networkGUI.network.updateView()
            else:
                self.modApp.computeEdgeBold()
                self.modApp.computeNxGraph()
                self.vwApp.networkGUI.network.axes.clear()
                self.vwApp.networkGUI.network.updateNodes()
                self.vwApp.networkGUI.network.updateLabels()
                self.vwApp.networkGUI.network.drawEdges()
        else:
            self.higlight(nodeclicked,None)
            self.modApp.lastNodeClicked = nodeclicked
            self.modApp.clicked_line = -1
            if (self.modApp.globalModelView):
                self.vwApp.networkGUI.network.updateView()
            else:
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
                        if (self.modApp.globalModelView):
                            self.vwApp.networkGUI.network.updateView()
                        else:
                            self.modApp.computeEdgeBold()
                            self.modApp.computeNxGraph()
                            self.vwApp.networkGUI.network.axes.clear()
                            self.vwApp.networkGUI.network.updateNodes()
                            self.vwApp.networkGUI.network.updateLabels()
                            self.vwApp.networkGUI.network.drawEdges()
                            self.vwApp.updateView()
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
            print('action:', nodeclicked)
            data_tmp = self.modApp.equacolO[np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3])]
            self.modApp.curr_tabl = self.modApp.equacolO[
                np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3, 4])]
            data = []
            for i in range(len(data_tmp)):
                data.append(data_tmp[i])
            self.modApp.data = data
            self.vwApp.eqTableGUI.updateView()

        if (self.modApp.globalModelView):
            class MyWidgetItem:
                self.row2=-1
                def __init__(self,row2):
                    self.row2=row2
                def row(self):
                    return self.row2
            eqCellToClick=self.modApp.selectedEq[self.modApp.lastNodeClicked]
            eqCellToClickWid=MyWidgetItem(eqCellToClick)
            print("clickedEq:"+str(eqCellToClick))
            self.eqTableClicked(eqCellToClickWid)
        else:
            self.vwApp.fitGUI.updateView()
        self.vwApp.networkGUI.fig.canvas.draw()
        self.vwApp.clickedNodeLab.setText(self.modApp.lastNodeClicked)

        QCoreApplication.processEvents()

    # TODO Réintègre le lien sélectionné
    def clickReinstateLink (self):
        if self.vwApp.scrolledListBox.currentText() == "Select link to reinstate":
            return
        else:
            self.modApp.scrolledList.pop(self.vwApp.scrolledListBox.currentIndex())
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
    def eqTableClicked(self, cellClicked):
        self.modApp.clicked_line = cellClicked.row()
        #print("self.modApp.mode_changeEq:" + str(self.modApp.mode_changeEq))
        if (self.modApp.mode_changeEq):
            self.modApp.selectedEq[self.modApp.lastNodeClicked] = cellClicked.row()
            self.modApp.computeGlobalView()
            self.vwApp.updateView()
            self.modApp.mode_changeEq = False
        else:
            self.vwApp.eqTableGUI.updateView()
            self.vwApp.fitGUI.updateView()
        #self.vwApp.networkGUI.updateView()

    def incMatClicked(self,cellClicked):
        print(cellClicked.row())
        self.vwApp.incMatGUI.highlight(cellClicked.row())
        nodeToClick=self.vwApp.incMatGUI.order[cellClicked.row()]
        print(nodeToClick)
        posNode=self.modApp.pos[nodeToClick]
        class MyEvent:
            def __init__(self,xdata,ydata):
                self.xdata=xdata
                self.ydata=ydata
        ev=MyEvent(*posNode)
        self.onClick(ev)
        eqCellToClick = -1
        if(not self.modApp.best_indv):
            for i in range(len(self.modApp.data)):
                if(self.modApp.data[i][2]==self.modApp.datumIncMat.iloc[cellClicked.row()][3]):
                    eqCellToClick=i
                    break
        else:
            eqCellToClick = self.modApp.best_indv[nodeToClick]
        class MyWidgetItem:
            self.row2=-1
            def __init__(self,row2):
                self.row2=row2
            def row(self):
                return self.row2
        eqCellToClickWid=MyWidgetItem(eqCellToClick)

        self.eqTableClicked(eqCellToClickWid)


    # TODO Crée le surlignage des noeuds
    def higlight(self, new_node: str, old_node: str = None):
        #print("higlight:"+new_node)
        self.modApp.G.clear()
        if old_node:
            self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(old_node)] = self.modApp.old_color
        if new_node:
            self.modApp.old_color = self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(new_node)]
            self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(new_node)] = (1.0, 0, 0)

        self.vwApp.networkGUI.network.updateNodes()

    def fileQuit(self):
        self.vwApp.close()


    def closeEvent(self, ce):
        self.fileQuit()

