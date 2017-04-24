from PyQt4 import QtGui, QtCore

class AssignButton(QtGui.QPushButton):

    def clickAction(self):
        item = self.listIn.selectedItems()[0]
        self.nodeOut.append(item.node)
        self.nodeOut.sort()
        self.nodeIn.remove(self.listIn.selectedItems()[0].node)
        self.notifyAll()

    def __init__(self, text,):
        QtGui.QPushButton.__init__(self, text)
        self.clicked.connect(self.clickAction)
        self.observers = []

    def setLists(self, listIn: QtGui.QListWidget, listOut: QtGui.QListWidget, nodeIn: list, nodeOut: list):
        self.listIn = listIn
        self.listOut = listOut
        self.nodeIn = nodeIn
        self.nodeOut = nodeOut


    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyAll(self):
        for obs in self.observers:
            obs.notify(keepSelected=True)
