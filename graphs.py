#-*- coding: utf-8
from sys import path
path.append("fitness/")
import fitness
import networkx as nx
from RFGraph_Model import RFGraph_Model
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PyQt4 import QtGui

import network

curr_tabl=[]


class RFGraphCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, modApp, parent=None, width=5, height=4, dpi=100):
        self.modApp=modApp
        self.fig, self.axes =  plt.subplots()
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.fig.patch.set_visible(False)
        self.fig.tight_layout()
        self.axes.axis('off')
        self.axes.set_xlim([0,0.1])
        self.axes.set_ylim([0, 0.6])
        self.G=nx.DiGraph()
        self.pos=self.modApp.pos_graph()

        self.network = network.network(self.modApp,self.G, self.axes, self.fig, self.pos)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        plt.axis('off')
        self.network.update(0.5,0.5)
        self.axes.set_xlim([0, 1.07])
        self.axes.set_ylim([0, 1.07])

    def updateGraph(self,ts,ds):
        self.network.update(ts,ds)


class FitCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.fig, self.axes =  plt.subplots()
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        self.axes.axis('off')
        self.compute_initial_figure()
        self.mg = False
        self.last_clicked = None

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.computeDictionaries()

    def computeDictionaries(self):
        self.cell_pop = []
        self.mol_cell = []

        f = open("data/dataset_cell_pop.csv")
        t = f.readline()
        variables = []
        for i in t.split(','):
            variables.append(i.strip())
        for line in f:
            t = zip(variables,[float(i.strip()) for i in line.split(',')])
            self.cell_pop.append(dict(t))

        f = open("data/dataset_mol_cell.csv")
        t = f.readline()
        variables = []
        for i in t.split(','):
            variables.append(i.strip())
        for line in f:
            t = zip(variables, [float(i.strip()) for i in line.split(',')])
            self.mol_cell.append(dict(t))



    def compute_initial_figure(self):
        plt.axis('on')

    def setCurrentTable(self, table):
        self.table = table

    def fitplot(self,line):
        global curr_tabl
        eq = self.table.item(line,2).text()

        datafrom=curr_tabl[line][3]

        x = []
        y = []

        if datafrom=='1':

            currdatasetF = self.modApp.dataset_cell_popF
            currdatasetS = self.modApp.dataset_cell_popS

            for n, i in enumerate(self.cell_pop):
                x.append(n)
                y.append(parse_expr(eq.replace("^","**"),i))
            v =  "fitness/params_ce_po.csv"

        else:

            currdatasetF = self.modApp.dataset_mol_cellF
            currdatasetS = self.modApp.dataset_mol_cellS

            for n, i in enumerate(self.mol_cell):
                x.append(n)
                y.append(parse_expr(eq.replace("^","**"), i))
            v = "fitness/params_mo_ce.csv"

        num_exp=range(len(currdatasetF[1:,currdatasetS[0,:]==self.last_clicked]))

        if self.mg:
            ft = fitness.Individual(v, "fitness/ex_indiv.csv","fitness/varnames.csv" )
            x = num_exp
            z = [ft.process(i)[self.last_clicked] for i in x]


        val_node_exp=currdatasetF[1:,currdatasetS[0,:]==self.last_clicked]
        self.fig.clear()
        currax=self.fig.add_subplot(111)
        if not self.mg:
            currax.plot(num_exp, val_node_exp, 'ro')
            currax.plot(num_exp,y,'k--')
        else:
            currax.plot(num_exp, val_node_exp, 'ro')
            currax.plot(num_exp,y)
            currax.plot(num_exp,z,'k--')
        self.fig.canvas.draw()



