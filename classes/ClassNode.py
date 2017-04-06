import random
from PyQt4 import QtGui

class ClassNode:

    @staticmethod
    def nextColor():
        if len(ClassNode.color) > 0:
            return ClassNode.color.pop(0)
        else:
            r = random.random()
            g = random.random()
            b = random.random()
            return tuple((r, g, b))

    def __init__(self, name, nodeList: list, pos=(0, 0), color=None, lineWidth=0, size=300):
        if color == None:
            color = ClassNode.nextColor()
        self.color = color
        self.name = name
        self.nodeList = nodeList
        self.pos = pos
        self.lineWidth = lineWidth
        self.size = size

    def __str__(self):
        return str(self.name)

    def rename(self):
        from classes.MenuAction import MenuAction
        rep = QtGui.QInputDialog.getText(MenuAction.window, "Rename class", "Class' new name :")
        if rep[1]:
            self.name = rep[0]

    def changeColor(self):
        from classes.MenuAction import MenuAction
        print(self.color)
        rep = QtGui.QColorDialog.getColor(QtGui.QColor(self.color[0]*255, self.color[1]*255, self.color[2]*255) ,MenuAction.window, "Class' color")
        if rep.isValid():
            self.color = (rep.red() / 255, rep.green() / 255, rep.blue() / 255,)



    color = [(0.8, 0.8, 0.2), (0.7, 0.7, 0.2), (0.6, 0.6, 0.2)]
