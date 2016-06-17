#-*- coding: utf-8
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#import fitness
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
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
            return

        eq = self.modApp.data[self.modApp.clicked_line][2]


        datafrom=self.modApp.curr_tabl[self.modApp.clicked_line][3]

        x = []
        y = []

        if datafrom=='1':

            currdataset = self.modApp.dataset

            for n, i in enumerate(self.cell_pop):
                x.append(n)
                y.append(parse_expr(eq.replace("^","**"),i))
            v =  "fitness/params_ce_po.csv"

        else:

            currdataset = self.modApp.dataset

            for n, i in enumerate(self.modApp.dataDict):
                x.append(n)
                y.append(parse_expr(eq.replace("^","**"), i))
            v = "fitness/params_mo_ce.csv"

        num_exp=range(len(currdataset[2:,currdataset[0,:]==self.modApp.last_clicked].astype('float64').flatten()))

        if self.modApp.showGlobalModel:
            ft = fitness.Individual(self.modApp,"fitness/ex_indiv.csv" )
            x = num_exp
            z = [ft.process(i)[self.modApp.last_clicked] for i in x]


        val_node_exp=currdataset[2:,currdataset[0,:]==self.modApp.last_clicked].astype('float64').flatten()
        self.fig.clear()
        currax=self.fig.add_subplot(111)
        if not self.modApp.showGlobalModel:
            currax.plot(num_exp, val_node_exp, 'ro')
            currax.plot(num_exp,y,'k--')
        else:
            currax.plot(num_exp, val_node_exp, 'ro')
            currax.plot(num_exp,y,'k--')
            currax.plot(num_exp,z)
        self.fig.canvas.draw()



