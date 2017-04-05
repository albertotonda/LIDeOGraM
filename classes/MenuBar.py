from PyQt4 import QtGui
from classes.MenuAction import MenuAction


class MenuBar:

    def __init__(self, window):
        MenuAction.setWindow(window)

        exitAction = QtGui.QAction('&Exit', window)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        addNodeAction = QtGui.QAction('&Add Node', window)
        addNodeAction.setStatusTip('Add Node')
        addNodeAction.triggered.connect(MenuAction.addNode)

        menubar = window.menuBar()

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exitAction)

        editMode = QtGui.QActionGroup(window, exclusive=True)

        moveModeAction = QtGui.QAction("&Move node", window, checkable=True)
        moveModeAction.triggered.connect(MenuAction.setMoveMode)
        moveModeAction.activate(QtGui.QAction.Trigger)
        moveMode = editMode.addAction(moveModeAction)

        newEdgeModeAction = QtGui.QAction("&New Edge", window, checkable=True)
        newEdgeModeAction.triggered.connect(MenuAction.setAddEdgeMode)
        newEdgeMode = editMode.addAction(newEdgeModeAction)

        cpAction = QtGui.QAction("&Del Edge", window, checkable=True)
        cpAction.triggered.connect(MenuAction.setDelEdgeMode)
        delEdgeMode = editMode.addAction(cpAction)

        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(addNodeAction)
        editMenu.addSeparator()
        editMenu.addAction(moveMode)
        editMenu.addAction(newEdgeMode)
        editMenu.addAction(delEdgeMode)

