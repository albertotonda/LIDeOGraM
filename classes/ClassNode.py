class ClassNode:
    def __init__(self, name, nodeList: list=[], pos=(0, 0), color="white", lineWidth=1):
        self.color = color
        self.name = name
        self.nodeList = nodeList
        self.pos = pos
        self.lineWidth = lineWidth

    def __str__(self):
        return str(self.name)
