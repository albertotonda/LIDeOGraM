import networkx as nx
import json
from classes.ClassNode import ClassNode

class ClassGraph(nx.DiGraph):
    def __init__(self, unboundNode = None):
        if not unboundNode:
            unboundNode = []
        self.unboundNode = unboundNode
        nx.DiGraph.__init__(self)

    @staticmethod
    def readJson(filePath : str):
        cg = ClassGraph()
        file = open(filePath, "r")
        dicoG = json.loads(file.read())
        listeNode = dict()
        listeEdge = []
        selectedNode = None
        for node in dicoG["node"]:
            listeNode[node["name"]] = ClassNode(node["name"], node["nodeList"], pos=node["pos"], color=node["color"], lineWidth=0)    #node["lineWidth"])
            print(node["name"], node["pos"])
        for edge in dicoG["edge"]:
            listeEdge.append((
                listeNode[edge[0]]
                , listeNode[edge[1]]
                ))
        cg.unboundNode = dicoG["unbound"]
        cg.add_nodes_from(listeNode.values())
        cg.add_edges_from(listeEdge)

        file.close()
        return cg

    def remove_node(self, node: ClassNode,  beforeChange=None):
        if beforeChange:
            beforeChange("- Remove class : "+node.name, color=(255, 200, 200))
        self.unboundNode.extend(node.nodeList)
        self.unboundNode.sort()
        super(ClassGraph, self).remove_node(node)

    def toJSON(self, path: str="test2"):
        file = open(path, "w")
        saveGraph = dict()

        print("save")

        saveGraph["edge"] = []
        for ed in self.edges():
            saveGraph["edge"].append((str(ed[0]), str(ed[1])))
        saveGraph["node"] = self.nodes()
        saveGraph["unbound"] = self.unboundNode

        file.write(json.dumps(saveGraph, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        file.close()


