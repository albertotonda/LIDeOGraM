import json
import networkx as nx
import classes.ClassNode as ClassNode

class SavingGraph():
    def __init__(self, node, edge):
        self.edge = []
        for ed in edge:
            self.edge.append((str(ed[0]), str(ed[1])))
        self.node = node

    def toJSON(self):
        file = open("test", "w")
        file.write(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
        file.close()

    @staticmethod
    def readJson():
        dg = nx.DiGraph()
        file = open("test", "r")
        dicoG = json.loads(file.read())
        listNode = dict()
        listeEdge = []
        for node in dicoG["node"]:
            listNode[node["name"]] = ClassNode.ClassNode(node["name"], node["nodeList"], pos=node["pos"], color=node["color"], lineWidth=node["lineWidth"])
        for edge in dicoG["edge"]:
            listeEdge.append((
                listNode[edge[0]]
                , listNode[edge[1]]
                ))

        dg.add_nodes_from(listNode.values())
        dg.add_edges_from(listeEdge)

        file.close()
        return dg
