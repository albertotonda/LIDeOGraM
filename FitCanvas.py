#-*- coding: utf-8
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from fitness import fitness
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
import numpy as np
from PyQt4 import QtGui


# TODO Crée la courbe correpondant à l'équation sélectionnée
class FitCanvas(FigureCanvas):
    def __init__(self,modApp):
        self.modApp=modApp
        self.fig, self.axes =  plt.subplots()
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        self.axes.axis('off')
        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.computeDictionaries()


    #TODO: Rendre plus fonctionelle en ajoutant le parametre NomDuFichier
    def computeDictionaries(self):
        #self.cell_pop ans self.mol_cell are dictionary lists.
        #Each dictionary represents the results for every variables of an experiment.
        self.cell_pop = []
        self.mol_cell = []

        cell_pop_HVdatafile = open("data/dataset_cell_pop.csv")
        cell_pop_line = cell_pop_HVdatafile.readline()  # First line are the variables name
        variables = []
        for i in cell_pop_line.split(','):
            variables.append(i.strip())
        for line in cell_pop_HVdatafile:
            cell_pop_line = zip(variables, [float(i.strip()) for i in line.split(',')])
            self.cell_pop.append(dict(cell_pop_line))

        mol_cellHVdatafile = open("data/dataset_mol_cell.csv")
        mol_cell_line = mol_cellHVdatafile.readline()  # First line are the variables name
        variables = []
        for i in mol_cell_line.split(','):
            variables.append(i.strip())
        for line in mol_cellHVdatafile:
            mol_cell_line = zip(variables, [float(i.strip()) for i in line.split(',')])
            self.mol_cell.append(dict(mol_cell_line))


    #TODO : Afficher un plot Initial intéressant
    def compute_initial_figure(self):
        plt.axis('on')



    def updateView(self):
        if self.modApp.clicked_line==-1:
            return

        eq = self.modApp.data[self.modApp.clicked_line][2]


        datafrom=self.modApp.curr_tabl[self.modApp.clicked_line][3]

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

        num_exp=range(len(currdatasetF[1:,currdatasetS[0,:]==self.modApp.last_clicked]))

        if self.modApp.showGlobalModel:
            ft = fitness.Individual(v, "fitness/ex_indiv.csv","fitness/varnames.csv" )
            x = num_exp
            z = [ft.process(i)[self.modApp.last_clicked] for i in x]
            z = np.asarray(z)


        val_node_exp=currdatasetF[1:,currdatasetS[0,:]==self.modApp.last_clicked]
        self.fig.clear()
        currax=self.fig.add_subplot(111)
        y = np.asarray(y)
        if not self.modApp.showGlobalModel:
            mx = np.maximum(val_node_exp.max(), np.float64(y.max()))
            mn = np.minimum(val_node_exp.min(), np.float64(y.min()))
            inter = (val_node_exp.max()- val_node_exp.min())*0.1
            currax.plot(val_node_exp, y, 'ro', label="Local Model")
            currax.plot([0, mx + inter], [0, mx + inter], 'r-')
            currax.legend(loc='upper left')
            plt.xlabel("Mesured")
            plt.ylabel("Predicted")
            plt.xlim(mn - inter, mx + inter)
            plt.ylim(mn - inter, mx + inter)

        else:
            if  np.float64(y.max()) >  np.float64(z.max()) and  np.float64(y.min()) <  np.float64(y.min()):
                mx = np.maximum(val_node_exp.max(), np.float64(y.max()))
                mn = np.minimum(val_node_exp.min(), np.float64(y.min()))
                inter = (val_node_exp.max() - val_node_exp.min()) * 0.1
                currax.plot(val_node_exp, y, 'ro', label="Local Model")
                currax.plot(val_node_exp, z, 'bo', label="Global Model")
                currax.plot([0, mx + inter], [0, mx + inter], 'r-')
                #currax.legend(loc= 'upper left')
                plt.xlabel("Mesured")
                plt.ylabel("Predicted")
                plt.xlim(mn - inter, mx + inter)
                plt.ylim(mn - inter, mx + inter)
            else:
                mx = np.maximum(val_node_exp.max(), np.float64(z.max()))
                mn = np.minimum(val_node_exp.min(), np.float64(z.min()))
                inter = (val_node_exp.max() - val_node_exp.min()) * 0.1
                currax.plot(val_node_exp, y, 'ro', label="Local Model")
                currax.plot(val_node_exp, z, 'bo', label="Global Model")
                currax.plot([0, mx + inter], [0, mx + inter], 'r-')
                #currax.legend(loc='upper left')
                plt.xlabel("Mesured")
                plt.ylabel("Predicted")
                plt.xlim(mn - inter, mx + inter)
                plt.ylim(mn - inter, mx + inter)
        self.fig.canvas.draw()



