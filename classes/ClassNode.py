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

    def __init__(self, name, nodeList: list, pos=None, color=None, lineWidth=0, size=700):
        if color is None:
            color = ClassNode.nextColor()
        if pos is None:
            pos = (random.random(), random.random())
        self.color = color
        self.name = name
        self.nodeList = nodeList
        self.pos = pos
        self.lineWidth = lineWidth
        self.size = size

    def __str__(self):
        return str(self.name)

    def rename(self, beforeChange=None):
        from classes.MenuAction import MenuAction
        rep = QtGui.QInputDialog.getText(MenuAction.window, "Rename class", "Class' new name :", text=self.name)
        if rep[1]:
            if beforeChange:
                beforeChange("Rename "+self.name + " into " + rep[0], color=(255, 255, 150))
            self.name = rep[0]

    def changeColor(self, beforeChange=None):
        from classes.MenuAction import MenuAction
        print(self.color)
        rep = QtGui.QColorDialog.getColor(QtGui.QColor(self.color[0]*255, self.color[1]*255, self.color[2]*255) ,MenuAction.window, "Class' color")
        if rep.isValid() and [int(c * 255) for c in self.color] != [rep.red(), rep.green(), rep.blue()]:
            if beforeChange:
                beforeChange("Change the color of " + self.name, color=(255, 255, 150))
            self.color = (rep.red()/255, rep.green()/255, rep.blue()/255)


    color = [(31,120,180), (178,223,138), (227,26,28), (253,191,111), (106,61,154), (166,206,227), (51,160,44), (251,154,153), (255,127,0), (202,178,214), (177,89,40)]
    for n in range(len(color)):
        color[n] = (color[n][0]/255, color[n][1]/255, color[n][2]/255)
    print(color)
