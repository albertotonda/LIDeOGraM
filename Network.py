# -*- coding: utf-8
import networkx as nx
import numpy as np
import copy
import nx_pylab_angle as nxa

class Network:
    def __init__(self, modApp, vwApp, ax, fig):
        self.modApp = modApp
        self.vwApp = vwApp
        self.axes = ax
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        self.fig = fig

    def draw_nodes_labels(self, hover=None):
        hEdgeColor = self.modApp.edgeColor.copy()
        hEdge = self.modApp.edgelist_inOrder.copy()
        hBold = [False] * len(hEdge)
        hNodeColor = self.modApp.nodeColor.copy()
        greyLab = {}
        greyLabPos = {}
        blackLab = {}
        blackLabPos = {}
        greyColor = [0.85, 0.85, 0.85, 1.0]
        greyNode = (0.8, 0.8, 0.8)
        redNode = (0.9, 0, 0)
        redLab = {}
        redLabPos = {}
        lineWidthsNode = []
        linewidthsColors = []

        for v in self.modApp.dataset.varnames.tolist():
            if (v == self.modApp.lastNodeClicked):
                lineWidthsNode.append(5.0)
                linewidthsColors.append((0, 0, 0))
            else:
                lineWidthsNode.append(0.0)
                linewidthsColors.append((0, 0, 0))

            if (v in self.modApp.nodesWithNoEquations):
                hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = redNode

        if (hover != None):
            hBold = [True] * len(hEdge)
            for i in range(len(self.modApp.edgelist_inOrder)):
                if (self.modApp.edgelist_inOrder[i][0] != hover and self.modApp.edgelist_inOrder[i][1] != hover
                    and self.modApp.edgelist_inOrder[i][0] != self.modApp.lastNodeClicked and
                            self.modApp.edgelist_inOrder[i][1] != self.modApp.lastNodeClicked):
                    hEdgeColor[i] = greyColor
                    hBold[i] = False

            for v in self.modApp.dataset.varnames.tolist():
                if (not (hover, v) in self.modApp.edgelist_inOrder and not (v,hover) in self.modApp.edgelist_inOrder and hover != v and v != self.modApp.lastNodeClicked and not v in self.modApp.nodesWithNoEquations):
                    hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = greyNode
                    greyLab[v] = v
                    greyLabPos[v] = self.modApp.lpos[v]
                elif (not v in self.modApp.nodesWithNoEquations):
                    blackLab[v] = v
                    blackLabPos[v] = self.modApp.lpos[v]
                else:
                    redLab[v] = v
                    redLabPos[v] = self.modApp.lpos[v]


        else:
            blackLab = self.modApp.labels.copy()
            blackLabPos = self.modApp.lpos.copy()
            for v in self.modApp.nodesWithNoEquations:
                del blackLab[v]
                del blackLabPos[v]
                redLab[v] = v
                redLabPos[v] = self.modApp.lpos[v]

        for i in range(len(self.modApp.edgelist_inOrder)):
            if (self.modApp.edgelist_inOrder[i] in self.modApp.invisibleTup or self.modApp.edgelist_inOrder[
                i] in self.modApp.forbidden_edge):
                hEdgeColor[i] = greyColor
        for v in self.modApp.forbiddenNodes:
            try:
                hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = greyNode
            except:
                pass
            try:  # If the node is black, change it to grey, nothing to do otherwise
                blackLab.pop(v)
                blackLabPos.pop(v)
                greyLab[v] = v
                greyLabPos[v] = self.modApp.lpos[v]
            except:
                pass  # Not a test ! Do not remove the try except pass !


        nxa.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                                node_color=hNodeColor,
                                with_labels=False, edgelist=hEdge, edge_color=hEdgeColor, linewidths=lineWidthsNode,
                                linewidthsColors=linewidthsColors, ax=self.axes)

        if(self.modApp.ColorMode == 'Pearson'):
            nxa.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                                    node_color=self.modApp.nodeColor, with_labels=False, edgelist=hEdge,
                                    edge_color=hEdgeColor, edge_bold=hBold, ax=self.axes)
        else:
            nxa.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                                    node_color=self.modApp.nodeColor, with_labels=False, edgelist=hEdge,
                                    edge_color=hEdgeColor, edge_bold=hBold, ax=self.axes)

        nxa.draw_networkx_labels_angle(self.modApp.G, greyLabPos, greyLab, ax=self.axes, font_color=greyNode,
                                       rotate=45)
        nxa.draw_networkx_labels_angle(self.modApp.G, redLabPos, redLab, ax=self.axes, font_color=redNode,
                                       rotate=45)
        nxa.draw_networkx_labels_angle(self.modApp.G, blackLabPos, blackLab, ax=self.axes, rotate=45)


    def draw_global_nodes_labels(self, hover=None):
        hEdgeColor = self.modApp.global_Edge_Color.copy()
        hEdge = self.modApp.edgelist_inOrder.copy()
        hBold = [False] * len(hEdgeColor)
        hNodeColor = self.modApp.nodeColor.copy()
        greyLab = {}
        greyLabPos = {}
        blackLab = {}
        blackLabPos = {}
        greyFpos = {}
        blackFpos = {}
        greyFLab = {}
        blackFLab = {}

        greyColor = [0.85, 0.85, 0.85, 1.0]
        greyNode = (0.8, 0.8, 0.8)

        if (hover != None):
            hBold = [True] * len(hEdge)
            for i in range(len(self.modApp.edgelist_inOrder)):
                if (self.modApp.edgelist_inOrder[i][0] != hover and self.modApp.edgelist_inOrder[i][1] != hover):
                    hEdgeColor[i] = greyColor
                    hBold[i] = False

            for v in self.modApp.dataset.varnames.tolist():
                if (not (hover, v) in self.modApp.edgelist_inOrder and not (
                        v, hover) in self.modApp.edgelist_inOrder and hover != v):
                    hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = greyNode
                    greyLab[v] = v
                    greyLabPos[v] = self.modApp.lpos[v]
                    if (not v in self.modApp.varsIn):
                        #TODO possibly un elif
                        greyFLab[v] = self.modApp.globErrLab[v]
                        greyFpos[v] = self.modApp.fpos[v]
                else:
                    blackLab[v] = v
                    blackLabPos[v] = self.modApp.lpos[v]
                    if (not v in self.modApp.varsIn):
                        blackFLab[v] = self.modApp.globErrLab[v]
                        blackFpos[v] = self.modApp.fpos[v]

        else:
            for v in self.modApp.dataset.varnames.tolist():
                blackLab[v] = v
                blackLabPos[v] = self.modApp.lpos[v]
                if (not v in self.modApp.varsIn):
                    blackFLab[v] = self.modApp.globErrLab[v]
                    blackFpos[v] = self.modApp.fpos[v]
                    # for v in parOffNodes:
                    #    hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = (0, 0, 1)

        allposx = []
        allposy = []
        for (x, y) in self.modApp.pos.values():
            allposx.append(x)
            allposy.append(y)
        minx = np.min(allposx)
        miny = np.min(allposy)

        blackFpos['GlobErr'] = (minx, miny)

        blackFLab['GlobErr'] = ' Global fitness: ' + "{0:.3f}".format(self.modApp.GlobErr)


        # nx.draw_networkx_labels(self.modApp.G,labpos,lab,ax=self.axes)
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


        # nx.draw_networkx(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
        #                      node_color=hNodeColor,
        #                      with_labels=False, edgelist=hEdge,edge_color=hEdgeColor,ax=self.axes)

        nx.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                               node_color=hNodeColor,
                               with_labels=False, edgelist=hEdge, edge_color=hEdgeColor, ax=self.axes)
        nxa.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                                node_color=self.modApp.nodeColor, with_labels=False, edgelist=hEdge,
                                edge_color=hEdgeColor, edge_bold=hBold, ax=self.axes)

        if (hover != None):
            nxa.draw_networkx_labels_angle(self.modApp.G, greyLabPos, greyLab, ax=self.axes, font_color=(0.8, 0.8, 0.8),
                                           rotate=45)
            nxa.draw_networkx_labels_angle(self.modApp.G, blackLabPos, blackLab, ax=self.axes, rotate=45)
            nx.draw_networkx_labels(self.modApp.G, greyFpos, greyFLab, font_color=(0.8, 0.8, 0.8), ax=self.axes)
            nx.draw_networkx_labels(self.modApp.G, blackFpos, blackFLab, ax=self.axes)
        else:
            nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)
            nx.draw_networkx_labels(self.modApp.G, greyFpos, greyFLab, font_color=(0.8, 0.8, 0.8), ax=self.axes)
            nx.draw_networkx_labels(self.modApp.G, blackFpos, blackFLab, ax=self.axes)

        self.vwApp.networkGUI.fig.canvas.draw()

    def draw_global_nodes_labels2(self, hover=None):
        # testpos=self.modApp.pos.copy()
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

                    # for v in parOffNodes:
                    #    hNodeColor[self.modApp.dataset.varnames.tolist().index(v)] = (0, 0, 1)

        nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)
        # nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.fitCmplxlPos, self.modApp.labels, ax=self.axes, rotate=45)

        allposx = []
        allposy = []
        for (x, y) in self.modApp.pos.values():
            allposx.append(x)
            allposy.append(y)
        minx = np.min(allposx)
        miny = np.min(allposy)

        self.modApp.fpos['GlobErr'] = (minx, miny)
        # self.modApp.fitCmplxlfPos['GlobErr'] = (minx, miny)

        self.modApp.globErrLab['GlobErr'] = ' Global fitness: ' + "{0:.3f}".format(self.modApp.GlobErr)
        # self.modApp.fpos
        nx.draw_networkx_labels(self.modApp.G, self.modApp.fpos, self.modApp.globErrLab, ax=self.axes)
        # nx.draw_networkx_labels(self.modApp.G, self.modApp.fitCmplxlfPos, self.modApp.globErrLab, ax=self.axes)

        labpos = {}

        # nx.draw_networkx_labels(self.modApp.G,labpos,lab,ax=self.axes)
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

        # nx.draw_networkx(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
        #                       node_color=hNodeColor,
        #                       with_labels=False, edgelist=hEdge,edge_color=hEdgeColor,ax=self.axes)

        nx.draw_networkx(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
                         node_color=hNodeColor,
                         with_labels=False, edgelist=hEdge, edge_color=hEdgeColor, ax=self.axes)

        self.vwApp.networkGUI.fig.canvas.draw()

        # def updateNodes(self):
        #    nx.draw_networkx_nodes(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
        #                           node_color=self.modApp.nodeColor,
        #                           with_labels=False, edgelist=self.modApp.edgelist_inOrder, edge_color=self.modApp.edgeColor,
        #                           ax=self.axes)
        # self.vwApp.networkGUI.fig.canvas.draw()
        # def updateLabels(self):
        #    nxa.draw_networkx_labels_angle(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes, rotate=45)
        # nx.draw_networkx_labels(self.modApp.G, self.modApp.lpos, self.modApp.labels, ax=self.axes)

        # self.vwApp.networkGUI.fig.canvas.draw()

        # def drawEdges(self):
        #    nxa.draw_networkx_edges(self.modApp.G, self.modApp.pos, nodelist=self.modApp.dataset.varnames.tolist(),
        #                           node_color=self.modApp.nodeColor, with_labels=False,
        #                           edgelist=self.modApp.edgelist_inOrder,
        #                           edge_color=self.modApp.edgeColor,edge_bold=self.modApp.edgeBold, ax=self.axes)
        # self.vwApp.networkGUI.fig.canvas.draw()

    def updateView(self, hover=None):
        self.axes.clear()
        self.axes.hold(True)
        if (self.modApp.globalModelView):
            self.draw_global_nodes_labels(hover)
        else:
            self.draw_nodes_labels(hover)
        self.vwApp.networkGUI.fig.canvas.draw()
        self.axes.hold(True)
        self.fig.subplots_adjust(left=0.00001, bottom=0.00001, right=0.99999, top=0.99999)
