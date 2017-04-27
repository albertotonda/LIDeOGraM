from PyQt4 import QtGui, QtCore
from classes.ClassMode import ClassMode

class ToolMenu(QtGui.QFrame):
    def __init__(self, canv):
        QtGui.QFrame.__init__(self)
        layout = QtGui.QHBoxLayout()
        self.buttons = [ToolButton(canv, ClassMode.moveMode, "ressources/images/move"),
                        ToolButton(canv, ClassMode.addEdgeMode, "ressources/images/NewEdge"),
                        ToolButton(canv, ClassMode.delEdgeMode, "ressources/images/DelEdge")]
        self.buttons[0]
        layout.addWidget(self.buttons[0])
        layout.addWidget(self.buttons[1])
        layout.addWidget(self.buttons[2])
        group = QtGui.QButtonGroup()
        group.addButton(self.buttons[0])
        group.addButton(self.buttons[1])
        group.addButton(self.buttons[2])
        self.setLayout(layout)
        self.setMaximumHeight(120)
        self.setMaximumWidth(340)

class ToolButton(QtGui.QPushButton):
    def __init__(self, canv, modeToSet, iconName):
        self.canv = canv
        self.modeToSet = modeToSet
        QtGui.QPushButton.__init__(self)
        self.clicked.connect(lambda e: self.changeMode())
        icon = QtGui.QIcon(QtGui.QPixmap(iconName))
        self.setIcon(icon)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setIconSize(QtCore.QSize(100, 100))

    def setMenuAction(self, menuAction):
        self.menuAction = menuAction

    def changeMode(self):
        self.canv.mode = self.modeToSet
        self.menuAction.setChecked(True)
        self.setChecked(True)
