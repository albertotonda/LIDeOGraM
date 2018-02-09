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
        self.fig =  plt.figure()
        self.axes =  self.fig.add_subplot(111)
        self.axes.hold(False)
        self.fig.patch.set_visible(False)
        self.axes.axis('off')
        self.compute_initial_figure()


        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def get_ax_size(self,fig,ax):
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height
        width *= fig.dpi
        height *= fig.dpi
        return width, height



    #TODO : Afficher un plot Initial intéressant
    def compute_initial_figure(self):
        plt.axis('on')



    def updateView(self):
        if self.modApp.clicked_line==-1:
            self.fig.clear()
            self.fig.canvas.draw()
            return

        #datafrom = None


        eq = self.modApp.data[self.modApp.clicked_line][2]



        datafrom=self.modApp.curr_tabl[self.modApp.clicked_line][3]

        x = []
        y = []

        if datafrom=='1':
            for n, i in enumerate(self.cell_pop):
                x.append(n)
                y.append(parse_expr(eq.replace("^","**"),i))

        else:
            for i in range(self.modApp.dataset.nbExp):
                x.append(i)
                y.append(parse_expr(eq.replace("^","**"),self.modApp.dataset.getAllVarsforExp(i)))

        num_exp = range(self.modApp.dataset.nbExp)

        if self.modApp.globalModelView:
            ft = fitness.Individual(self.modApp)
            x = num_exp
            z = [ft.process(i,self.modApp.selectedEq)[self.modApp.lastNodeClicked] for i in x]
            z = np.asarray(z)

        val_node_exp=self.modApp.dataset.getAllExpsforVar(self.modApp.lastNodeClicked)
        self.fig.clear()
        currax=self.fig.add_subplot(111)

        y = np.asarray(y)
        if not self.modApp.globalModelView:
            mx = np.maximum(val_node_exp.max(), np.float64(y.max()))
            mn = np.minimum(val_node_exp.min(), np.float64(y.min()))
            inter = (val_node_exp.max()- val_node_exp.min())*0.1
            currax.plot(val_node_exp, y, 'ro', label="Local Model")
            #currax.plot(val_node_exp[[0,1,8]], y[[0,1,8]], 'ro', label="Local Model")
            #currax.plot(val_node_exp[[2, 3, 9]], y[[2, 3, 9]], 'bo', label="Local Model")
            #currax.plot(val_node_exp[[4, 5, 10]], y[[4, 5, 10]], 'yo', label="Local Model")
            #currax.plot(val_node_exp[[6, 7, 11]], y[[6, 7, 11]], 'go', label="Local Model")
            currax.plot([mn-inter, mx + inter], [mn-inter, mx + inter], 'r-')
            currax.set_xlim(mn - inter, mx + inter)
            currax.set_ylim(mn - inter, mx + inter)

            sizeYax = self.get_ax_size(self.fig, currax)[1]
            sizeYscale = currax.get_ylim()[1] - currax.get_ylim()[0]
            sizeUncertaintyPix=self.modApp.dataset.variablesUncertainty[self.modApp.lastNodeClicked]
            linewidthUncertainty = sizeUncertaintyPix / sizeYscale * sizeYax * np.sqrt(2)
            currax.plot([mn-inter, mx + inter], [mn-inter, mx + inter], 'r-', alpha=0.5, linewidth=linewidthUncertainty)

            currax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=4, borderaxespad=0., numpoints= 1)
            currax.set_xlabel("Measured --->")
            currax.set_ylabel("Predicted --->")
            plt.suptitle('Measured    VS    Predicted    Plot', fontsize= 11, y= 1.00111)


        else:
            if  np.float64(y.max()) >  np.float64(z.max()) and  np.float64(y.min()) <  np.float64(y.min()):
                mx = np.maximum(val_node_exp.max(), np.float64(y.max()))
                mn = np.minimum(val_node_exp.min(), np.float64(y.min()))
                inter = (val_node_exp.max() - val_node_exp.min()) * 0.1
                #currax.plot(val_node_exp, y, 'ro', label="Local Model")
                currax.plot(val_node_exp[[0, 1, 8]], y[[0, 1, 8]], 'ro', label="22C 0h")
                currax.plot(val_node_exp[[2, 3, 9]], y[[2, 3, 9]], 'ro', label="22C 6h")
                currax.plot(val_node_exp[[4, 5, 10]], y[[4, 5, 10]], 'ro', label="30C 0h")
                currax.plot(val_node_exp[[6, 7, 11]], y[[6, 7, 11]], 'ro', label="30C 6h")
                currax.plot(val_node_exp, z, 'bo', label="Global Model")
                currax.plot([mn-inter, mx + inter], [mn-inter, mx + inter], 'r-')
                currax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, borderaxespad=0., numpoints= 1, width= 29)
                currax.set_xlabel("Measured --->")
                currax.set_ylabel("Predicted --->")
                plt.suptitle('Measured    VS    Predicted    Plot', fontsize= 11, y= 1.00111)
                currax.set_xlim(mn - inter, mx + inter)
                currax.set_ylim(mn - inter, mx + inter)

                sizeYax = self.get_ax_size(self.fig, currax)[1]
                sizeYscale = currax.get_ylim()[1] - currax.get_ylim()[0]
                sizeUncertaintyPix=self.modApp.dataset.variablesUncertainty[self.modApp.lastNodeClicked]
                linewidthUncertainty = sizeUncertaintyPix / sizeYscale * sizeYax * np.sqrt(2)
                currax.plot([mn-inter, mx + inter], [mn-inter, mx + inter], 'r-', alpha=0.5, linewidth=linewidthUncertainty)
            else:
                mx = np.maximum(val_node_exp.max(), np.float64(z.max()))
                mn = np.minimum(val_node_exp.min(), np.float64(z.min()))
                inter = (val_node_exp.max() - val_node_exp.min()) * 0.1
                #currax.plot(val_node_exp, y, 'ro', label="Local Model")
                currax.plot(val_node_exp[[0, 1, 8]], y[[0, 1, 8]], 'ro', label="22C 0h")
                currax.plot(val_node_exp[[2, 3, 9]], y[[2, 3, 9]], 'ro', label="22C 6h")
                currax.plot(val_node_exp[[4, 5, 10]], y[[4, 5, 10]], 'ro', label="30C 0h")
                currax.plot(val_node_exp[[6, 7, 11]], y[[6, 7, 11]], 'ro', label="30C 6h")
                currax.plot(val_node_exp, z, 'bo', label="Global Model")
                currax.plot([mn-inter, mx + inter], [mn-inter, mx + inter], 'r-')
                currax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, borderaxespad=0., numpoints= 1)
                currax.set_xlabel("Measured --->")
                currax.set_ylabel("Predicted --->")
                plt.suptitle('Measured    VS    Predicted    Plot', fontsize= 11, y= 1.00111)
                currax.set_xlim(mn - inter, mx + inter)
                currax.set_ylim(mn - inter, mx + inter)

                sizeYax = self.get_ax_size(self.fig, currax)[1]
                sizeYscale = currax.get_ylim()[1] - currax.get_ylim()[0]
                sizeUncertaintyPix = self.modApp.dataset.variablesUncertainty[self.modApp.lastNodeClicked]
                linewidthUncertainty = sizeUncertaintyPix / sizeYscale * sizeYax * np.sqrt(2)
                currax.plot([mn-inter, mx + inter], [mn-inter, mx + inter], 'r-', alpha=0.5, linewidth=linewidthUncertainty)
        self.fig.canvas.draw()

