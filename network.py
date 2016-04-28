import copy
import networkx as nx
import numpy as np

class Network:
    def __init__(self,modApp, G,ax , fig, pos):
        self.modApp=modApp
        self.edgeColor = []
        self.cmplxMin = np.amin(self.modApp.equacolPOf[:, 0])
        self.cmplxMax = np.amax(self.modApp.equacolPOf[:, 0])
        self.nodeColor = []
        self.nodeWeight = []
        self.pareto = []
        self.G = G
        self.fig = fig
        self.pos = pos
        self.lpos = copy.deepcopy(pos)
        for p in self.lpos:  # raise text positions
            self.lpos[p][1] += 0.04

        self.axes = ax
        self.labels = {}

        for v in self.modApp.varnames:
            G.add_node(v)
            self.labels[v] = v

        for i in range(len(self.modApp.adj_simple)):
            self.pareto.append([])
            for j in range(len(self.modApp.adj_simple[i])):
                self.pareto[i - 1].append(self.modApp.equacolPOf[np.ix_(
                    np.logical_and(self.modApp.equacolPOs[:, 2] == self.modApp.varnames[i],
                                   self.modApp.equacolPOs[:, 3] == self.modApp.varnames[j])), 0:2][0])

        for i in range(len(self.modApp.varnames)):
            if ((len(self.modApp.varnames) - np.sum(self.modApp.adj_contr, axis=0)[i]) != 0):
                self.nodeWeight.append(
                    np.sum(self.modApp.adj_simple, axis=0)[i] / (len(self.modApp.varnames) - np.sum(self.modApp.adj_contr, axis=0)[i]))
            else:
                self.nodeWeight.append(0)
        for i in range(len(self.modApp.varnames)):
            self.nodeColor.append((0.5, 0.5 + 0.5 * self.nodeWeight[i] / np.amax(self.nodeWeight), 0.5))

        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

    def draw_nodes_labels(self):
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.modApp.varnames.tolist(), node_color=self.nodeColor, with_labels=False, ax=self.axes)
        nx.draw_networkx_labels(self.G, self.lpos, self.labels, ax=self.axes)


    def higlight(self, new_node: str, old_node: str):
        #nx.draw_networkx_nodes(self.G, self.pos, nodelist=self.modApp.varnames.tolist(), node_color=self.nodeColor,
        #                       with_labels=False, ax=self.fig.axes)
        pass

    def update(self, ts: float, ds: float):
        self.G.clear()
        self.draw_nodes_labels()
        edgelist_inOrder = []
        self.edgeColor = []

        for i in range(len(self.pareto)):
            for j in range(len(self.pareto[i])):
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    lIdxColPareto[:, 0] = (lIdxColPareto[:, 0] - self.cmplxMin) / (
                        self.cmplxMax - self.cmplxMin)  # Normalisation de la complexité
                    dist_lIdxColPareto = np.sqrt(np.power(np.cos(ds * (np.pi / 2)) * lIdxColPareto[:, 0], 2) +
                                                 np.power(np.sin(ds * (np.pi / 2)) * lIdxColPareto[:, 1], 2))
                    dist_lIdxColPareto_idxMin = np.argmin(
                        dist_lIdxColPareto)  # Indice dans dist_lIdxColPareto correspondant au meilleur compromi
                    dist_lIdxColPareto_valMin = dist_lIdxColPareto[
                        dist_lIdxColPareto_idxMin]  # Distance meilleur compromi
                    if self.modApp.nbeq[i] == np.float64(0.0) : continue
                    r = self.modApp.adj_simple[i, j] / self.modApp.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                    if (r > ts):
                        self.G.add_edge(self.modApp.varnames[j], self.modApp.varnames[i], adjsimple=self.modApp.adj_simple[i, j], adjfit=
                        self.modApp.adj_fit[i, j], adjcmplx=self.modApp.adj_cmplx[i, j], adjcontr=self.modApp.adj_contr[i, j])
                        edgelist_inOrder.append((self.modApp.varnames[j], self.modApp.varnames[i]))
                        self.edgeColor.append((dist_lIdxColPareto_valMin + (1 - dist_lIdxColPareto_valMin) * (1 - r)
                                               , (1 - dist_lIdxColPareto_valMin) + dist_lIdxColPareto_valMin * (1 - r)
                                               , 1 - r))
        nx.draw_networkx_edges(self.G, self.pos, edgelist=edgelist_inOrder, edge_color=self.edgeColor, ax=self.axes)

