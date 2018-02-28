from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from PyQt4 import QtGui
from matplotlib.pyplot import cm


class Gene2DCanvas(FigureCanvas):

    def __init__(self,modGene,vwGene):
        self.modGene = modGene
        self.vwGene = vwGene
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)
        self.fig.patch.set_visible(False)
        self.axes.axis('off')


        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateView(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)


        #fig, ax = plt.subplots()
        self.axes.scatter(*self.modGene.TXf.T, c=[0.8,0.8,0.8,1],linewidths=0.0)
        self.axes.scatter(*self.modGene.TXf.T[:,self.modGene.currGeneExpPlt],c='r',linewidths=0.0)


        minx=np.min(self.modGene.TXf.T[0,:])
        maxx=np.max(self.modGene.TXf.T[0,:])
        miny=np.min(self.modGene.TXf.T[1,:])
        maxy=np.max(self.modGene.TXf.T[1,:])
        diffy=maxy-miny
        diffx=maxx-minx

        self.axes.set_xlim((minx - 0.05 * diffx, maxx + 0.05 * diffx))
        self.axes.set_ylim((miny-0.05*diffy,maxy+0.05*diffy))

        #fig.show()
        self.fig.canvas.draw()
