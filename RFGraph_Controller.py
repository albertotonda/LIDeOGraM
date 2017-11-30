# -*- coding: utf-8
from Help import Help
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QAbstractItemView
import numpy as np
from OptimModGlobal import OptimModGlobal
import logging
import threading
import re
from itertools import compress
from time import strftime
import random
import pickle
from math import fabs

class RFGraph_Controller:
    def __init__(self, modApp, vwApp):
        self.modApp = modApp
        self.vwApp = vwApp
        self.onMoveMutex = threading.Lock()
        self.moveListMutex = threading.Lock()
        self.protectMutex = threading.Lock()
        self.returnMutex = threading.Lock()
        self.moveEventList = []
        self.nbOnMoveWaiting = 0
        self.lastEvent = None
        self.on_off_state = False

    def clickHelp(self):
        self.modApp.help_params = Help.get_params()
        logging.info("Clicked on help -- {}".format(strftime("%d %m %y: %H %M %S")))

    def testmultitouch(self, event):
        print('event :' + str(event))
        return True

    def testmultitouch2(self, event):
        print('event2 :' + str(event))
        return True

    def clickFitness(self):
        print("clic fitness")
        self.modApp.ColorMode = 'Fit'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        # self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        # self.vwApp.buttonFitness.setStyleSheet("background-color: grey")
        # self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        self.vwApp.networkGUI.fig.canvas.draw()
        logging.info("Clicked view fitness -- {}".format(strftime("%d %m %y: %H %M %S")))
        QCoreApplication.processEvents()

    def clickSA(self):
        print("clic SA")
        self.modApp.ColorMode = 'SA'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        # self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        # self.vwApp.buttonFitness.setStyleSheet("background-color: grey")
        # self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        self.vwApp.networkGUI.fig.canvas.draw()
        QCoreApplication.processEvents()

    def clickPearson(self):
        print("clic Pearson")
        self.modApp.ColorMode = 'Pearson'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        # self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        # self.vwApp.buttonFitness.setStyleSheet("background-color: grey")
        # self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        logging.info("Cliked view Pearson -- {}".format(strftime("%d %m %y: %H %M %S")))
        self.vwApp.networkGUI.fig.canvas.draw()
        QCoreApplication.processEvents()

    def clickCompromis(self):
        print("clic Compr")
        self.modApp.ColorMode = 'Compr'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        # self.vwApp.buttonCompromis.setStyleSheet("background-color: grey")
        # self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        # self.vwApp.buttonComplexite.setStyleSheet("background-color: None")
        self.vwApp.networkGUI.fig.canvas.draw()
        QCoreApplication.processEvents()

    def clickCmplx(self):
        print("clic Complx")
        self.modApp.ColorMode = 'Cmplx'
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        # self.vwApp.buttonCompromis.setStyleSheet("background-color: None")
        # self.vwApp.buttonFitness.setStyleSheet("background-color: None")
        # self.vwApp.buttonComplexite.setStyleSheet("background-color: grey")
        self.vwApp.networkGUI.fig.canvas.draw()
        logging.info("Clicked view complexity -- {}".format(strftime("%d %m %y: %H %M %S")))
        QCoreApplication.processEvents()

    def clickOptmuGP(self):
        logging.info("Global optimisation started -- {}".format(strftime("%d %m %y: %H %M %S")))
        # self.modApp.opt_params = OptimisationCanvas.get_params()
        if (len(self.modApp.nodesWithNoEquations) > 0):
            self.vwApp.noEquationError()
        else:
            self.vwApp.global_compute_progress.reset()
            optModGlob = OptimModGlobal(self.modApp)
            optModGlob.update_bar_signal.connect(self.vwApp.global_compute_progress.setValue)
            self.modApp.best_indv = optModGlob.startOptim()
            self.modApp.globalModelView = True
            self.modApp.bestindvToSelectedEq()
            self.modApp.computeGlobalView()
            self.vwApp.incMatGUI.highlight(-1)
            self.vwApp.incMatGUI.mutipleHighlight(-1)
            self.vwApp.updateView()
            self.vwApp.showAction.setChecked(True)
            optModGlob.update_bar_signal.disconnect(self.vwApp.global_compute_progress.setValue)

    # TODO
    def clickHideModGlobal(self):
        logging.info("Clicked Hide global model -- {}".format(strftime("%d %m %y: %H %M %S")))
        self.modApp.showGlobalModel = False
        self.vwApp.cmAction.setEnabled(True)
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        self.clickFitness()

    def clickUncertaintyButton(self):
        logging.info("Clicked uncertainty button -- {}".format(strftime("%d %m %y: %H %M %S")))
        self.modApp.dataset.variablesUncertainty[self.modApp.lastNodeClicked] = float(
            self.vwApp.uncertaintyModifTxt.text())
        self.vwApp.fitGUI.updateView()

    # TODO Affiche le modèle d'équation global
    def clickShowModGlobal(self):
        logging.info("Clicked show model global -- {}".format(strftime("%d %m %y: %H %M %S")))
        self.modApp.globalModelView = True
        self.vwApp.cmAction.setDisabled(True)
        self.modApp.computeGlobalView()
        self.vwApp.networkGUI.network.updateView()

    # TODO Enlève le lien entre les noeuds choisis
    def clickRemoveLink(self, event):
        logging.info("Cliked remove link -- {}".format(strftime("%d %m %y: %H %M %S")))
        self.modApp.mode_cntrt = True
        self.vwApp.selectContrTxtLab.setText("Select the starting node")

    def clickChangeEq(self):
        logging.info("clicked change equation -- {}".format(strftime("%d %m %y: %H %M %S")))
        self.modApp.mode_changeEq = True

    def clickSaveEq(self):
        print("clickSaveEq")
        filehandler = open('equations' + str(random.random()) + '.txt', 'wb')
        pickle.dump(self.modApp.equacolO, filehandler)
        print("Saved")

    def onPick(self, event):
        pass

    def onHover(self, dstMin, movingOrClikingNode):
        if dstMin == '':
            if self.modApp.lastHover != '':
                self.vwApp.networkGUI.network.updateView()
                self.modApp.lastHover = ''
            return

        if (not self.modApp.lastHover == dstMin or movingOrClikingNode):
            logging.info("Hovered {} -- {}".format(str(dstMin), strftime("%d %m %y: %H %M %S")))
            self.vwApp.networkGUI.network.updateView(dstMin)
            self.modApp.lastHover = dstMin
            # print('hover: '+dstMin[1])

    def onMove3(self, event):
        if (not self.onMoveMutex.acquire(False)):
            # print('already computing,return : ' + str(event))
            self.lastEvent = event
            return
        # print('computing' + str(event))
        self.onMove(event)
        # print('computing finished :' + str(event))
        if (self.lastEvent != None):
            # print('computing last : ' + str(self.lastEvent))
            self.onMove(self.lastEvent)
            self.lastEvent = None
        self.onMoveMutex.release()

    def onMove2(self, event):
        print('new event : ' + str(event))
        self.moveListMutex.acquire(True)
        self.moveEventList.append(event)
        self.moveListMutex.release()
        self.protectMutex.acquire(True)
        if (not self.returnMutex.acquire(False)):
            print('already in computation : ' + str(event))
            self.nbOnMoveWaiting += 1
            self.returnMutex.release()
            self.returnMutex.acquire(True)
            while (self.nbOnMoveWaiting > 1):
                print('cleaning : nbOnMoveWaiting = ' + str(self.nbOnMoveWaiting) + '  event : ' + str(event))
                self.returnMutex.release()
                self.returnMutex.acquire(True)
            self.protectMutex.release()
            print('waiting : ' + str(event))
            self.returnMutex.acquire(True)
            print('released : ' + event)
            if (self.nbOnMoveWaiting > 1):
                print('another is already in the list, return : ' + str(event))
                self.nbOnMoveWaiting -= 1
                return
        self.protectMutex.release()
        if (not self.onMoveMutex.acquire(False)):
            print('already computing : ' + str(event))
            return
        self.moveListMutex.acquire(True)
        lastevent = self.moveEventList[-1]
        self.moveEventList = []
        self.moveListMutex.release()
        print('computing' + str(lastevent))
        self.onMove(lastevent)
        print('computing finished :' + str(lastevent))
        self.onMoveMutex.release()
        self.returnMutex.release()

    def onMove(self, event):
        # print(event)

        (x, y) = (event.xdata, event.ydata)
        if not x or not y:
            if (self.modApp.lastHover != ''):
                self.vwApp.networkGUI.network.updateView()
                self.modApp.lastHover = ''
            return
        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
               self.modApp.pos]
        dst = list(filter(lambda x: x[0] < self.modApp.radius, dst))
        if (len(dst) != 0):
            dstMin = min(dst, key=(lambda x: x[0]))
        else:
            dstMin = ('', '')

        if (event.button == None and self.modApp.lastHover == dstMin[1]):
            # print('return1')
            return

        # if (self.onMoveMutex.locked() or event.inaxes == None ):
        if (event.inaxes == None):
            # print('return2')
            return

        # self.onMoveMutex.acquire()
        if (event.button == 1 and self.modApp.lastNodeClicked != None):
            logging.info("Moving {} -- {}".format(self.modApp.lastNodeClicked, strftime("%d %m %y: %H %M %S")))
            old_pos = self.modApp.pos[self.modApp.lastNodeClicked]
            self.modApp.pos[self.modApp.lastNodeClicked] = (event.xdata, event.ydata)

            self.modApp.lpos[self.modApp.lastNodeClicked] = (
                self.modApp.lpos[self.modApp.lastNodeClicked][0] - old_pos[0] + event.xdata,
                self.modApp.lpos[self.modApp.lastNodeClicked][1] - old_pos[1] + event.ydata)
            # print("old_pos:"+str(old_pos))
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
            self.onHover(self.modApp.lastNodeClicked, True)
            # print('process' + str(random.random()))
            QCoreApplication.processEvents()

        else:
            self.onHover(dstMin[1], False)
            # print('process'+str(random.random()))
            QCoreApplication.processEvents()

            # self.onMoveMutex.release()

    def p(self, s):
        if s == None:
            return ""
        else:
            return s

    def onClick(self, event):
        # TODO  affichage du nom du noeud selectionné + changer couleur
        (x, y) = (event.xdata, event.ydata)
        if x == None or y == None:
            return

        updateFitGUI = False
        updateEqTable = False

        dst = [(pow(x - self.modApp.pos[node][0], 2) + pow(y - self.modApp.pos[node][1], 2), node) for node in
               # compute the distance to each node
               self.modApp.pos]

        if (len(list(filter(lambda x: x[0] < self.modApp.radius,
                            dst))) == 0 and event.button == 1):  # If no node is close enougth, select no node update view and exit
            self.modApp.lastNodeClicked = None
            self.modApp.computeEdgeBold()
            self.modApp.data = []
            updateFitGUI = True  # Clean the equation table and the measured/predicted plot
            updateEqTable = True
            # self.vwApp.eqTableGUI.updateView()
            # self.vwApp.fitGUI.updateView()
            self.vwApp.clickedNodeLab.setText('Selected node: ' + self.p(self.modApp.lastNodeClicked))
            logging.info("Clicked {} -- {}".format(self.modApp.lastNodeClicked, strftime("%d %m %y: %H %M %S")))


        else:
            logging.info("Clicked graph deselect all -- {}".format(strftime("%d %m %y: %H %M %S")))
            nodeclicked = min(dst, key=(lambda x: x[0]))[1]  # Closest node
            self.vwApp.incMatGUI.mutipleHighlight(nodeclicked)
            self.vwApp.incMatGUI.highlight(-1)
            print("highlighting " + nodeclicked)
            # self.higlight(nodeclicked, self.p(self.modApp.lastNodeClicked))
            self.modApp.lastNodeClicked = nodeclicked

            if (self.modApp.mode_cntrt == True):  # Click action when we are deleting a link
                self.deleteLink(nodeclicked)

            if (not self.modApp.mode_cntrt):  # Update the Equation table
                # print('action:', nodeclicked)
                data_tmp = self.modApp.equacolO[np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3, 4])]
                self.modApp.curr_tabl = self.modApp.equacolO[
                    np.ix_(self.modApp.equacolO[:, 2] == [nodeclicked], [0, 1, 3, 4])]
                data = []
                for i in range(len(data_tmp)):
                    data.append(data_tmp[i])
                self.modApp.data = data
                updateEqTable = True
                # self.vwApp.eqTableGUI.updateView()

            if (
            self.modApp.globalModelView):  # Simulate a click on the equation selected for a node when viewing a global model
                class MyWidgetItem:
                    self.row2 = -1

                    def __init__(self, row2):
                        self.row2 = row2

                    def row(self):
                        return self.row2

                eqCellToClick = self.modApp.selectedEq[self.modApp.lastNodeClicked]
                eqCellToClickWid = MyWidgetItem(eqCellToClick)
                # print("clickedEq:"+str(eqCellToClick))
                self.eqTableClicked(eqCellToClickWid)
            else:
                self.modApp.clicked_line = -1
                updateFitGUI = True
                # self.vwApp.fitGUI.updateView()
            self.vwApp.clickedNodeLab.setText('Selected node: ' + self.p(self.modApp.lastNodeClicked))
            if (event.button == 3):
                print("right click")
                self.vwApp.updateRightClickMenu(self, event, nodeclicked)

        self.modApp.clicked_line = -1

        if (not self.modApp.globalModelView):
            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()

        self.onHover(self.modApp.lastNodeClicked, True)
        # self.vwApp.networkGUI.network.updateView()
        # self.vwApp.networkGUI.fig.canvas.draw()

        QCoreApplication.processEvents()
        if (updateEqTable):
            self.vwApp.eqTableGUI.updateView()
        if (updateFitGUI):
            if (not self.modApp.lastNodeClicked == None):
                self.vwApp.uncertaintyModifTxt.setText(
                    str(self.modApp.dataset.variablesUncertainty[self.modApp.lastNodeClicked]))
            else:
                self.vwApp.uncertaintyModifTxt.setText('')
            self.vwApp.fitGUI.updateView()

    def deleteLink(self, nodeclicked, isRmNode=False):
        self.modApp.NodeConstraints.append(nodeclicked)
        self.atLeastOnce = []
        self.notEvenOnce = []
        for i in self.modApp.edgelist_inOrder:
            if i[0] not in self.atLeastOnce:  # List of the beginning element of every arrow
                self.atLeastOnce.append(i[0])
        for i in self.modApp.edgelist_inOrder:
            if i[1] not in self.notEvenOnce:  # List of the end element of every arrow
                self.notEvenOnce.append(i[1])
        if self.modApp.NodeConstraints[
            0] in self.atLeastOnce:  # If the first clicked not correspond to a least a begining element of an arrow
            self.vwApp.selectContrTxtLab.setText("Select the ending node")
            if (len(self.modApp.NodeConstraints) == 2):  # If there are 2 elements in the list of clicked nodes
                if self.modApp.NodeConstraints[1] in self.notEvenOnce \
                        and (self.modApp.NodeConstraints[0], self.modApp.NodeConstraints[
                            1]) in self.modApp.edgelist_inOrder:  # verify if the second element clicked corespond to at least the end of an arrow
                    self.constraint = " - ".join(self.modApp.NodeConstraints)
                    logging.info("Adding a constrain {} -- {}".format(" - ".join(self.modApp.NodeConstraints),
                                                                      strftime("%d %m %y: %H %M %S")))
                    # self.modApp.scrolledList.append(self.constraint)
                    # self.vwApp.scrolledListBox.clear()
                    # for item in self.modApp.scrolledList:
                    #    self.vwApp.scrolledListBox.addItem(item)


                    self.modApp.selectContrTxt = ""
                    self.modApp.mode_cntrt = False

                    self.vwApp.selectContrTxtLab.setText("")
                    # linesInEquaPO=np.logical_and(self.modApp.equacolPO[:, 3] == self.modApp.NodeConstraints[0],
                    #               self.modApp.equacolPO[:, 2] == self.modApp.NodeConstraints[1])
                    # a = self.modApp.equacolPO[linesInEquaPO]

                    r = re.compile(r'\b%s\b' % re.escape(self.modApp.NodeConstraints[0]))
                    rsearch = np.vectorize(lambda x: bool(r.search(x)))
                    ix1 = np.ix_(self.modApp.equacolO[:, 2] == self.modApp.NodeConstraints[1])
                    rcontain = rsearch(self.modApp.equacolO[ix1, 3])

                    linesToRemove = list(compress(ix1[0].tolist(), rcontain.tolist()[0]))
                    self.modApp.rmByRmEdge.append(linesToRemove)
                    if (isRmNode):
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

    def clickReinstateLink(self, name, isRestoreByNode=False):
        idx = self.modApp.scrolledList.index(name)
        v = name.split(' ')

        self.modApp.forbidden_edge.remove((v[0], v[2]))
        self.modApp.scrolledList.pop(idx)

        linesToReinstate = self.modApp.rmByRmEdge.pop(idx - 1)
        if (isRestoreByNode):
            self.modApp.rmByRmNode.remove(linesToReinstate)
        flist = [item for sublist in self.modApp.rmByRmEdge for item in sublist]
        logging.info("Clicked reinstate line {} -- {}".format(str(flist), strftime("%d %m %y: %H %M %S")))
        linesToReinstate = [av for av in linesToReinstate if not av in flist]
        linesToReinstate = [av for av in linesToReinstate if not av in self.modApp.rmByRmEq]
        self.modApp.equacolO[linesToReinstate, 4] = True
        self.modApp.data = self.modApp.equacolO[
            np.ix_(self.modApp.equacolO[:, 2] == [self.modApp.lastNodeClicked], [0, 1, 3, 4])]

        if (not isRestoreByNode):
            self.vwApp.eqTableGUI.updateView()
            self.modApp.computeEdgeBold()
            self.modApp.computeNxGraph()
            self.vwApp.networkGUI.network.updateView()
            self.vwApp.networkGUI.fig.canvas.draw()

            QCoreApplication.processEvents()

    def SliderMoved(self, value):
        if (self.modApp.adjThresholdVal != self.vwApp.adjThreshold_slider.value() / 100.0):
            self.modApp.adjThresholdVal = self.vwApp.adjThreshold_slider.value() / 100.0
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()

    # TODO Affiche la courbe de l'équation sélectionnée
    def eqTableClicked(self, cellClicked):
        self.modApp.clicked_line = cellClicked.row()
        # print("self.modApp.mode_changeEq:" + str(self.modApp.mode_changeEq))
        if (self.modApp.mode_changeEq):
            self.modApp.selectedEq[self.modApp.lastNodeClicked] = cellClicked.row() - int(
                self.modApp.varEquasize[self.modApp.lastNodeClicked] - self.modApp.varEquasizeOnlyTrue[
                    self.modApp.lastNodeClicked])

            self.modApp.computeGlobalView()
            self.vwApp.updateView()
            self.modApp.mode_changeEq = False
        else:
            logging.info(
                "Clicked equation table {}:{} -- {}".format(self.modApp.lastNodeClicked, self.modApp.clicked_line,
                                                            strftime("%d %m %y: %H %M %S")))
            self.vwApp.eqTableGUI.updateView()
            if not self.modApp.lastNodeClicked is None:
                #invOrder = self.vwApp.incMatGUI.newOrder[:]
                #for c, _ in enumerate(self.vwApp.incMatGUI.newOrder):
                #    invOrder[_] = c
                counter = 0
                matrix_position =0
                uncertainty = str(self.modApp.dataset.variablesUncertainty[self.modApp.lastNodeClicked])
                self.vwApp.uncertaintyModifTxt.setText(uncertainty)
                for n,i in enumerate(self.vwApp.incMatGUI.order):
                    if i == self.modApp.lastNodeClicked:
                        if counter == self.modApp.clicked_line:
                            #matrix_position = invOrder[n]
                            matrix_position =self.vwApp.incMatGUI.newOrder.index(n)
                            break
                        counter += 1

                self.vwApp.incMatGUI.highlight(matrix_position)


            else:

                self.vwApp.uncertaintyModifTxt.setText('')

            self.vwApp.fitGUI.updateView()
            item_to_select = self.vwApp.eqTableGUI.item(self.modApp.clicked_line, 0)
            self.vwApp.eqTableGUI.scrollToItem(item_to_select, QAbstractItemView.PositionAtCenter)
        pass
        # self.vwApp.networkGUI.updateView()

    def eqTableHeaderClicked(self, clicked):
        print("Header {}".format(clicked))
        if clicked == 3:
            for _ in range(len(np.ix_(self.modApp.equacolO[:, 2] == [self.modApp.lastNodeClicked])[0])):
                lineToModify = np.ix_(self.modApp.equacolO[:, 2] == [self.modApp.lastNodeClicked])[0][_]
                self.modApp.equacolO[lineToModify][4] = self.on_off_state
                self.modApp.data[_][3] = self.on_off_state
            self.vwApp.eqTableGUI.updateView()
            self.on_off_state = not self.on_off_state

    def incMatClicked(self, cellClicked):
        print(cellClicked.row())
        self.vwApp.incMatGUI.highlight(cellClicked.row())
        nodeToClick = self.vwApp.incMatGUI.order[cellClicked.row()]
        print(nodeToClick)
        logging.info("Clicked Matrix {} -- {}".format(nodeToClick, strftime("%d %m %y: %H %M %S")))
        posNode = self.modApp.pos[nodeToClick]

        class MyEvent:
            def __init__(self, xdata, ydata):
                self.xdata = xdata
                self.ydata = ydata
                self.button = None

        ev = MyEvent(*posNode)
        self.onClick(ev)
        eqCellToClick = -1
        for i in range(len(self.modApp.data)):
            if (self.modApp.data[i][2] == self.modApp.datumIncMat.iloc[cellClicked.row()][3]):
                eqCellToClick = i
                break
        if self.modApp.best_indv:
            eqCellToClick = self.vwApp.incMatGUI.newOrder[eqCellToClick]

        class MyWidgetItem:
            self.row2 = -1

            def __init__(self, row2):
                self.row2 = row2

            def row(self):
                return self.row2

        eqCellToClickWid = MyWidgetItem(eqCellToClick)

        self.eqTableClicked(eqCellToClickWid)

    # TODO Crée le surlignage des noeuds
    def higlight(self, new_node: str, old_node: str = None):
        self.modApp.G.clear()
        if old_node:
            self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(old_node)] = self.modApp.old_color
        if new_node:
            self.modApp.old_color = self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(new_node)]
            self.modApp.nodeColor[(self.modApp.dataset.varnames.tolist()).index(new_node)] = (1.0, 0, 0)

            # self.vwApp.networkGUI.network.updateNodes()

    def fileQuit(self):
        self.vwApp.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def onOffClicked(self, objClicked, id=0):
        scroll_handle = self.vwApp.eqTableGUI.verticalScrollBar()
        scroll_position = scroll_handle.value()
        first_row = self.vwApp.eqTableGUI.rowAt(0)
        lineToModify = np.ix_(self.modApp.equacolO[:, 2] == [self.modApp.lastNodeClicked])[0][objClicked.id]
        logging.info("OnOffClicked {} -- {}".format(lineToModify, strftime("%d %m %y: %H %M %S")))
        self.modApp.equacolO[lineToModify][4] = objClicked.isChecked()
        self.modApp.data[objClicked.id][3] = objClicked.isChecked()
        if objClicked.isChecked():
            self.modApp.varEquasizeOnlyTrue[self.modApp.lastNodeClicked] += 1
            self.modApp.rmByRmEq.remove(lineToModify)
        else:
            self.modApp.varEquasizeOnlyTrue[self.modApp.lastNodeClicked] -= 1
            self.modApp.rmByRmEq.append(lineToModify)

        self.vwApp.eqTableGUI.updateView()
        self.vwApp.eqTableGUI.scrollToItem(self.vwApp.eqTableGUI.item(first_row, 0), QAbstractItemView.PositionAtTop)
        self.vwApp.eqTableGUI.show()

    def removeNode(self, nodeToRemove):
        logging.info("Removing node {} -- {}".format(str(nodeToRemove), strftime("%d %m %y: %H %M %S")))

        for i, o in self.modApp.edgelist_inOrder:
            if ((i == nodeToRemove or o == nodeToRemove) and not (i, o) in self.modApp.forbidden_edge):
                self.deleteLink(i, True)
                self.deleteLink(o, True)
        self.modApp.forbiddenNodes.append(nodeToRemove)
        ix = np.ix_(self.modApp.equacolO[:, 2] == nodeToRemove)
        linesToRemove = [ixe for ixe in ix[0] if
                         not ixe in [le for l in self.modApp.rmByRmEdge for le in l]]  # Remove the constant equations
        self.modApp.rmByRmNode.append(linesToRemove)
        self.modApp.equacolO[linesToRemove, 4] = False

        self.vwApp.eqTableGUI.updateView()
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        self.vwApp.networkGUI.fig.canvas.draw()

    def restoreNode(self, nodeToRestore):
        logging.info("Restoring node {} -- {}".format(str(nodeToRestore), strftime("%d %m %y: %H %M %S")))

        self.modApp.debugCmp = 0
        ix = np.ix_(self.modApp.equacolO[:, 2] == nodeToRestore)
        linesToRestore = [ixe for ixe in ix[0] if not ixe in [le for l in self.modApp.rmByRmEdge for le in l]]
        self.modApp.rmByRmNode.remove(linesToRestore)
        self.modApp.equacolO[linesToRestore, 4] = True

        for i, o in self.modApp.edgelist_inOrder:
            if (i == nodeToRestore and (i, o) in self.modApp.forbidden_edge and not o in self.modApp.forbiddenNodes):
                name = i + ' - ' + o
                self.vwApp.removeConstrain(name, True)
            elif (o == nodeToRestore and (i, o) in self.modApp.forbidden_edge and not i in self.modApp.forbiddenNodes):
                name = i + ' - ' + o
                self.vwApp.removeConstrain(name, True)

        self.modApp.forbiddenNodes.remove(nodeToRestore)
        self.vwApp.eqTableGUI.updateView()
        self.modApp.computeNxGraph()
        self.vwApp.networkGUI.network.updateView()
        self.vwApp.networkGUI.fig.canvas.draw()

        QCoreApplication.processEvents()

    def recomputeNode(self, nodeToCompute):
        logging.info("Recompute node {} -- {}".format(nodeToCompute, strftime("%d %m %y: %H %M %S")))

        print("Recomputing " + nodeToCompute)
        tmp_equacolO = self.modApp.readEureqaResults('data/eureqa_sans_calcmol_soussurexpr_expertcorrected.txt')
        tmp_equacolO = tmp_equacolO[tmp_equacolO[:, 2] == nodeToCompute, :]
        self.modApp.recomputeNode(nodeToCompute, tmp_equacolO)
