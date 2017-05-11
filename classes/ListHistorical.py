from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class ListHistorical(QtGui.QListWidget):
    def __init__(self, undoRedo):
        QtGui.QListWidget.__init__(self)
        self.setMaximumWidth(250)
        self.undoRedo = undoRedo
        self.paint()
        self.itemClicked.connect(undoRedo.returnToState)

    def paint(self):
        selected = False
        self.clear()
        self.setWordWrap(True)
        #self.setTextElideMode(Qt.ElideMiddle)
        for state in self.undoRedo.redoStack:
            item = QtGui.QListWidgetItem(state[1])
            item.state = state
            item.setBackgroundColor(QtGui.QColor(state[2][0], state[2][1], state[2][2]))
            item.setFont(QtGui.QFont("AnyStyle", 14, QtGui.QFont.Normal))
            self.addItem(item)
            self.addSeparator()



        # if self.undoRedo.redoStack:
        #     selectedItem = QtGui.QListWidgetItem(self.undoRedo.redoStack[0][1])
        #     selectedItem.setSelected(True)
        #     self.addItem(selectedItem)

        lastState = None
        for state in reversed(self.undoRedo.undoStack):
            item = QtGui.QListWidgetItem(state[1])
            item.setBackgroundColor(QtGui.QColor(state[2][0], state[2][1], state[2][2]))
            item.setFont(QtGui.QFont("AnyStyle", 14, QtGui.QFont.Normal))
            self.addItem(item)
            if not selected:
                selected = True
                self.setItemSelected(item, True)

            item.state = lastState
            lastState = state
            self.addSeparator()


        initItem = QtGui.QListWidgetItem("Initial graph")
        initItem.setFont(QtGui.QFont("AnyStyle", 14, QtGui.QFont.Normal))
        self.addItem(initItem)
        if not selected:
            self.setItemSelected(initItem, True)
        initItem.state = lastState

        self.wordWrap()
        #self.connect(self, QtCore.SIGNAL("itemClicked(QListWidgetItem)"), self, QtCore.SLOT("test(self, QListWidgetItem)"))

    def addSeparator(self):
        separator = QtGui.QListWidgetItem()
        separator.setSizeHint(QtCore.QSize(-1, 5))
        separator.setFlags(Qt.NoItemFlags)
        separFrame = QtGui.QFrame()
        separator.state = None
        separFrame.setFrameShape(QtGui.QFrame.HLine)
        self.addItem(separator)
        self.setItemWidget(separator, separFrame)

