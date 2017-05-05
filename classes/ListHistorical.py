from PyQt4 import QtGui

class ListHistorical(QtGui.QListWidget):
    def __init__(self, undoRedo):
        QtGui.QListWidget.__init__(self)
        self.setMaximumWidth(250)
        self.undoRedo = undoRedo
        self.paint()

    def paint(self):
        self.clear()
        for state in self.undoRedo.undoStack:
            self.addItem(QtGui.QListWidgetItem(state[1]))
        self.addItem(QtGui.QListWidgetItem("Current"))
        if self.undoRedo.redoStack:
            selectedItem = QtGui.QListWidgetItem(self.undoRedo.redoStack[0][0])

