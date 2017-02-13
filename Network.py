#-*- coding: utf-8
import networkx as nx
import numpy as np
import copy
import nx_pylab_angle as nxa

class Network:
    def __init__(self,modApp, vwApp, ax):
        self.modApp=modApp
        self.vwApp = vwApp
        self.axes = ax
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)



    def draw_nodes_labels(self):
        nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)
        #nx.draw_networkx_labels(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes)

        nx.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(), node_color=self.modApp.nodeColor,
                               with_labels=False,edgelist=self.modApp.edgelist_inOrder,edge_color=self.modApp.edgeColor, ax=self.axes)
        nxa.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                           node_color=self.modApp.nodeColor, with_labels=False, edgelist=self.modApp.edgelist_inOrder,
                           edge_color=self.modApp.edgeColor,edge_bold=self.modApp.edgeBold, ax=self.axes)
        self.vwApp.networkGUI.fig.canvas.draw()

    def draw_global_nodes_labels(self):
        nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)

        allposx=[]
        allposy=[]
        for (x,y) in self.modApp.pos.values():
            allposx.append(x)
            allposy.append(y)
        minx=np.min(allposx)
        miny=np.min(allposy)

        self.modApp.fpos['GlobErr']=(minx,miny)

        self.modApp.globErrLab['GlobErr'] = ' Global fitness: ' + "{0:.5f}".format(self.modApp.GlobErr)
        self.modApp.fpos
        nx.draw_networkx_labels(self.modApp.G, self.modApp.fpos, self.modApp.globErrLab, ax=self.axes)

        labpos={}

        #nx.draw_networkx_labels(self.modApp.G,labpos,lab,ax=self.axes)
        # nx.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
        #                        node_color=self.modApp.nodeColor,
        #                        with_labels=False, edgelist=self.modApp.edgelist_inOrder,
        #                        #edge_color=self.modApp.edgeColor,
        #                        ax=self.axes)
        # nx.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
        #                         node_color=self.modApp.nodeColor, with_labels=False,
        #                         edgelist=self.modApp.edgelist_inOrder,
        #                         edge_color=self.modApp.global_Edge_Color,
        #                         #edge_bold=self.modApp.edgeBold,
        #                         ax=self.axes)

        nx.draw_networkx(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                               node_color=self.modApp.nodeColor,
                               with_labels=False, edgelist=self.modApp.edgelist_inOrder,edge_color=self.modApp.global_Edge_Color,ax=self.axes)

        self.vwApp.networkGUI.fig.canvas.draw()

    def updateNodes(self):
        nx.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                               node_color=self.modApp.nodeColor,
                               with_labels=False, edgelist=self.modApp.edgelist_inOrder, edge_color=self.modApp.edgeColor,
                               ax=self.axes)
        #self.vwApp.networkGUI.fig.canvas.draw()
    def updateLabels(self):
        nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)
        #nx.draw_networkx_labels(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes)

        #self.vwApp.networkGUI.fig.canvas.draw()

    def drawEdges(self):
        nxa.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                               node_color=self.modApp.nodeColor, with_labels=False,
                               edgelist=self.modApp.edgelist_inOrder,
                               edge_color=self.modApp.edgeColor,edge_bold=self.modApp.edgeBold, ax=self.axes)
        #self.vwApp.networkGUI.fig.canvas.draw()

    def updateView(self):

            #self.modApp.lpos[p][1] +=0.04
        self.axes.clear()
        #self.axes.plot([0,1.07],[(self.modApp.pos['REGULFUN'] + self.modApp.pos['C140'])/2,(self.modApp.pos['REGULFUN'] + self.modApp.pos['C140'])/2],'-')
        self.axes.hold(True)
        #self.axes.plot([0, 1.07], [(self.modApp.pos['Age'] + self.modApp.pos['AMACBIOSYNTH']) / 2,(self.modApp.pos['Age'] + self.modApp.pos['AMACBIOSYNTH']) / 2],'-')
        #self.axes.plot([0, 1.07], [(self.modApp.pos['C220'] + self.modApp.pos['UFCcentri']) / 2,(self.modApp.pos['C220'] + self.modApp.pos['UFCcentri']) / 2],'-')
        if(self.modApp.globalModelView):
            self.draw_global_nodes_labels()
        else:
            self.draw_nodes_labels()

        #self.vwApp.networkGUI.fig.canvas.draw()
        #self.axes.clear()
        #self.axes.hold(True)
        #self.draw_nodes_labels()
        #nx.draw_networkx_edges(self.modApp.G, self.modApp.pos, edgelist=self.edgelist_inOrder,edge_color=self.modApp.edgeColor, ax=self.axes)

