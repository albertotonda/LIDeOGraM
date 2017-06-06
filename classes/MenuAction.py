from classes.ClassMode import ClassMode
from PyQt4 import QtGui
import time
class MenuAction:
    @staticmethod
    def setWindow(window):
        MenuAction.window = window

    @staticmethod
    def addNode():
        from classes.ClassNode import ClassNode
        rep = QtGui.QInputDialog.getText(MenuAction.window, "New class", "Class name :")
        if (MenuAction.window.isLog):
            f = open(MenuAction.window.LogFilename, "a")
            f.write("t:" + str(time.time()) + " " + "AddNode:" +str(rep) + "\n")
            f.close()
        if rep[1]:
            MenuAction.window.saveGraphState("+ New class : "+rep[0], color=(200, 255, 200))
            node = ClassNode(rep[0], [], pos=MenuAction.window.canv.center)
            MenuAction.window.canv.graph.add_node(node)
            if MenuAction.window.selectedNode:
                MenuAction.window.selectedNode.lineWidth = 1
            MenuAction.window.notify(node)

    @staticmethod
    def setMoveMode():
        if (MenuAction.window.isLog):
            f = open(MenuAction.window.LogFilename, "a")
            f.write("t:" + str(time.time()) + " " + "MoveModeMenu" + "\n")
            f.close()
        MenuAction.window.canv.mode = ClassMode.moveMode

    @staticmethod
    def setAddEdgeMode():
        print("testAddEdge")
        if (MenuAction.window.isLog):
            f = open(MenuAction.window.LogFilename, "a")
            f.write("t:" + str(time.time()) + " " + "AddEdgeModeMenu" + "\n")
            f.close()
        MenuAction.window.canv.mode = ClassMode.addEdgeMode

    @staticmethod
    def setDelEdgeMode():
        if (MenuAction.window.isLog):
            f = open(MenuAction.window.LogFilename, "a")
            f.write("t:" + str(time.time()) + " " + "DelEdgeModeMenu" + "\n")
            f.close()
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

        if(MenuAction.window.isLog):
            f=open(MenuAction.window.LogFilename,"a")
            f.write("t:"+str(time.time())+" "+"Loading:"+str(rep)+"\n")
            f.close()
        if rep:
            print(rep)
            MenuAction.window.graph = ClassGraph.readJson(rep)
            MenuAction.window.canv.graph = ClassGraph.readJson(rep)
            MenuAction.window.undoRedo.clear()
            MenuAction.window.notify()
