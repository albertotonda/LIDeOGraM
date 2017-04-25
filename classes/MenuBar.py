from PyQt4 import QtGui
from classes.MenuAction import MenuAction


class MenuBar:

    def __init__(self, window, toolButtons):
        MenuAction.setWindow(window)

        exitAction = QtGui.QAction('&Exit', window)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        addNodeAction = QtGui.QAction('&Add Node', window)
        addNodeAction.setStatusTip('Add Node')
        addNodeAction.triggered.connect(MenuAction.addNode)

        saveAction = QtGui.QAction('&Save', window)
        saveAction.setStatusTip('Save')
        saveAction.triggered.connect(MenuAction.save)

        loadAction = QtGui.QAction('&Load', window)
        loadAction.setStatusTip('Load')
        loadAction.triggered.connect(MenuAction.load)

        menubar = window.menuBar()

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)

        editMode = QtGui.QActionGroup(window, exclusive=True)


        moveModeAction = QtGui.QAction("&Move node", window, checkable=True)
        toolButtons[0].setMenuAction(moveModeAction)
        moveModeAction.triggered.connect(toolButtons[0].changeMode)
        moveModeAction.activate(QtGui.QAction.Trigger)
        moveMode = editMode.addAction(moveModeAction)

        newEdgeModeAction = QtGui.QAction("&New Edge", window, checkable=True)
        toolButtons[1].setMenuAction(newEdgeModeAction)
        newEdgeModeAction.triggered.connect(toolButtons[1].changeMode)
        newEdgeMode = editMode.addAction(newEdgeModeAction)

        delEdgeAction = QtGui.QAction("&Del Edge", window, checkable=True)
        toolButtons[2].setMenuAction(delEdgeAction)
        delEdgeAction.triggered.connect(toolButtons[2].changeMode)
        delEdgeMode = editMode.addAction(delEdgeAction)

        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(addNodeAction)
        editMenu.addSeparator()
        editMenu.addAction(moveMode)
        editMenu.addAction(newEdgeMode)
        editMenu.addAction(delEdgeMode)

