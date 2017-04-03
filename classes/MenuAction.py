import classes.ClassNode as ClassNode
from PyQt4 import QtGui

class MenuAction:
    @staticmethod
    def setWindow(window):
        MenuAction.window = window
        print("init")

    @staticmethod
    def addNode():
        rep = QtGui.QInputDialog.getText(MenuAction.window, "New class", "Class name :")
        if rep[1]:
            node =ClassNode.ClassNode(rep[0], [])
            MenuAction.window.graph.add_node(node)
            MenuAction.window.selectedNode.lineWidth = 1
            MenuAction.window.notify(node)