#-*- coding: utf-8
import networkx as nx
import numpy as np

class Network:
    def __init__(self,modApp, vwApp, ax):
        self.modApp=modApp
        self.vwApp = vwApp
        self.axes = ax
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)


    def draw_nodes_labels(self):
        nx.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.varnames.tolist(), node_color=self.modApp.nodeColor, with_labels=False, ax=self.axes)
        nx.draw_networkx_labels(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes)

    def updateView(self):
        self.modApp.G.clear()
        self.draw_nodes_labels()
        self.edgelist_inOrder = []
        self.modApp.edgeColor  =  []
        adjThreshold=self.modApp.adjThresholdVal
        comprFitCmplx=self.modApp.comprFitCmplxVal

        for i in range(len(self.modApp.pareto)):
            for j in range(len(self.modApp.pareto[i])):
                lIdxColPareto = self.modApp.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    lIdxColPareto[:, 0] = (lIdxColPareto[:, 0] - self.modApp.cmplxMin) / (
                        self.modApp.cmplxMax - self.modApp.cmplxMin)  # Normalisation de la complexité
                    dist_lIdxColPareto = np.sqrt(np.power(np.cos(comprFitCmplx * (np.pi / 2)) * lIdxColPareto[:, 0], 2) +
                                                 np.power(np.sin(comprFitCmplx * (np.pi / 2)) * lIdxColPareto[:, 1], 2))
                    dist_lIdxColPareto_idxMin = np.argmin(
                        dist_lIdxColPareto)  # Indice dans dist_lIdxColPareto correspondant au meilleur compromi
                    dist_lIdxColPareto_valMin = dist_lIdxColPareto[dist_lIdxColPareto_idxMin]  # Distance meilleur compromi
                    if self.modApp.nbeq[i] == np.float64(0.0) : continue
                    r = self.modApp.adj_simple[i, j] / self.modApp.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                    if (r > adjThreshold):
                        self.modApp.G.add_edge(self.modApp.varnames[j], self.modApp.varnames[i], adjsimple=self.modApp.adj_simple[i, j], adjfit=
                        self.modApp.adj_fit[i, j], adjcmplx=self.modApp.adj_cmplx[i, j], adjcontr=self.modApp.adj_contr[i, j])
                        self.edgelist_inOrder.append((self.modApp.varnames[j], self.modApp.varnames[i]))
                        self.modApp.edgeColor.append((dist_lIdxColPareto_valMin + (1 - dist_lIdxColPareto_valMin) * (1 - r)
                                               , (1 - dist_lIdxColPareto_valMin) + dist_lIdxColPareto_valMin * (1 - r)
                                               , 1 - r))

                    n1= self.modApp.varnames[i]+' - '+self.modApp.varnames[j]
                    n2= self.modApp.varnames[j]+' - '+self.modApp.varnames[i]
                    allItems = [self.vwApp.scrolledList.itemText(i) for i in range(self.vwApp.scrolledList.count())]
                    if n1 in allItems or n2 in allItems:
                        try:
                            index = self.edgelist_inOrder.index((self.modApp.varnames[i],self.modApp.varnames[j]))
                        except:
                            index = self.edgelist_inOrder.index((self.modApp.varnames[j],self.modApp.varnames[i]))
                        self.edgelist_inOrder.pop(index)
                        self.modApp.edgeColor.pop(index)

        nx.draw_networkx_edges(self.modApp.G, self.modApp.pos, edgelist=self.edgelist_inOrder,edge_color=self.modApp.edgeColor, ax=self.axes)


