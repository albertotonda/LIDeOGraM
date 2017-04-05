import random


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

    def __init__(self, name, nodeList: list, pos=(0, 0), color=None, lineWidth=1, size=300):
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

    color = [(0.8, 0.8, 0.2), (0.7, 0.7, 0.2), (0.6, 0.6, 0.2)]
