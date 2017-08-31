#-*- coding: utf-8
from PyQt4 import QtGui, QtCore

from NetworkCanvas import NetworkCanvas
from EqTableCanvas import EqTableCanvas
from IncMatrixCanvas import IncMatrixCanvas
from FitCanvas import FitCanvas
from OnOffCheckBox import *
from PyQt4.Qt import QPoint

import sys
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from types import *


# TODO Crée tout les boutons (or graphes + équations)
class RFGraph_View(QtGui.QMainWindow,QtGui.QGraphicsItem):

    def sceneEventFilter(self, event):
        #print(event)
        pass

    def __init__(self,modApp):

        self.modApp = modApp

        QtGui.QMainWindow.__init__(self)
        QtGui.QGraphicsItem.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # self.setWindowTitle(QtGui.QLabel("Test"))
        self.setWindowTitle("LIDeoGraM")
        self.icon = QtGui.QIcon("Icone.png")
        self.setWindowIcon(self.icon)

        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.main_widget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)
        self.networkGUI = NetworkCanvas(self.modApp, self)
        # self.gridLayout.addWidget(self.networkGUI, 1, 0, 7, 60)
        self.gridLayout.addWidget(self.networkGUI, 1, 0, 2, 2)
        self.incMatGUI = IncMatrixCanvas(self.modApp, self)
        # self.gridLayout.addWidget(self.incMatGUI,1,61,12,60)
        #self.gridLayout.addWidget(self.incMatGUI, 1, 2, 3, 1)
        self.adjThreshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.adjThreshold_slider.setValue(self.modApp.adjThresholdVal * 100)

        self.adjThreshold_lab = QtGui.QLabel('Edges importance : ')
        # self.gridLayout.addWidget(self.adjThreshold_lab, 8, 0, 1, 2)
        self.gridLayout.addWidget(self.adjThreshold_lab, 3, 0, 1, 1)
        # self.gridLayout.addWidget(self.adjThreshold_slider, 8, 2, 1, 57)
        self.gridLayout.addWidget(self.adjThreshold_slider , 3, 1, 1, 1)

        # self.comprFitCmplx_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        # self.comprFitCmplx_slider.setValue(self.modApp.comprFitCmplxVal * 100)
        # self.comprFitCmplx_lab = QtGui.QLabel('Compromise : ')
        # self.gridLayout.addWidget(self.comprFitCmplx_lab, 9, 0)
        # self.comprFitCmplx_lab_cmplx = QtGui.QLabel('Complexity')
        # self.gridLayout.addWidget(self.comprFitCmplx_lab_cmplx, 9, 1)
        # self.gridLayout.addWidget(self.comprFitCmplx_slider, 9, 2, 1, 57)
        self.comprFitCmplx_lab_fit = QtGui.QLabel('Fitness')
        # self.gridLayout.addWidget(self.comprFitCmplx_lab_fit, 9, 59, 1, 1)
        self.selectContrTxtLab = QtGui.QLabel('')
        self.gridLayout.addWidget(self.selectContrTxtLab, 0, 1, 1, 1)
        selectContrFont = QtGui.QFont("AnyStyle", 14, QtGui.QFont.DemiBold)
        self.selectContrTxtLab.setFont(selectContrFont)

        self.clickedNodeLab = QtGui.QLabel('Selected node:')
        selNodeFont = QtGui.QFont("AnyStyle", 14, QtGui.QFont.DemiBold)
        self.clickedNodeLab.setFont(selNodeFont)
        self.eqTableGUI = EqTableCanvas(self.modApp)
        # self.gridLayout.addWidget(self.eqTableGUI, 1, 130, 6, 60)
        self.gridLayout.addWidget(self.eqTableGUI, 1, 3, 1, 1)
        # selNodeLab=QtGui.QLabel('Selected node:')
        # selNodeLab.setFont(selNodeFont)
        # self.gridLayout.addWidget(selNodeLab,0,140,1,30)
        # self.gridLayout.addWidget(self.clickedNodeLab, 0, 153, 1, 30)
        # self.gridLayout.addWidget(selNodeLab,0,3,1,1)
        self.gridLayout.addWidget(self.clickedNodeLab, 0, 3, 1, 1)

        self.uncertaintyModifTxt = QtGui.QLineEdit()
        self.uncertaintyModifButton=QtGui.QPushButton("Change Uncertainty")
        self.fitGUI = FitCanvas(self.modApp)
        # self.gridLayout.addWidget(self.fitGUI, 7, 130, 6, 60)

        self.fit_widget = QtGui.QWidget(self)
        self.fitLayout = QtGui.QGridLayout(self.fit_widget)
        self.fitLayout.addWidget(self.uncertaintyModifTxt,0,0,1,1)
        self.fitLayout.addWidget(self.uncertaintyModifButton,0,1,1,1)
        self.fitLayout.addWidget(self.fitGUI, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.fit_widget, 2, 3, 2, 1)
        # self.buttonCompromis = QtGui.QPushButton('Compromise', self)
        # self.buttonFitness = QtGui.QPushButton('Fitness', self)
        # self.buttonComplexite = QtGui.QPushButton('Complexity', self)
        # self.buttonOptUgp3 = QtGui.QPushButton('Global Optimisation', self)
        # self.buttonShowModGlobal = QtGui.QPushButton('Show Global Model', self)
        # self.buttonHideModGlobal = QtGui.QPushButton('Hide Global Model', self)
        self.buttonChangerEq = QtGui.QPushButton('Change equation', self)
        # self.buttonRemoveLink = QtGui.QPushButton('Remove Link', self)
        # self.buttonReinstateLink = QtGui.QPushButton('Reinstate', self)
        # self.buttonHelp = QtGui.QPushButton('Help', self)
        # self.buttonCompromis.setStyleSheet("background-color: grey")

        # self.gridLayout.addWidget(self.buttonCompromis, 10, 0, 1, 15)
        # self.gridLayout.addWidget(self.buttonFitness, 10, 15, 1, 15)
        # self.gridLayout.addWidget(self.buttonComplexite, 10, 30, 1, 15)
        # self.gridLayout.addWidget(self.buttonOptUgp3, 10, 45, 1, 15)
        # self.gridLayout.addWidget(self.buttonShowModGlobal, 11, 0, 1, 30)
        # self.gridLayout.addWidget(self.buttonHideModGlobal, 11, 30, 1, 30)
        self.gridLayout.addWidget(self.buttonChangerEq, 4, 0, 1, 1)
        # self.gridLayout.addWidget(self.buttonRemoveLink, 12, 0, 1, 30)
        # self.gridLayout.addWidget(self.buttonReinstateLink, 0, 12, 1, 8)
        #        self.gridLayout.addWidget(self.buttonHelp, 0, 120, 1, 12)

        # self.scrolledListBox = QtGui.QComboBox(self)
        # self.gridLayout.addWidget(self.scrolledListBox, 0, 1, 1, 1)


        # self.font = QtGui.QFont('Liberation Sans Narrow')
        # self.font.setPointSize(12)
        # self.setFont(self.font)

        self.eqTableGUI.setAttribute(Qt.WA_AcceptTouchEvents)

        #self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        # self.show()
        self.updateView()




        ##self.main_widget.setFocus()
        #self.setCentralWidget(self.main_widget)

        def old__init(self, modApp):
            self.modApp = modApp

            QtGui.QMainWindow.__init__(self)
            QtGui.QGraphicsItem.__init__(self)
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            # self.setWindowTitle(QtGui.QLabel("Test"))
            self.setWindowTitle("LIDeoGraM")
            self.icon = QtGui.QIcon("Icone.png")
            self.setWindowIcon(self.icon)

            self.setWindowState(QtCore.Qt.WindowMaximized)

            self.main_widget = QtGui.QWidget(self)

            self.gridLayout = QtGui.QGridLayout(self.main_widget)
            self.gridLayout.setSpacing(5)
            self.networkGUI = NetworkCanvas(self.modApp, self)
            # self.gridLayout.addWidget(self.networkGUI, 1, 0, 7, 60)
            self.gridLayout.addWidget(self.networkGUI, 1, 0, 2, 2)
            self.incMatGUI = IncMatrixCanvas(self.modApp, self)
            # self.gridLayout.addWidget(self.incMatGUI,1,61,12,60)
            self.gridLayout.addWidget(self.incMatGUI, 1, 2, 3, 1)
            self.adjThreshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
            self.adjThreshold_slider.setValue(self.modApp.adjThresholdVal * 100)

            self.adjThreshold_lab = QtGui.QLabel('Edges importance : ')
            # self.gridLayout.addWidget(self.adjThreshold_lab, 8, 0, 1, 2)
            self.gridLayout.addWidget(self.adjThreshold_lab, 3, 0, 1, 1)
            # self.gridLayout.addWidget(self.adjThreshold_slider, 8, 2, 1, 57)
            self.gridLayout.addWidget(self.adjThreshold_slider, 3, 1, 1, 1)

            # self.comprFitCmplx_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
            # self.comprFitCmplx_slider.setValue(self.modApp.comprFitCmplxVal * 100)
            # self.comprFitCmplx_lab = QtGui.QLabel('Compromise : ')
            # self.gridLayout.addWidget(self.comprFitCmplx_lab, 9, 0)
            # self.comprFitCmplx_lab_cmplx = QtGui.QLabel('Complexity')
            # self.gridLayout.addWidget(self.comprFitCmplx_lab_cmplx, 9, 1)
            # self.gridLayout.addWidget(self.comprFitCmplx_slider, 9, 2, 1, 57)
            self.comprFitCmplx_lab_fit = QtGui.QLabel('Fitness')
            # self.gridLayout.addWidget(self.comprFitCmplx_lab_fit, 9, 59, 1, 1)
            self.selectContrTxtLab = QtGui.QLabel('')
            self.gridLayout.addWidget(self.selectContrTxtLab, 0, 1, 1, 1)
            selectContrFont = QtGui.QFont("AnyStyle", 14, QtGui.QFont.DemiBold)
            self.selectContrTxtLab.setFont(selectContrFont)

            self.clickedNodeLab = QtGui.QLabel('Selected node:')
            selNodeFont = QtGui.QFont("AnyStyle", 14, QtGui.QFont.DemiBold)
            self.clickedNodeLab.setFont(selNodeFont)
            self.eqTableGUI = EqTableCanvas(self.modApp)
            # self.gridLayout.addWidget(self.eqTableGUI, 1, 130, 6, 60)
            self.gridLayout.addWidget(self.eqTableGUI, 1, 3, 1, 1)
            # selNodeLab=QtGui.QLabel('Selected node:')
            # selNodeLab.setFont(selNodeFont)
            # self.gridLayout.addWidget(selNodeLab,0,140,1,30)
            # self.gridLayout.addWidget(self.clickedNodeLab, 0, 153, 1, 30)
            # self.gridLayout.addWidget(selNodeLab,0,3,1,1)
            self.gridLayout.addWidget(self.clickedNodeLab, 0, 3, 1, 1)

            self.fitGUI = FitCanvas(self.modApp)
            # self.gridLayout.addWidget(self.fitGUI, 7, 130, 6, 60)
            self.gridLayout.addWidget(self.fitGUI, 2, 3, 2, 1)

            # self.buttonCompromis = QtGui.QPushButton('Compromise', self)
            # self.buttonFitness = QtGui.QPushButton('Fitness', self)
            # self.buttonComplexite = QtGui.QPushButton('Complexity', self)
            # self.buttonOptUgp3 = QtGui.QPushButton('Global Optimisation', self)
            # self.buttonShowModGlobal = QtGui.QPushButton('Show Global Model', self)
            # self.buttonHideModGlobal = QtGui.QPushButton('Hide Global Model', self)
            # self.buttonChangerEq = QtGui.QPushButton('Change equation', self)
            # self.buttonRemoveLink = QtGui.QPushButton('Remove Link', self)
            # self.buttonReinstateLink = QtGui.QPushButton('Reinstate', self)
            # self.buttonHelp = QtGui.QPushButton('Help', self)
            # self.buttonCompromis.setStyleSheet("background-color: grey")

            # self.gridLayout.addWidget(self.buttonCompromis, 10, 0, 1, 15)
            # self.gridLayout.addWidget(self.buttonFitness, 10, 15, 1, 15)
            # self.gridLayout.addWidget(self.buttonComplexite, 10, 30, 1, 15)
            # self.gridLayout.addWidget(self.buttonOptUgp3, 10, 45, 1, 15)
            # self.gridLayout.addWidget(self.buttonShowModGlobal, 11, 0, 1, 30)
            # self.gridLayout.addWidget(self.buttonHideModGlobal, 11, 30, 1, 30)
            # self.gridLayout.addWidget(self.buttonChangerEq, 12, 30, 1, 30)
            # self.gridLayout.addWidget(self.buttonRemoveLink, 12, 0, 1, 30)
            # self.gridLayout.addWidget(self.buttonReinstateLink, 0, 12, 1, 8)
            #        self.gridLayout.addWidget(self.buttonHelp, 0, 120, 1, 12)

            # self.scrolledListBox = QtGui.QComboBox(self)
            # self.gridLayout.addWidget(self.scrolledListBox, 0, 1, 1, 1)


            # self.font = QtGui.QFont('Liberation Sans Narrow')
            # self.font.setPointSize(12)
            # self.setFont(self.font)

            self.eqTableGUI.setAttribute(Qt.WA_AcceptTouchEvents)

            self.main_widget.setFocus()
            self.setCentralWidget(self.main_widget)
            # self.show()
            self.updateView()

    def updateRightClickMenu(self,cntrApp,event,nodeclicked):
        rightclickMenu=QtGui.QMenu(self)
        if(nodeclicked in self.modApp.forbiddenNodes):
            restoreAction= QtGui.QAction("Restore " + nodeclicked,self)
            restoreAction.triggered.connect(lambda: cntrApp.restoreNode(nodeclicked))
            rightclickMenu.addAction(restoreAction)
        else:
            removeAction = QtGui.QAction("Remove " + nodeclicked,self)
            removeAction.triggered.connect(lambda :cntrApp.removeNode(nodeclicked))
            rightclickMenu.addAction(removeAction)
        recomputeAction=QtGui.QAction("Recompute " + nodeclicked,self)
        recomputeAction.triggered.connect(lambda: cntrApp.recomputeNode(nodeclicked))
        rightclickMenu.addAction(recomputeAction)
        rightclickMenu.addAction("Cancel")
        #rightclickMenu.addAction("Restart "+ nodeclicked)

        yPxlSizeFig=int((self.networkGUI.fig.get_size_inches()*self.networkGUI.fig.dpi)[1])
        rightclickMenu.move(self.networkGUI.mapToGlobal(QPoint(event.x, yPxlSizeFig-event.y)))
        rightclickMenu.show()
        #self.gridLayout.addWidget(rightclickMenu,3,4,1,1)

    def updateMenuBar(self, cntrApp):
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        helpAction = QtGui.QAction("&Show help", self)
        helpAction.setStatusTip("Display Help")
        helpAction.triggered.connect(cntrApp.clickHelp)

        optmAction = QtGui.QAction("&Optimize model",self)
        optmAction.setStatusTip("Start global optimisation process")
        optmAction.triggered.connect(cntrApp.clickOptmuGP)

        viewGroupAction = QtGui.QActionGroup(self, exclusive=True)

        self.cmAction = QtGui.QAction("&Compromise", self, checkable=True)
        self.cmAction.triggered.connect(cntrApp.clickCompromis)
        comproAction = viewGroupAction.addAction(self.cmAction)
        ftAction = QtGui.QAction("&Fitness", self, checkable=True)
        ftAction.triggered.connect(cntrApp.clickFitness)
        ftAction.activate(QtGui.QAction.Trigger)
        fitnesAction = viewGroupAction.addAction(ftAction)
        cpAction = QtGui.QAction("&Complexity", self, checkable=True)
        cpAction.triggered.connect(cntrApp.clickCmplx)
        compleAction = viewGroupAction.addAction(cpAction)
        saAction = QtGui.QAction("&Sensitivity Analysis", self, checkable=True)
        saAction.triggered.connect(cntrApp.clickSA)
        stvAnlsAction = viewGroupAction.addAction(saAction)
        psAction = QtGui.QAction("&Pearson correlation", self, checkable=True)
        psAction.triggered.connect(cntrApp.clickPearson)
        PearsonAction = viewGroupAction.addAction(psAction)

        self.showAction = QtGui.QAction("&Show Global model", self, checkable=True)
        self.showAction.triggered.connect(self.viewGlobalModel)
        self.showActionS = cntrApp.clickShowModGlobal
        self.showActionH = cntrApp.clickHideModGlobal
        #TODO ShowAction connectors

