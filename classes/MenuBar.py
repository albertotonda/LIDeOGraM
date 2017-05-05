from PyQt4 import QtGui
from classes.MenuAction import MenuAction


class MenuBar:

    def __init__(self, window, toolButtons):
        MenuAction.setWindow(window)

        #----- File -----#

        exitAction = QtGui.QAction('&Exit', window)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

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

        # ----- File -----#

        editMode = QtGui.QActionGroup(window, exclusive=True)

        undoAction = QtGui.QAction('&Undo', window)
        undoAction.setStatusTip('Undo')
        undoAction.triggered.connect(window.undoGraphState)
        undoAction.setDisabled(True)
        window.undoRedo.addActionEmptyUndo(lambda: undoAction.setDisabled(True))
        window.undoRedo.addActionNonEmptyUndo(lambda: undoAction.setDisabled(False))

        redoAction = QtGui.QAction('&Redo', window)
        redoAction.setStatusTip('Redo')
        redoAction.triggered.connect(window.redoGraphState)
        redoAction.setDisabled(True)
        window.undoRedo.addActionEmptyRedo(lambda: redoAction.setDisabled(True))
        window.undoRedo.addActionNonEmptyRedo(lambda: redoAction.setDisabled(False))

        addNodeAction = QtGui.QAction('&Add Node', window)
        addNodeAction.setStatusTip('Add Node')
        addNodeAction.triggered.connect(MenuAction.addNode)

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
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        editMenu.addSeparator()
        editMenu.addAction(addNodeAction)
        editMenu.addSeparator()
        editMenu.addAction(moveMode)
        editMenu.addAction(newEdgeMode)
        editMenu.addAction(delEdgeMode)

