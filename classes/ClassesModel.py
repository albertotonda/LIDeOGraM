import networkx as nx
from classes.ClassGraph import ClassGraph
import classes.ClassGraph as ClassGraph
import classes.ClassNode as ClassNode

class ClassesModel:

    def __init__(self):
        self.graph = None
        self.initGraph()


    def initGraph(self):
        self.graph = ClassGraph.ClassGraph()
        graph = self.graph
        """
        n0 = ClassNode.ClassNode(0, nodeList=["a", "b", "c"], color=(0.5, 0.5, 0.9))
        n1 = ClassNode.ClassNode(1, [], color=(0.9, 0.55, 0.55))
        n2 = ClassNode.ClassNode(2, [], color=(0.3, 0.9, 0.9))
        n3 = ClassNode.ClassNode(3, [], color=(0.7, 0.7, 0.5))
        n4 = ClassNode.ClassNode(4, [], color=(0.8, 0.8, 0.2))
        n5 = ClassNode.ClassNode(5, [])
        n6 = ClassNode.ClassNode(6, [])
        n7 = ClassNode.ClassNode(7, [])
        n8 = ClassNode.ClassNode(8, [])
        G.add_node(n0)
        G.add_node(n1)
        G.add_node(n2)
        G.add_node(n3)
        G.add_node(n4)
        G.add_node(n5)
        G.add_node(n6)
        G.add_node(n7)
        G.add_node(n8)
        G.add_edge(n1, n2)
        G.add_edge(n2, n3)
        G.add_edge(n1, n3)
        G.add_edge(n3, n4)
        G.add_edge(n3, n0)
        """


        condition = ClassNode.ClassNode('Condition', ['Temperature', 'Age'])
        molss = ClassNode.ClassNode('GenomicSousExpr', ['AMACBIOSYNTHsousexpr', 'BIOSYNTH_CARRIERSsousexpr', 'CELLENVELOPEsousexpr', 'CELLPROCESSESsousexpr', 'CENTRINTMETABOsousexpr', 'ENMETABOsousexpr', 'FATTYACIDMETABOsousexpr', 'Hypoprotsousexpr', 'OTHERCATsousexpr', 'PURINESsousexpr', 'REGULFUNsousexpr', 'REPLICATIONsousexpr', 'TRANSCRIPTIONsousexpr', 'TRANSLATIONsousexpr', 'TRANSPORTPROTEINSsousexpr'])
        molsur = ClassNode.ClassNode('GenomicSurExpr', ['AMACBIOSYNTHsurexpr', 'BIOSYNTH_CARRIERSsurexpr', 'CELLENVELOPEsurexpr', 'CELLPROCESSESsurexpr', 'CENTRINTMETABOsurexpr', 'ENMETABOsurexpr', 'FATTYACIDMETABOsurexpr', 'Hypoprotsurexpr', 'OTHERCATsurexpr', 'PURINESsurexpr', 'REGULFUNsurexpr', 'REPLICATIONsurexpr', 'TRANSCRIPTIONsurexpr', 'TRANSLATIONsurexpr', 'TRANSPORTPROTEINSsurexpr'])
        cell = ClassNode.ClassNode('Cellular', ["C140", "C150", "C160", "C161cis", "C170", "C180", "C181trans", "C181cis", "C19cyc", "C220"])
        cellAniso = ClassNode.ClassNode('Anisotropy', ["Anisotropie"])
        popCentri = ClassNode.ClassNode('PopulationAtCentrifugation', ["UFCcentri", "tpH07centri"])
        popCong = ClassNode.ClassNode('PopulationAtCongelation', ["UFCcong", "tpH07cong"])
        popLyo = ClassNode.ClassNode('PopulationAtLyophilisation ', ["UFClyo", "TpH07lyo"])
        popSto3 = ClassNode.ClassNode('PopulationAfter3Months', ["UFCsto3", "tpH07sto3"])

        graph.add_node(condition)
        graph.add_node(molss)
        graph.add_node(molsur)
        graph.add_node(cell)
        graph.add_node(cellAniso)
        graph.add_node(popCentri)
        graph.add_node(popCong)
        graph.add_node(popLyo)
        graph.add_node(popSto3)

        graph.add_edge(condition, molss)
        graph.add_edge(condition, molsur)
        graph.add_edge(condition, cell)
        graph.add_edge(molss, cell)
        graph.add_edge(molsur, cell)
        graph.add_edge(cell, cellAniso)
        graph.add_edge(cell, popCentri)
        graph.add_edge(cell, popCong)
        graph.add_edge(cell, popLyo)
        graph.add_edge(cell, popSto3)
        graph.add_edge(cellAniso, popCentri)
        graph.add_edge(cellAniso, popCong)
        graph.add_edge(cellAniso, popLyo)
        graph.add_edge(cellAniso, popSto3)
        graph.add_edge(condition, popCentri)
        graph.add_edge(condition, popCong)
        graph.add_edge(condition, popLyo)
        graph.add_edge(condition, popSto3)
        graph.add_edge(popCentri, popCong)
        graph.add_edge(popCentri, popLyo)
        graph.add_edge(popCentri, popSto3)
        graph.add_edge(popCong, popLyo)
        graph.add_edge(popCong, popSto3)
        graph.add_edge(popLyo, popSto3)
        #test = ClassGraph.SavingGraph(graph.nodes(), graph.edges())
        #test.toJSON()


        #self.graph = save.SavingGraph.readJson()

    def getGraph(self):
        return self.graph