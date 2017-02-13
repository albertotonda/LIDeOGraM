#-*- coding: utf-8
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import fitness
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







    #TODO : Afficher un plot Initial intéressant
    def compute_initial_figure(self):
        plt.axis('on')



    def updateView(self):
        if self.modApp.clicked_line==-1:
            self.fig.clear()
            self.fig.canvas.draw()
            return

        eq = self.modApp.data[self.modApp.clicked_line][2]


        datafrom=self.modApp.curr_tabl[self.modApp.clicked_line][3]

        x = []
        y = []

        if datafrom=='1':

            #currdataset = self.modApp.dataset

            for n, i in enumerate(self.cell_pop):
                x.append(n)
                y.append(parse_expr(eq.replace("^","**"),i))
            v =  "fitness/params_ce_po.csv"

        else:

            #currdataset = self.modApp.dataset

            #for n, i in enumerate(self.modApp.dataset):
            #    x.append(n)
            #    y.append(parse_expr(eq.replace("^","**"), i))
            #v = "fitness/params_mo_ce.csv"

            for i in range(self.modApp.dataset.nbExp):
                x.append(i)
                y.append(parse_expr(eq.replace("^","**"),self.modApp.dataset.getAllVarsforExp(i)))

        #num_exp=range(len(currdataset[2:,currdataset[0,:]==self.modApp.lastNodeClicked].astype('float64').flatten()))
        num_exp = range(self.modApp.dataset.nbExp)

        if self.modApp.showGlobalModel:
            ft = fitness.Individual(self.modApp)
            x = num_exp
            z = [ft.process(i,self.modApp.selectedEq)[self.modApp.lastNodeClicked] for i in x]
            z = np.asarray(z)


        #val_node_exp=currdataset[2:,currdataset[0,:]==self.modApp.lastNodeClicked].astype('float64').flatten()
        val_node_exp=self.modApp.dataset.getAllExpsforVar(self.modApp.lastNodeClicked)
        self.fig.clear()
        currax=self.fig.add_subplot(111)
        y = np.asarray(y)
        if not self.modApp.showGlobalModel:
            mx = np.maximum(val_node_exp.max(), np.float64(y.max()))
            mn = np.minimum(val_node_exp.min(), np.float64(y.min()))
            inter = (val_node_exp.max()- val_node_exp.min())*0.1
            currax.plot(val_node_exp, y, 'ro', label="Local Model")
            currax.plot([0, mx + inter], [0, mx + inter], 'r-')
            currax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=1, borderaxespad=0., numpoints= 1)
            plt.xlabel("Measured --->")
            plt.ylabel("Predicted --->")
            plt.suptitle('Measured    VS    Predicted    Plot', fontsize= 11, y= 1.00111)
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
                currax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, borderaxespad=0., numpoints= 1, width= 29)
                plt.xlabel("Measured --->")
                plt.ylabel("Predicted --->")
                plt.suptitle('Measured    VS    Predicted    Plot', fontsize= 11, y= 1.00111)
                plt.xlim(mn - inter, mx + inter)
                plt.ylim(mn - inter, mx + inter)
            else:
                mx = np.maximum(val_node_exp.max(), np.float64(z.max()))
                mn = np.minimum(val_node_exp.min(), np.float64(z.min()))
                inter = (val_node_exp.max() - val_node_exp.min()) * 0.1
                currax.plot(val_node_exp, y, 'ro', label="Local Model")
                currax.plot(val_node_exp, z, 'bo', label="Global Model")
                currax.plot([0, mx + inter], [0, mx + inter], 'r-')
                currax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, borderaxespad=0., numpoints= 1)
                plt.xlabel("Measured --->")
                plt.ylabel("Predicted --->")
                plt.suptitle('Measured    VS    Predicted    Plot', fontsize= 11, y= 1.00111)
                plt.xlim(mn - inter, mx + inter)
                plt.ylim(mn - inter, mx + inter)
        self.fig.canvas.draw()