#        self.constrainAction =


        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exitAction)


        constrainAction = QtGui.QAction("&Add constrain", self)
        constrainAction.triggered.connect(cntrApp.clickRemoveLink)

        newVariable = QtGui.QAction("&New hierarchical variable", self)
        newVariable.triggered.connect(lambda : print("Wololo"))

        self.editMenu = menubar.addMenu("&Edit")
        self.editMenu.addAction(newVariable)
        self.editMenu.addAction(constrainAction)
        self.editMenu.addSeparator()

        viewMenu = menubar.addMenu("&View")
        viewMenu.addAction(comproAction)
        viewMenu.addAction(fitnesAction)
        viewMenu.addAction(compleAction)
        viewMenu.addAction(stvAnlsAction)
        viewMenu.addAction(psAction)
        viewMenu.addSeparator()
        viewMenu.addAction(self.showAction)


        opmMenu = menubar.addMenu("&Optimisation")
        opmMenu.addAction(optmAction)

        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(helpAction)

        self.mapper = QtCore.QSignalMapper(self)
        self.mapper.mapped['QString'].connect(self.removeConstrain)



    def viewGlobalModel(self):
        if self.showAction.isChecked():
            print("ok")
            self.showActionS()
        else:
            print("nok")
            self.showActionH()

    def addConstrain(self, name):
        constrainAction = QtGui.QAction(name, self)
        constrainAction.setStatusTip('Remove this constrain')
        self.mapper.setMapping(constrainAction,name)
        constrainAction.triggered.connect(self.mapper.map)
        self.editMenu.addAction(constrainAction)
        self.modApp.scrolledList.append(name)
        #self.modApp.computeEdgeBold()
        #self.modApp.computeNxGraph()
        #self.networkGUI.network.axes.clear()
        #self.networkGUI.network.updateView()
        #self.networkGUI.network.updateNodes()
        #self.networkGUI.network.updateLabels()
        #self.networkGUI.network.drawEdges()
        #self.updateView()


    def removeConstrain(self,name,isRestoreByNode=False):
        #print("Inside")
        self.modApp.debugCmp+=1
        print("Cmp:" + str(self.modApp.debugCmp))
        print("removing : " + name)
        b=len(self.editMenu.actions())
        print("sizeActionB=" + str(len(self.editMenu.actions())))
        self.editMenu.removeAction(self.mapper.mapping(name))
        self.mapper.removeMappings(self.mapper.mapping(name))
        a=len(self.editMenu.actions())
        print("sizeActionA=" + str(len(self.editMenu.actions())))
        if(b==a):
            a=''
            print(a)
        self.cntrApp.clickReinstateLink(name,isRestoreByNode)

        #try:
        #    self.modApp.scrolledList.remove(name)
        #except:
        #    print("No such link.")
        #    return
        #self.modApp.computeEdgeBold()
        #self.modApp.computeNxGraph()
        #self.networkGUI.network.axes.clear()
        #self.networkGUI.network.updateNodes()
        #self.networkGUI.network.updateLabels()
        #self.networkGUI.network.drawEdges()
        #self.updateView()
        #remove de la liste aussi peu être histoire que ça soit pas trop inutile.

    def noEquationError(self):
        msg=QtGui.QMessageBox()
        s="Impossible to start the optimisation while the following node have no candidate equations.\nRemove the nodes from the model or restart a local optimisation on them :\n"
        for v in self.modApp.nodesWithNoEquations:
            s+="\t" + v + "\n"
        msg.setText(s)
        msg.exec()
    def updateView(self):
        if(self.modApp.globalModelView==True):
            pass
        self.networkGUI.network.updateView()

        if(not self.modApp.lastNodeClicked==None):
            self.uncertaintyModifTxt.setText(str(self.modApp.dataset.variablesUncertainty[self.modApp.lastNodeClicked]))
        else:
            self.uncertaintyModifTxt.setText('')
        self.fitGUI.updateView()
        self.eqTableGUI.updateView()
        # self.selectContrTxtLab.setText(self.modApp.lastNodeClicked)

        if(self.modApp.lastNodeClicked != None):
            self.clickedNodeLab.setText('Selected node: ' + self.modApp.lastNodeClicked)
        #
        #self.scrolledListBox.clear()
        self.clickedNodeLab.setText(self.modApp.lastNodeClicked)
        #for item in self.modApp.scrolledList:
        #    self.scrolledListBox.addItem(item)
        self.incMatGUI.updateView()

