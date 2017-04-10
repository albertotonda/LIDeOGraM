#-*- coding: utf-8
from PyQt5 import QtGui, QtCore, QtWidgets

from NetworkCanvas import NetworkCanvas
from EqTableCanvas import EqTableCanvas
from IncMatrixCanvas import IncMatrixCanvas
from FitCanvas import FitCanvas
from OnOffCheckBox import *
from PyQt5.Qt import QPoint




# TODO Crée tout les boutons (or graphes + équations)
class RFGraph_View(QtWidgets.QMainWindow):

    def __init__(self,modApp):


        self.modApp=modApp




        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.setWindowTitle(QtWidgets.QLabel("Test"))
        self.setWindowTitle("LIDeoGraM")
        self.icon = QtGui.QIcon("Icone.png")
        self.setWindowIcon(self.icon)

        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.main_widget = QtWidgets.QWidget(self)

        self.gridLayout = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)
        self.networkGUI = NetworkCanvas(self.modApp, self)
        #self.gridLayout.addWidget(self.networkGUI, 1, 0, 7, 60)
        self.gridLayout.addWidget(self.networkGUI, 1, 0, 2, 2)
        self.incMatGUI = IncMatrixCanvas(self.modApp,self)
        self.gridLayout.addWidget(self.incMatGUI,1,2,3,1)
        self.adjThreshold_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.adjThreshold_slider.setValue(self.modApp.adjThresholdVal * 100)

        self.adjThreshold_lab = QtWidgets.QLabel('Edges importance : ')
        self.gridLayout.addWidget(self.adjThreshold_lab, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.adjThreshold_slider, 3, 1, 1, 1)


        self.comprFitCmplx_lab_fit = QtWidgets.QLabel('Fitness')
        self.selectContrTxtLab = QtWidgets.QLabel('')
        self.gridLayout.addWidget(self.selectContrTxtLab, 0, 1, 1, 1)
        selectContrFont = QtGui.QFont("AnyStyle", 14, QtGui.QFont.DemiBold)
        self.selectContrTxtLab.setFont(selectContrFont)


        self.clickedNodeLab = QtWidgets.QLabel('Selected node:')
        selNodeFont=QtGui.QFont("AnyStyle",14,QtGui.QFont.DemiBold)
        self.clickedNodeLab.setFont(selNodeFont)
        self.eqTableGUI = EqTableCanvas(self.modApp)
        self.gridLayout.addWidget(self.eqTableGUI, 1, 3, 1, 1)
        #selNodeLab=QtWidgets.QLabel('Selected node:')
        #selNodeLab.setFont(selNodeFont)
        #self.gridLayout.addWidget(selNodeLab,0,140,1,30)
        #self.gridLayout.addWidget(self.clickedNodeLab, 0, 153, 1, 30)
        #self.gridLayout.addWidget(selNodeLab,0,3,1,1)
        self.gridLayout.addWidget(self.clickedNodeLab, 0, 3, 1, 1)




        self.fitGUI = FitCanvas(self.modApp)
        self.gridLayout.addWidget(self.fitGUI, 2, 3, 2, 1)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.show()
        self.updateView()

    def updateRightClickMenu(self,cntrApp,event,nodeclicked):
        rightclickMenu=QtWidgets.QMenu(self)
        if(nodeclicked in self.modApp.forbiddenNodes):
            restoreAction= QtWidgets.QAction("Restore " + nodeclicked,self)
            restoreAction.triggered.connect(lambda: cntrApp.restoreNode(nodeclicked))
            rightclickMenu.addAction(restoreAction)
        else:
            removeAction = QtWidgets.QAction("Remove " + nodeclicked,self)
            removeAction.triggered.connect(lambda :cntrApp.removeNode(nodeclicked))
            rightclickMenu.addAction(removeAction)
        recomputeAction=QtWidgets.QAction("Recompute " + nodeclicked,self)
        recomputeAction.triggered.connect(lambda: cntrApp.recomputeNode(nodeclicked))
        rightclickMenu.addAction(recomputeAction)
        rightclickMenu.addAction("Cancel")
        #rightclickMenu.addAction("Restart "+ nodeclicked)

        yPxlSizeFig=int((self.networkGUI.fig.get_size_inches()*self.networkGUI.fig.dpi)[1])
        rightclickMenu.move(self.networkGUI.mapToGlobal(QPoint(event.x, yPxlSizeFig-event.y)))
        rightclickMenu.show()
        #self.gridLayout.addWidget(rightclickMenu,3,4,1,1)


    def tooltips(self, cntrApp, event, nodeclicked):
        if nodeclicked in self.modApp.dataset.nodeDescription.index:
            infos = self.modApp.dataset.nodeDescription.ix[nodeclicked].to_string()
            print(infos)
        #ttips = QtGui.QTooltip()
        #yPxlSizeFig = int((self.networkGUI.fig.get_size_inches() * self.networkGUI.fig.dpi)[1])
        #ttips.showText((QPoint(event.x, yPxlSizeFig - event.y)), infos)

            #yPxlSizeFig = int((self.networkGUI.fig.get_size_inches() * self.networkGUI.fig.dpi)[1])
            #rightclickMenu.move(self.networkGUI.mapToGlobal(QPoint(event.x, yPxlSizeFig - event.y)))
            #rightclickMenu.show()
            # self.gridLayout.addWidget(rightclickMenu,3,4,1,1)

    def updateMenuBar(self, cntrApp):
        exitAction = QtWidgets.QAction('&Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        helpAction = QtWidgets.QAction("&Show help", self)
        helpAction.setStatusTip("Display Help")
        helpAction.triggered.connect(cntrApp.clickHelp)

        optmAction = QtWidgets.QAction("&Optimize model",self)
        optmAction.setStatusTip("Start global optimisation process")
        optmAction.triggered.connect(cntrApp.clickOptmuGP)

        viewGroupAction = QtWidgets.QActionGroup(self, exclusive=True)

        self.cmAction = QtWidgets.QAction("&Compromise", self, checkable=True)
        self.cmAction.triggered.connect(cntrApp.clickCompromis)
        comproAction = viewGroupAction.addAction(self.cmAction)
        ftAction = QtWidgets.QAction("&Fitness", self, checkable=True)
        ftAction.triggered.connect(cntrApp.clickFitness)
        ftAction.activate(QtWidgets.QAction.Trigger)
        fitnesAction = viewGroupAction.addAction(ftAction)
        cpAction = QtWidgets.QAction("&Complexity", self, checkable=True)
        cpAction.triggered.connect(cntrApp.clickCmplx)
        compleAction = viewGroupAction.addAction(cpAction)

        self.showAction = QtWidgets.QAction("&Show Global model", self, checkable=True)
        self.showAction.triggered.connect(self.viewGlobalModel)
        self.showActionS = cntrApp.clickShowModGlobal
        self.showActionH = cntrApp.clickHideModGlobal
        #TODO ShowAction connectors

        chEqAction = QtWidgets.QAction("&Edit equation", self)
        chEqAction.triggered.connect(cntrApp.clickChangeEq)

#        self.constrainAction =


        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exitAction)

        self.editmenu = menubar.addMenu("&Edit")



        viewMenu = menubar.addMenu("&View")
        viewMenu.addAction(comproAction)
        viewMenu.addAction(fitnesAction)
        viewMenu.addAction(compleAction)
        viewMenu.addSeparator()
        viewMenu.addAction(self.showAction)


        opmMenu = menubar.addMenu("&Optimisation")
        opmMenu.addAction(optmAction)
        opmMenu.addAction(chEqAction)

        constrainAction = QtWidgets.QAction("&Add constrain", self)
        constrainAction.triggered.connect(cntrApp.clickRemoveLink)


        self.constrainMenu = menubar.addMenu("&Constrains")
        self.constrainMenu.addAction(constrainAction)
        self.constrainMenu.addSeparator()

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
        constrainAction = QtWidgets.QAction(name, self)
        constrainAction.setStatusTip('Remove this constrain')
        self.mapper.setMapping(constrainAction,name)
        constrainAction.triggered.connect(self.mapper.map)

        self.constrainMenu.addAction(constrainAction)
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
        b=len(self.constrainMenu.actions())
        print("sizeActionB="+str(len(self.constrainMenu.actions())))
        self.constrainMenu.removeAction(self.mapper.mapping(name))
        self.mapper.removeMappings(self.mapper.mapping(name))
        a=len(self.constrainMenu.actions())
        print("sizeActionA=" + str(len(self.constrainMenu.actions())))
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
        self.fitGUI.updateView()
        self.eqTableGUI.updateView()

        if(self.modApp.lastNodeClicked != None):
            self.clickedNodeLab.setText('Selected node: ' + self.modApp.lastNodeClicked)
        self.clickedNodeLab.setText(self.modApp.lastNodeClicked)
        self.incMatGUI.updateView()

