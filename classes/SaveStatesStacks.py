import copy
from classes.ClassGraph import ClassGraph

class SaveStatesStacks:
    def __init__(self, window):
        self.undoStack = []
        self.redoStack = []

        self.emptyUndoFunc = []
        self.emptyRedoFunc = []
        self.nonEmptyUndoFunc = []
        self.nonEmptyRedoFunc = []

        self.window = window

    def saveState(self, graph: ClassGraph, actionName: str, color: tuple = (255, 255, 255)):
        if self.redoStack: #If not empty
            self.callFunc(self.emptyRedoFunc)
        self.redoStack = []

        if not self.undoStack: #If empty
            self.callFunc(self.nonEmptyUndoFunc)
        self.undoStack.append((copy.deepcopy(graph), actionName, color))

    def undo(self, currentGraph: ClassGraph):
        if not self.undoStack:
            print("Undo Stack empty")
            return
        if not self.redoStack:
            self.callFunc(self.nonEmptyRedoFunc)
        state = self.undoStack.pop()
        self.redoStack.append((currentGraph, state[1], state[2]))

        if not self.undoStack:
            self.callFunc(self.emptyUndoFunc)
        return state[0]

    def redo(self, currentGraph: ClassGraph):
        if not self.redoStack:
            print("Redo Stack empty")
            return
        if not self.undoStack: #If empty
            self.callFunc(self.nonEmptyUndoFunc)

        state = self.redoStack.pop()
        self.undoStack.append((currentGraph, state[1], state[2]))

        if not self.redoStack:
            self.callFunc(self.emptyRedoFunc)

        return state[0]

    def clear(self):
        self.undoStack = []
        self.redoStack = []
        self.callFunc(self.emptyUndoFunc)
        self.callFunc(self.emptyRedoFunc)

    def popLastState(self):
        self.undoStack.pop()
        if not self.undoStack:
            self.callFunc(self.emptyUndoFunc)

    def addActionEmptyUndo(self, f):
        self.emptyUndoFunc.append(f)

    def addActionEmptyRedo(self, f):
        self.emptyRedoFunc.append(f)

    def addActionNonEmptyUndo(self, f):
        self.nonEmptyUndoFunc.append(f)

    def addActionNonEmptyRedo(self, f):
        self.nonEmptyRedoFunc.append(f)

    def callFunc(self, funcList):
        for f in funcList:
            f()

    def returnToState(self, item):
        print("click : "+ str(item))
        if item.state is None:
            return
        graph = self.window.canv.graph
        if item.state in self.undoStack:
            action = self.undo
        elif item.state in self.redoStack:
            action = self.redo
        while graph != item.state[0]:
            graph = action(graph)
        self.window.canv.graph = graph
        self.window.notify()
