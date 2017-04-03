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

        actionMenu = menubar.addMenu("&Action")
        actionMenu.addAction(addNodeAction)


