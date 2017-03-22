#-*- coding: utf-8
from Help import Help
from PyQt4.QtCore import QCoreApplication
from OptimisationCanvas import OptimisationCanvas
from ErrorConstraint import ErrorConstraint
from Network import Network
import numpy as np
from OptimModGlobal import OptimModGlobal
import threading
import re
from itertools import compress
import random
from OnOffCheckBox import *

class RFGraph_Controller:
    def __init__(self,modApp,vwApp):
        self.modApp=modApp
        self.vwApp=vwApp
        self.onMoveMutex = threading.Lock()
        self.moveListMutex= threading.Lock()
        self.protectMutex = threading.Lock()
        self.returnMutex=threading.Lock()
        self.moveEventList=[]
        self.nbOnMoveWaiting=0
        self.lastEvent=None

    def clickHelp(self):
        self.modApp.help_params = Help.get_params()

    # TODO
    def clickFitness(self):
        print("clic fitness")
        self.modApp.ColorMode='Fit'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        #self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        #self.vwApp.buttonFitness.setStyleSheet("background-color: grey")
        #self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        self.vwApp.networkGUI.fig.canvas.draw()
        QCoreApplication.processEvents()
    # TODO
    def clickCompromis(self):
        print("clic Compr")
        self.modApp.ColorMode='Compr'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        #self.vwApp.buttonCompromis.setStyleSheet("background-color: grey")
        #self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        #self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        self.vwApp.networkGUI.fig.canvas.draw()
        QCoreApplication.processEvents()

    # TODO
    def clickCmplx(self):
        print("clic Complx")
        self.modApp.ColorMode='Cmplx'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        #self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        #self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        #self.vwApp.buttonComplexite.setStyleSheet("background-color: grey")
        self.vwApp.networkGUI.fig.canvas.draw()
        QCoreApplication.processEvents()
    # TODO
    def clickOptmuGP(self):
        #self.modApp.opt_params = OptimisationCanvas.get_params()
        optModGlob = OptimModGlobal(self.modApp)
        self.modApp.best_indv=optModGlob.startOptim()
        self.modApp.globalModelView=True
        self.modApp.bestindvToSelectedEq()
        self.modApp.computeGlobalView()
        self.vwApp.incMatGUI.highlight(-1)
        self.vwApp.incMatGUI.mutipleHighlight(-1)
        self.vwApp.updateView()
        self.vwApp.showAction.setChecked(True)

    # TODO
    def clickHideModGlobal(self):
        self.modApp.showGlobalModel = False
        self.vwApp.cmAction.setEnabled(True)
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        self.clickFitness()


    # TODO Affiche le modèle d'équation global
    def clickShowModGlobal(self):
        self.modApp.globalModelView = True
        self.vwApp.cmAction.setDisabled(True)
        self.modApp.computeGlobalView()
        self.vwApp.networkGUI.network.updateView()

    # TODO Enlève le lien entre les noeuds choisis
    def clickRemoveLink(self, event):
        self.modApp.mode_cntrt = True
        self.vwApp.selectContrTxtLab.setText("Select the starting node")

    def clickChangeEq(self):
        print("clickChangeEq")
        self.modApp.mode_changeEq=True

    def onPick(self,event):
        pass

    def onHover(self,dstMin,movingOrClikingNode):

        if(dstMin==''):
            if (self.modApp.lastHover != ''):
                self.vwApp.networkGUI.network.updateView()
                self.modApp.lastHover = ''
            return


        if(not self.modApp.lastHover==dstMin or movingOrClikingNode):

            self.vwApp.networkGUI.network.updateView(dstMin)
            self.modApp.lastHover=dstMin
        #print('hover: '+dstMin[1])

    def onMove3(self,event):
        if(not self.onMoveMutex.acquire(False)):
             #print('already computing,return : ' + str(event))
            self.lastEvent=event
            return
        #print('computing' + str(event))
        self.onMove(event)
        #print('computing finished :' + str(event))
        if(self.lastEvent != None):
            #print('computing last : ' + str(self.lastEvent))
            self.onMove(self.lastEvent)
            self.lastEvent=None
        self.onMoveMutex.release()


    def onMove2(self,event):
        print('new event : ' + str(event))
        self.moveListMutex.acquire(True)
        self.moveEventList.append(event)
        self.moveListMutex.release()
        self.protectMutex.acquire(True)
        if(not self.returnMutex.acquire(False)):
            print('already in computation : ' + str(event))
            self.nbOnMoveWaiting+=1
            self.returnMutex.release()
            self.returnMutex.acquire(True)
            while(self.nbOnMoveWaiting>1):
                print('cleaning : nbOnMoveWaiting = ' + self.nbOnMoveWaiting + '  event : ' + str(event)  )
                self.returnMutex.release()
                self.returnMutex.acquire(True)
            self.protectMutex.release()
            print('waiting : ' + str(event))
            self.returnMutex.acquire(True)
            print('released : ' + event)
            if(self.nbOnMoveWaiting>1):
                print('another is already in the list, return : ' + str(event))
                self.nbOnMoveWaiting-=1
                return
        self.protectMutex.release()
        if(not self.onMoveMutex.acquire(False)):
            print('already computing : ' + str(event))
            return
        self.moveListMutex.acquire(True)
        lastevent=self.moveEventList[-1]
        self.moveEventList=[]
        self.moveListMutex.release()
        print('computing' + str(lastevent))
        self.onMove(lastevent)
        print('computing finished :' + str(lastevent))
        self.onMoveMutex.release()
        self.returnMutex.release()




    def onMove(self,event):
        #print(event)

        (x, y) = (event.xdata, event.ydata)
        if not x or not y:
            if (self.modApp.lastHover != ''):
                self.vwApp.networkGUI.network.updateView()
                self.modApp.lastHover = ''
            return
        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
               self.modApp.pos]
        dst = list(filter(lambda x: x[0] < self.modApp.radius, dst))
        if(len(dst) != 0):
            dstMin = min(dst, key=(lambda x: x[0]))

        else:
            dstMin = ('','')


        if(event.button==None and self.modApp.lastHover == dstMin[1] ):
            #print('return1')
            return

        #if (self.onMoveMutex.locked() or event.inaxes == None ):
        if (event.inaxes == None):
           # print('return2')
            return

        #self.onMoveMutex.acquire()
        if(event.button==1 and self.modApp.lastNodeClicked != None):
            print(event)

            old_pos = self.modApp.pos[self.modApp.lastNodeClicked]
            self.modApp.pos[self.modApp.lastNodeClicked] = (event.xdata, event.ydata)

            self.modApp.lpos[self.modApp.lastNodeClicked] = (
                self.modApp.lpos[self.modApp.lastNodeClicked][0] - old_pos[0] + event.xdata,
                self.modApp.lpos[self.modApp.lastNodeClicked][1] - old_pos[1] + event.ydata)
            #print("old_pos:"+str(old_pos))
            self.modApp.fpos[self.modApp.lastNodeClicked] = (
                self.modApp.fpos[self.modApp.lastNodeClicked][0] - old_pos[0] + event.xdata,
                self.modApp.fpos[self.modApp.lastNodeClicked][1] - old_pos[1] + event.ydata)

            # if (self.modApp.globalModelView):
            #     #self.vwApp.updateView()
            #     self.vwApp.networkGUI.network.updateView()
            # else:
            #     self.vwApp.networkGUI.network.axes.clear()
            #     self.vwApp.networkGUI.network.updateNodes()
            #     self.vwApp.networkGUI.network.updateLabels()
            #     self.vwApp.networkGUI.network.drawEdges()
            #     self.vwApp.networkGUI.fig.canvas.draw()
            self.onHover(self.modApp.lastNodeClicked,True)
            #print('process' + str(random.random()))
            QCoreApplication.processEvents()

        else:
            self.onHover(dstMin[1],False)
            #print('process'+str(random.random()))
            QCoreApplication.processEvents()

        #self.onMoveMutex.release()


    def p(self,s):
        if s==None:
            return ""
        else:
            return s

    def onClick(self, event):
        # TODO  affichage du nom du noeud selectionné + changer couleur
        #print("clicked")
        (x, y) = (event.xdata, event.ydata)
        if  x == None or y == None :
            return

        updateFitGUI=False
        updateEqTable=False

        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in #compute the distance to each node
               self.modApp.pos]

        if(len(list(filter(lambda x: x[0] < self.modApp.radius, dst))) == 0 and event.button==1): #If no node is close enougth, select no node update view and exit
            #self.higlight(None, self.p(self.modApp.lastNodeClicked))
            self.modApp.lastNodeClicked=None
            self.modApp.computeEdgeBold()
            self.modApp.data=[]
            self.modApp.clicked_line = -1
            updateFitGUI=True#Clean the equation table and the measured/predicted plot
            updateEqTable=True
            #self.vwApp.eqTableGUI.updateView()
            #self.vwApp.fitGUI.updateView()
            self.vwApp.clickedNodeLab.setText('Selected node: ' + self.p(self.modApp.lastNodeClicked))

        else:
            nodeclicked = min(dst, key=(lambda x: x[0]))[1] #Closest node
            self.vwApp.incMatGUI.mutipleHighlight(nodeclicked)
            self.vwApp.incMatGUI.highlight(-1)
            print("highlighting "+nodeclicked)
            #self.higlight(nodeclicked, self.p(self.modApp.lastNodeClicked))
            self.modApp.lastNodeClicked = nodeclicked

            if (self.modApp.mode_cntrt == True):                    #Click action when we are deleting a link
                self.deleteLink(nodeclicked)


            if (not self.modApp.mode_cntrt):        #Update the Equation table
                #print('action:', nodeclicked)
                data_tmp = self.modApp.equacolO[np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3, 4])]
                self.modApp.curr_tabl = self.modApp.equacolO[
                    np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3, 4])]
                data = []
                for i in range(len(data_tmp)):
                    data.append(data_tmp[i])
                self.modApp.data = data
                updateEqTable=True
                #self.vwApp.eqTableGUI.updateView()

            if (self.modApp.globalModelView):       #Simulate a click on the equation selected for a node when viewing a global model
                class MyWidgetItem:
                    self.row2=-1
                    def __init__(self,row2):
                        self.row2=row2
                    def row(self):
                        return self.row2
                eqCellToClick=self.modApp.selectedEq[self.modApp.lastNodeClicked]
                eqCellToClickWid=MyWidgetItem(eqCellToClick)
                #print("clickedEq:"+str(eqCellToClick))
                self.eqTableClicked(eqCellToClickWid)
            else:
                self.modApp.clicked_line = -1
                updateFitGUI=True
                #self.vwApp.fitGUI.updateView()
            self.vwApp.clickedNodeLab.setText('Selected node: ' + self.p(self.modApp.lastNodeClicked))
            if(event.button==3):
                print("right click")
                self.vwApp.updateRightClickMenu(self,event,nodeclicked)

        self.modApp.clicked_line = -1

        if (not self.modApp.globalModelView):
            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()

        self.onHover(self.modApp.lastNodeClicked,True)
        #self.vwApp.networkGUI.network.updateView()
        #self.vwApp.networkGUI.fig.canvas.draw()

        QCoreApplication.processEvents()
        if(updateEqTable):
            self.vwApp.eqTableGUI.updateView()
        if(updateFitGUI):
            self.vwApp.fitGUI.updateView()

    def deleteLink(self,nodeclicked,isRmNode=False):
        self.modApp.NodeConstraints.append(nodeclicked)
        self.atLeastOnce = []
        self.notEvenOnce = []
        for i in self.modApp.edgelist_inOrder:
            if i[0] not in self.atLeastOnce:        #List of the beginning element of every arrow
                self.atLeastOnce.append(i[0])
        for i in self.modApp.edgelist_inOrder:
            if i[1] not in self.notEvenOnce:        #List of the end element of every arrow
                self.notEvenOnce.append(i[1])
        if self.modApp.NodeConstraints[0] in self.atLeastOnce: #If the first clicked not correspond to a least a begining element of an arrow
            self.vwApp.selectContrTxtLab.setText("Select the ending node")
            if (len(self.modApp.NodeConstraints) == 2):   # If there are 2 elements in the list of clicked nodes
                if self.modApp.NodeConstraints[1] in self.notEvenOnce \
                        and (self.modApp.NodeConstraints[0],self.modApp.NodeConstraints[1]) in self.modApp.edgelist_inOrder: #verify if the second element clicked corespond to at least the end of an arrow
                    self.constraint = " - ".join(self.modApp.NodeConstraints)
                    #self.modApp.scrolledList.append(self.constraint)
                    #self.vwApp.scrolledListBox.clear()
                    #for item in self.modApp.scrolledList:
                    #    self.vwApp.scrolledListBox.addItem(item)


                    self.modApp.selectContrTxt = ""
                    self.modApp.mode_cntrt = False

                    self.vwApp.selectContrTxtLab.setText("")
                    #linesInEquaPO=np.logical_and(self.modApp.equacolPO[:, 3] == self.modApp.NodeConstraints[0],
                    #               self.modApp.equacolPO[:, 2] == self.modApp.NodeConstraints[1])
                    #a = self.modApp.equacolPO[linesInEquaPO]

                    r = re.compile(r'\b%s\b' % re.escape(self.modApp.NodeConstraints[0]))
                    rsearch = np.vectorize(lambda x: bool(r.search(x)))
                    ix1 = np.ix_(self.modApp.equacolO[:, 2] == self.modApp.NodeConstraints[1])
                    rcontain=rsearch(self.modApp.equacolO[ix1, 3])

                    linesToRemove=list(compress(ix1[0].tolist(), rcontain.tolist()[0]))
                    self.modApp.rmByRmEdge.append(linesToRemove)
                    if(isRmNode):
                        self.modApp.rmByRmNode.append(linesToRemove)
                    self.modApp.equacolO[linesToRemove, 4] = False


                    self.modApp.NodeConstraints = []
                    self.vwApp.addConstrain(self.constraint)

                else:
                    self.modApp.selectContrTxt = ""
                    self.modApp.mode_cntrt = False
                    self.modApp.NodeConstraints = []
                    self.vwApp.selectContrTxtLab.setText('This link does not exist, please retry')
        else:
            self.modApp.selectContrTxt = ""
            self.modApp.mode_cntrt = False
            self.modApp.NodeConstraints = []

    # TODO Réintègre le lien sélectionné
    def clickReinstateLink(self,name,isRestoreByNode=False):
        #if self.vwApp.scrolledListBox.currentText() == "Select link to reinstate":
        #    return
        #else:
        idx=self.modApp.scrolledList.index(name)
        v=name.split(' ')

        self.modApp.forbidden_edge.remove((v[0],v[2]))
        self.modApp.scrolledList.pop(idx)

        linesToReinstate=self.modApp.rmByRmEdge.pop(idx - 1)
        if(isRestoreByNode):
            self.modApp.rmByRmNode.remove(linesToReinstate)
        flist = [item for sublist in self.modApp.rmByRmEdge for item in sublist]
        linesToReinstate=[av for av in linesToReinstate if not av in flist]
        linesToReinstate = [av for av in linesToReinstate if not av in self.modApp.rmByRmEq]
        self.modApp.equacolO[linesToReinstate, 4] = True
        self.modApp.data= self.modApp.equacolO[np.ix_(self.modApp.equacolO[:, 2] == [self.modApp.lastNodeClicked], [0, 1, 3, 4])]

        if(not isRestoreByNode):
            self.vwApp.eqTableGUI.updateView()
            #self.vwApp.scrolledListBox.clear()
            #for item in self.modApp.scrolledList:
            #    self.vwApp.scrolledListBox.addItem(item)
            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()
            self.vwApp.networkGUI.network.updateView()
            self.vwApp.networkGUI.fig.canvas.draw()

            QCoreApplication.processEvents()

    # TODO Change la couleur et la densité des "edges" en fonction du déplacement des sliders
    def SliderMoved(self, value):
        if( self.modApp.adjThresholdVal!=self.vwApp.adjThreshold_slider.value() / 100.0):
            self.modApp.adjThresholdVal=self.vwApp.adjThreshold_slider.value() / 100.0
        #if(self.modApp.comprFitCmplxVal != self.vwApp.comprFitCmplx_slider.value() / 100.0 ):
        #    self.modApp.comprFitCmplxVal=self.vwApp.comprFitCmplx_slider.value() / 100.0
        #    self.modApp.computeComprEdgeColor()
        #    self.modApp.computeEdgeBold()
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
        self.modApp.G.clear()
        if old_node:
            self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(old_node)] = self.modApp.old_color
        if new_node:
            self.modApp.old_color = self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(new_node)]
            self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(new_node)] = (1.0, 0, 0)

        #self.vwApp.networkGUI.network.updateNodes()

    def fileQuit(self):
        self.vwApp.close()


    def closeEvent(self, ce):
        self.fileQuit()

    def onOffClicked(self,objClicked):
        lineToModify=np.ix_(self.modApp.equacolO[:, 2] == [self.modApp.lastNodeClicked])[0][objClicked.id]
        self.modApp.equacolO[lineToModify][4]=objClicked.isChecked()
        self.modApp.data[objClicked.id][3]=objClicked.isChecked()
        if objClicked.isChecked():
            self.modApp.varEquasizeOnlyTrue[self.modApp.lastNodeClicked]+=1
            self.modApp.rmByRmEq.remove(lineToModify)
        else:
            self.modApp.varEquasizeOnlyTrue[self.modApp.lastNodeClicked]-=1
            self.modApp.rmByRmEq.append(lineToModify)

        self.vwApp.eqTableGUI.updateView()

    def removeNode(self,nodeToRemove):
        for i, o in self.modApp.edgelist_inOrder:
            if( (i == nodeToRemove or o == nodeToRemove) and not (i,o) in self.modApp.forbidden_edge ):
                self.deleteLink(i,True)
                self.deleteLink(o,True)
        self.modApp.forbiddenNodes.append(nodeToRemove)
        ix = np.ix_(self.modApp.equacolO[:, 2] == nodeToRemove)
        linesToRemove = [ixe for ixe in ix[0] if not ixe in [le for l in self.modApp.rmByRmEdge for le in l]] #Remove the constant equations
        self.modApp.rmByRmNode.append(linesToRemove)
        self.modApp.equacolO[linesToRemove, 4] = False

        self.vwApp.eqTableGUI.updateView()
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        self.vwApp.networkGUI.fig.canvas.draw()

    def restoreNode(self,nodeToRestore):
        self.modApp.debugCmp=0
        ix = np.ix_(self.modApp.equacolO[:, 2] == nodeToRestore)
        linesToRestore=[ixe for ixe in ix[0] if not ixe in [le for l in self.modApp.rmByRmEdge for le in l]]
        self.modApp.rmByRmNode.remove(linesToRestore)
        self.modApp.equacolO[linesToRestore, 4] = True

        for i, o in self.modApp.edgelist_inOrder:
            if (i == nodeToRestore  and (i,o) in self.modApp.forbidden_edge and not o in self.modApp.forbiddenNodes):
                name = i + ' - ' + o
                self.vwApp.removeConstrain(name,True)
            elif( o == nodeToRestore and (i,o) in self.modApp.forbidden_edge and not i in self.modApp.forbiddenNodes):
                name = i + ' - ' + o
                self.vwApp.removeConstrain(name, True)

        self.modApp.forbiddenNodes.remove(nodeToRestore)
        self.vwApp.eqTableGUI.updateView()
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        self.vwApp.networkGUI.fig.canvas.draw()

        QCoreApplication.processEvents()
    def recomputeNode(self,nodeToCompute):
        print("ToDo : recomputing " + nodeToCompute)