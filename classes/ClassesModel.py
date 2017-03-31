import networkx as nx
import classes.ClassNode as ClassNode


class ClassesModel:

    def __init__(self):
        self.G = None
        self.initGraph()

    def initGraph(self):
        self.G = nx.DiGraph()
        G=self.G
        G.add_node(ClassNode.ClassNode(0, nodeList=["a", "b", "c"], color=(0.5, 0.5, 0.9)))
        G.add_node(ClassNode.ClassNode(1, [], color=(0.9, 0.55, 0.55)))
        G.add_node(ClassNode.ClassNode(2, [], color=(0.3, 0.9, 0.9)))
        G.add_node(ClassNode.ClassNode(3, [], color=(0.7, 0.7, 0.5)))
        G.add_node(ClassNode.ClassNode(4, [], color=(0.8, 0.8, 0.2)))
        G.add_edge(self.G.nodes()[1], self.G.nodes()[2])
        G.add_edge(self.G.nodes()[2], self.G.nodes()[3])
        G.add_edge(self.G.nodes()[1], self.G.nodes()[3])
        G.add_edge(self.G.nodes()[3], self.G.nodes()[4])
        G.add_edge(self.G.nodes()[3], self.G.nodes()[0])
