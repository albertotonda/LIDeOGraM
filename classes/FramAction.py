#-*- coding: utf-8
from PyQt4 import QtGui
import classes.ClassNode as ClassNode

class FramAction(QtGui.QFrame):
    def __init__(self, notSet):
        QtGui.QFrame.__init__(self)

        grid = QtGui.QGridLayout(self)
        self.grid = grid;
        self.setLayout(grid)

        self.labelAssigned = QtGui.QLabel("Select a node")
        grid.addWidget(self.labelAssigned, 0, 0, 1, 1)

        grid.addWidget(QtGui.QPushButton(">"), 1, 1, 2, 1)
        grid.addWidget(QtGui.QPushButton("<"), 2, 1, 2, 1)
        grid.addWidget(QtGui.QLabel("Not assigned : "), 0, 2, 1, 1)
        self.setListsValues(notSet)

    def setListsValues(self,notSet: list, selectedNode: ClassNode = None):
        listBound  = QtGui.QListWidget()
        listUnbound = QtGui.QListWidget()
        if selectedNode is not None:
            self.labelAssigned.setText("Assigned to "+str(selectedNode)+" : ")
            for node in selectedNode.nodeList:
                    listBound.addItem(QtGui.QListWidgetItem(node))
        else:
            self.labelAssigned.setText("Select a node")
        for node in notSet:
            listUnbound.addItem(QtGui.QListWidgetItem(node))

        self.grid.addWidget(listBound, 1, 0, 3, 1)
        self.grid.addWidget(listUnbound, 1, 2, 3, 1)
