from PyQt4.QtCore import *
class QtConnectorGene:
    def __init__(self,vwGene,cntrGene):
        self.vwGene=vwGene
        self.cntrGene=cntrGene
        self.vwGene.networkGUI.fig.canvas.mpl_connect('button_press_event', self.cntrGene.onClick)