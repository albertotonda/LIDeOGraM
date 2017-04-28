from classes.ClassMode import ClassMode
from PyQt4 import QtGui

class MenuAction:
    @staticmethod
    def setWindow(window):
        MenuAction.window = window

    @staticmethod
    def addNode():
        from classes.ClassNode import ClassNode
        rep = QtGui.QInputDialog.getText(MenuAction.window, "New class", "Class name :")
        if rep[1]:
            node = ClassNode(rep[0], [])
            MenuAction.window.graph.add_node(node)
            if MenuAction.window.selectedNode:
                MenuAction.window.selectedNode.lineWidth = 1
            MenuAction.window.notify(node)

    @staticmethod
    def setMoveMode():
        MenuAction.window.canv.mode = ClassMode.moveMode

    @staticmethod
    def setAddEdgeMode():
        MenuAction.window.canv.mode = ClassMode.addEdgeMode

    @staticmethod
    def setDelEdgeMode():
        MenuAction.window.canv.mode = ClassMode.delEdgeMode

    @staticmethod
    def save():
        rep = QtGui.QFileDialog.getSaveFileName(MenuAction.window, caption="Save the class graph", filter="Class Graph (*.clgraph)")
        if rep:
            MenuAction.window.canv.graph.toJSON(rep)

    @staticmethod
    def load():
        from classes.ClassGraph import ClassGraph
        rep = QtGui.QFileDialog.getOpenFileName(MenuAction.window, filter="Class Graph (*.clgraph)")
        if rep:
            print(rep)
            MenuAction.window.graph = ClassGraph.readJson(rep)
            MenuAction.window.canv.graph = ClassGraph.readJson(rep)

            MenuAction.window.notify()




