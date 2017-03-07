#-*- coding: utf-8
import networkx as nx
import numpy as np
import copy
import nx_pylab_angle as nxa

class Network:
    def __init__(self,modApp, vwApp, ax,fig):
        self.modApp=modApp
        self.vwApp = vwApp
        self.axes = ax
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        self.fig=fig



    def draw_nodes_labels(self,hover=None):
        #print('draw_nodes_labels')
        hEdgeColor = self.modApp.edgeColor.copy()
        hEdge=self.modApp.edgelist_inOrder.copy()
        hBold=self.modApp.edgeBold.copy()
        hNodeColor=self.modApp.nodeColor.copy()
        greyLab={}
        greyLabPos={}
        blackLab={}
        blackLabPos={}
        #sizeNode=[1] * len(self.modApp.dataset.varnames)
        #parOffNodes=[]
        if (hover != None):
            for i in range(len(self.modApp.edgelist_inOrder)):
                if(self.modApp.edgelist_inOrder[i][0] != hover and self.modApp.edgelist_inOrder[i][1] !=hover):
                    hEdgeColor[i]=(0.8,0.8,0.8)
                    #hEdge[i]=(None,None)
                    #hBold[i]=-1
            #hEdgeColor=list(filter(lambda x: x != (1,1,1), hEdgeColor))
            #hEdge=list(filter(lambda x: x != (None,None), hEdge))
            #hBold = list(filter(lambda x: x != -1, hBold))

            for v in self.modApp.dataset.varnames.tolist():
                if(not (hover,v) in self.modApp.edgelist_inOrder and not (v,hover) in self.modApp.edgelist_inOrder and hover != v):
                    hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = (0.8, 0.8, 0.8)
                    greyLab[v]=v
                    greyLabPos[v]=self.modApp.lpos[v]
                else:
                    blackLab[v]=v
                    blackLabPos[v]=self.modApp.lpos[v]

            #for (x, y) in hEdge:
            #    if (y == hover):
            #        #parOffNodes.append(x)
            #        hNodeColor[self.modApp.dataset.varnames.tolist().index(x)] = (0, 0, 1)
            #    if (x==hover):
            #        #parOffNodes.append(y)
            #        hNodeColor[self.modApp.dataset.varnames.tolist().index(y)] = (0, 1, 0)

         #nx.draw_networkx_labels(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes)

        nx.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(), node_color=hNodeColor,
                               with_labels=False,edgelist=hEdge,edge_color=hEdgeColor, ax=self.axes)
        nxa.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                           node_color=self.modApp.nodeColor, with_labels=False, edgelist=hEdge,
                          edge_color=hEdgeColor,edge_bold=hBold, ax=self.axes)
        if (hover != None):
            nxa.draw_networkx_labels_angle(self.modApp.G, greyLabPos, greyLab, ax=self.axes, font_color=(0.8, 0.8, 0.8),
                                           rotate=45)
            nxa.draw_networkx_labels_angle(self.modApp.G, blackLabPos, blackLab, ax=self.axes, rotate=45)
        else:
            nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)

        self.vwApp.networkGUI.fig.canvas.draw()

    def draw_global_nodes_labels(self,hover=None):
        #testpos=self.modApp.pos.copy()
        hEdgeColor = self.modApp.global_Edge_Color.copy()
        hEdge = self.modApp.edgelist_inOrder.copy()
        hNodeColor = self.modApp.nodeColor.copy()
        parOffNodes = []



        if (hover != None):
            for i in range(len(self.modApp.edgelist_inOrder)):
                if (self.modApp.edgelist_inOrder[i][0] != hover and self.modApp.edgelist_inOrder[i][1] != hover):
                    hEdgeColor[i] = (1, 1, 1)
                    hEdge[i] = (None, None)

            hEdgeColor = list(filter(lambda x: x != (1, 1, 1), hEdgeColor))
            hEdge = list(filter(lambda x: x != (None, None), hEdge))


            for (x, y) in hEdge:
                if (x != hover and not x in parOffNodes):
                    parOffNodes.append(x)
                    hNodeColor[self.modApp.dataset.varnames.tolist().index(x)] = (0, 0, 1)
                if (y != hover and not y in parOffNodes):
                    parOffNodes.append(y)
                    hNodeColor[self.modApp.dataset.varnames.tolist().index(y)] = (0, 1, 0)

            #for v in parOffNodes:
            #    hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = (0, 0, 1)


        nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)
        #nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.fitCmplxlPos, self.modApp.labels, ax=self.axes, rotate=45)

        allposx=[]
        allposy=[]
        for (x,y) in self.modApp.pos.values():
            allposx.append(x)
            allposy.append(y)
        minx=np.min(allposx)
        miny=np.min(allposy)

        self.modApp.fpos['GlobErr']=(minx,miny)
        #self.modApp.fitCmplxlfPos['GlobErr'] = (minx, miny)

        self.modApp.globErrLab['GlobErr'] = ' Global fitness: ' + "{0:.3f}".format(self.modApp.GlobErr)
        #self.modApp.fpos
        nx.draw_networkx_labels(self.modApp.G, self.modApp.fpos, self.modApp.globErrLab, ax=self.axes)
        #nx.draw_networkx_labels(self.modApp.G, self.modApp.fitCmplxlfPos, self.modApp.globErrLab, ax=self.axes)

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

        #nx.draw_networkx(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
        #                       node_color=hNodeColor,
        #                       with_labels=False, edgelist=hEdge,edge_color=hEdgeColor,ax=self.axes)

        nx.draw_networkx(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                              node_color=hNodeColor,
                              with_labels=False, edgelist=hEdge,edge_color=hEdgeColor,ax=self.axes)

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

    def updateView(self,hover=None):

            #self.modApp.lpos[p][1] +=0.04

        self.axes.clear()
        #self.axes.plot([0,1.07],[(self.modApp.pos['REGULFUN'] + self.modApp.pos['C140'])/2,(self.modApp.pos['REGULFUN'] + self.modApp.pos['C140'])/2],'-')
        self.axes.hold(True)
        #self.axes.plot([0, 1.07], [(self.modApp.pos['Age'] + self.modApp.pos['AMACBIOSYNTH']) / 2,(self.modApp.pos['Age'] + self.modApp.pos['AMACBIOSYNTH']) / 2],'-')
        #self.axes.plot([0, 1.07], [(self.modApp.pos['C220'] + self.modApp.pos['UFCcentri']) / 2,(self.modApp.pos['C220'] + self.modApp.pos['UFCcentri']) / 2],'-')
        if(self.modApp.globalModelView):
            self.draw_global_nodes_labels(hover)
        else:
            self.draw_nodes_labels(hover)

        #self.vwApp.networkGUI.fig.canvas.draw()
        #self.axes.clear()
        self.axes.hold(True)
        #self.draw_nodes_labels()
        #nx.draw_networkx_edges(self.modApp.G, self.modApp.pos, edgelist=self.edgelist_inOrder,edge_color=self.modApp.edgeColor, ax=self.axes)
        #self.fig.tight_layout()
        self.fig.subplots_adjust(left=0.00001, bottom=0.00001, right=0.99999, top=0.99999)