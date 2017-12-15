from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as fca
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import matplotlib.pyplot as plt

class SaGUI(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.icon = QtGui.QIcon("Icone.png")
        self.setWindowTitle("Sensitivity analysis of the equation")
        self.setWindowIcon(self.icon)
        self.fig =  plt.figure()
        self.ax =  self.fig.add_subplot(111)
        self.ax.hold(False)
        self.fig.patch.set_visible(False)
        self.ax.axis('off')
        self.figCanv = FigureCanvas(self.fig)
        self.figCanv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.figCanv.updateGeometry()

        self.SAWidget = QtGui.QWidget(self)
        self.SALayout = QtGui.QVBoxLayout(self.SAWidget)
        self.SALayout.addWidget(self.figCanv)
        self.setCentralWidget(self.SAWidget)

    def showSA(self,SA):
        #self.fig.clear()
        # fig, ax = plt.subplots()
        a = np.arange(len(SA['ST']))
        b = SA['ST']
        #self.fig = plt.figure()
        #self.ax = self.fig.add_subplot(111)
        #self.show()
        #self.setGeometry(500, 500, 300, 300)
        # fig, ax = plt.subplots()

        #self.fig.patch.set_visible(False)

        self.ax.bar(a + 0.35, b, 0.35)


        #self.setCentralWidget(self.SAWidget)



        #self.SAWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.fig.tight_layout()



        self.ax.set_ylim(0, 1)
        self.ax.set_xticklabels(SA['par'])
        self.ax.set_xticks(np.arange(0.5, len(SA['par']) + 1, 1))
        self.ax.set_xlim(0, len(SA['par']))


        self.fig.canvas.draw()
        self.show()

        pass