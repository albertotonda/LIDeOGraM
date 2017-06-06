#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QCoreApplication, Qt
from classes.CanvGraph import CanvGraph
from classes.FramAction import FramAction
from classes.ClassGraph import ClassGraph
from classes.MenuBar import MenuBar
import copy
from classes.ToolMenu import ToolMenu
from classes.SaveStatesStacks import SaveStatesStacks
from classes.ListHistorical import ListHistorical
import time

class WindowClasses(QtGui.QMainWindow):

    def __init__(self, graph: ClassGraph,fctToCall,isLog=False,LogFilename=None):
        self.isLog=isLog
        self.LogFilename=LogFilename
        self.fctToCall=fctToCall
        self.graphReady = False

        QtGui.QMainWindow.__init__(self)
        self.mainWid = QtGui.QWidget(self)
        self.setWindowTitle("Class management")
        self.gridLayout = QtGui.QGridLayout(self.mainWid)
        self.mainWid.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # self.setWindowState(QtCore.Qt.WindowMaximized)

        self.setCentralWidget(self.mainWid)

        self.undoRedo = SaveStatesStacks(self)

        self.graph = copy.copy(graph)
        self.initialGraph = graph

        self.canv = CanvGraph(self.graph)
        self.canv.addObserver(self)

        self.frame = FramAction(graph.unboundNode)

        self.frame.button1.addObserver(self)
        self.frame.button2.addObserver(self)

        self.gridLayout.setSpacing(5)
        self.canv.setMinimumSize(200, 200)

        self.saveButton = QtGui.QPushButton("Validate")
        self.saveButton.clicked.connect(lambda: self.setReady(self.canv.graph))
        self.saveButton.setFont(QtGui.QFont("AnyStyle", 14, QtGui.QFont.Normal))

        editTools = ToolMenu(self, "edit")
        histTools = ToolMenu(self, "hist")

        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(lambda: self.setReady(self.initialGraph))
        self.cancelButton.setFont(QtGui.QFont("AnyStyle", 14, QtGui.QFont.Normal))

        self.historical = ListHistorical(self.undoRedo)

        self.gridLayout.addWidget(histTools, 0, 0, 1, 1)
        self.gridLayout.addWidget(editTools, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.historical, 1, 0, 2, 1)
        self.gridLayout.addWidget(self.canv, 1, 1, 2, 1)
        self.gridLayout.addWidget(self.frame, 0, 2, 2, 2)
        self.gridLayout.addWidget(self.cancelButton, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.saveButton, 2, 3, 1, 1)


        self.selectedNode = None
        MenuBar(self, editTools.buttons)

        QtGui.QMainWindow.show(self)
        #self.exec()
        QtGui.QShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.Key_Z), self, self.undoGraphState)
        QtGui.QShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.Key_Y), self, self.redoGraphState)


    def notify(self, selectedNode=None, keepSelected = False):
        # if (self.isLog):
        #     f = open(self.LogFilename, "a")
        #     f.write("t:" + str(time.time()) + " " + "notify:" + selectedNode + "\n")
        #     f.close()
        if keepSelected:
            selectedNode = self.selectedNode
        else:
            self.selectedNode = selectedNode
        self.canv.paint(selectedNode)
        self.frame.setListsValues(self.canv.graph.unboundNode, selectedNode)
        self.historical.paint()
        QCoreApplication.processEvents()

    def setReady(self, graph):
        if(self.isLog):
            f=open(self.LogFilename,"a")
            f.write("t:"+str(time.time())+" "+"ClassValide"+"\n")
            f.close()
        self.graph = graph
        self.graphReady = True
        print("pret !")
        self.fctToCall(self.graph)
        self.close()

    def saveGraphState(self, action="Unknown action", color: tuple = (0, 0, 0)):
        if (self.isLog):
            f=open(self.LogFilename,"a")
            f.write("t:"+str(time.time())+" "+"SaveGraph"+"\n")
            f.close()
        self.undoRedo.saveState(self.canv.graph, action, color)

    def undoGraphState(self):
        if (self.isLog):
            f=open(self.LogFilename,"a")
            f.write("t:"+str(time.time())+" "+"UndoGraph"+"\n")
            f.close()
        g = self.undoRedo.undo(self.canv.graph)
        if g:
            self.canv.graph = g
            self.notify()

    def redoGraphState(self):
        if (self.isLog):
            f=open(self.LogFilename,"a")
            f.write("t:"+str(time.time())+" "+"RedoGraph"+"\n")
            f.close()
        g = self.undoRedo.redo(self.canv.graph)
        if g:
            self.canv.graph = g
            self.notify()

    def popState(self):
        self.undoRedo.popLastState()