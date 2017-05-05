from PyQt4 import QtGui, QtCore
from classes.ClassMode import ClassMode

class ToolMenu(QtGui.QFrame):
    def __init__(self, window):
        iconSize = 50
        QtGui.QFrame.__init__(self)
        layout = QtGui.QHBoxLayout()
        self.buttons = [
                        ToolModeButton(window.canv, ClassMode.moveMode, "ressources/images/move", iconSize),
                        ToolModeButton(window.canv, ClassMode.addEdgeMode, "ressources/images/NewEdge", iconSize),
                        ToolModeButton(window.canv, ClassMode.delEdgeMode, "ressources/images/DelEdge", iconSize),
                        UndoRedoButton(window, UndoRedoButton.undo, "ressources/images/Undo", iconSize),
                        UndoRedoButton(window, UndoRedoButton.redo, "ressources/images/Redo", iconSize)]
        layout.addWidget(self.buttons[3])
        layout.addItem(QtGui.QSpacerItem(60, 0))
        layout.addWidget(self.buttons[4])
        layout.addItem(QtGui.QSpacerItem(60, 0))
        layout.addWidget(self.buttons[0])
        layout.addItem(QtGui.QSpacerItem(60, 0))
        layout.addWidget(self.buttons[1])
        layout.addItem(QtGui.QSpacerItem(60, 0))
        layout.addWidget(self.buttons[2])

        #layout.setAlignment(QtCore.Qt.AlignHCenter)
        group = QtGui.QButtonGroup()
        group.addButton(self.buttons[0])
        group.addButton(self.buttons[1])
        group.addButton(self.buttons[2])
        self.setLayout(layout)
        self.setMaximumHeight(iconSize + 20)


class ToolModeButton(QtGui.QPushButton):
    def __init__(self, canv, modeToSet, iconName, iconSize):
        self.canv = canv
        self.modeToSet = modeToSet
        QtGui.QPushButton.__init__(self)
        self.clicked.connect(lambda e: self.changeMode())
        icon = QtGui.QIcon(QtGui.QPixmap(iconName))
        self.setIcon(icon)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setIconSize(QtCore.QSize(iconSize, iconSize))
        self.setMaximumSize(QtCore.QSize(iconSize, iconSize))

    def setMenuAction(self, menuAction):
        self.menuAction = menuAction

    def changeMode(self):
        self.canv.mode = self.modeToSet
        self.menuAction.setChecked(True)
        self.setChecked(True)

class UndoRedoButton(QtGui.QPushButton):
    undo = 0
    redo = 1

    def __init__(self, window, mode, iconName, iconSize):
        QtGui.QPushButton.__init__(self)
        icon = QtGui.QIcon(QtGui.QPixmap(iconName))
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(iconSize, iconSize))
        self.setMaximumSize(QtCore.QSize(iconSize, iconSize))
        self.setDisabled(True)
        if mode == UndoRedoButton.undo:
            self.clicked.connect(window.undoGraphState)
            window.undoRedo.addActionEmptyUndo(lambda: self.setDisabled(True))
            window.undoRedo.addActionNonEmptyUndo(lambda: self.setDisabled(False))
        else:
            self.clicked.connect(window.redoGraphState)
            window.undoRedo.addActionEmptyRedo(lambda: self.setDisabled(True))
            window.undoRedo.addActionNonEmptyRedo(lambda: self.setDisabled(False))