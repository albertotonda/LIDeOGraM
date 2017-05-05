import copy
from classes.ClassGraph import ClassGraph

class SaveStatesStacks:
    def __init__(self):
        self.undoStack = []
        self.redoStack = []

        self.emptyUndoFunc = []
        self.emptyRedoFunc = []
        self.nonEmptyUndoFunc = []
        self.nonEmptyRedoFunc = []

    def saveState(self, graph: ClassGraph, actionName: str):
        if self.redoStack: #If not empty
            self.callFunc(self.emptyRedoFunc)
            print("On vide redo")
        self.redoStack = []

        if not self.undoStack: #If empty
            self.callFunc(self.nonEmptyUndoFunc)
        self.undoStack.append((copy.deepcopy(graph), actionName))

    def undo(self, currentGraph: ClassGraph):
        if not self.redoStack:
            self.callFunc(self.nonEmptyRedoFunc)
        self.redoStack.append((currentGraph, "Undo"))

        graph = self.undoStack.pop()[0]
        if not self.undoStack:
            self.callFunc(self.emptyUndoFunc)
        return graph

    def redo(self, currentGraph: ClassGraph):
        if not self.undoStack: #If empty
            self.callFunc(self.nonEmptyUndoFunc)
        self.undoStack.append((currentGraph, "Redo"))

        graph = self.redoStack.pop()[0]
        if not self.redoStack:
            self.callFunc(self.emptyRedoFunc)

        return graph

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

