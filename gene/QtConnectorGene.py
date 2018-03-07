from PyQt4.QtCore import *
class QtConnectorGene:
    def __init__(self,vwGene,cntrGene):
        self.vwGene=vwGene
        self.cntrGene=cntrGene
        self.vwGene.networkGUI.fig.canvas.mpl_connect('button_press_event', self.cntrGene.onClick)
        self.vwGene.searchButton.clicked.connect(self.cntrGene.clickSearchGene)
        self.vwGene.cond22h0CB.stateChanged.connect(self.cntrGene.checkBoxCondChanged)
        self.vwGene.cond22h6CB.stateChanged.connect(self.cntrGene.checkBoxCondChanged)
        self.vwGene.cond30h0CB.stateChanged.connect(self.cntrGene.checkBoxCondChanged)
        self.vwGene.cond30h6CB.stateChanged.connect(self.cntrGene.checkBoxCondChanged)
        self.vwGene.removeGeneButton.clicked.connect(self.cntrGene.clickRmGene)
        self.vwGene.addGeneButton.clicked.connect(self.cntrGene.clickAddGene)
        self.vwGene.geneCurrClustList.selectionModel().currentChanged.connect(self.cntrGene.currClustSelChanged)









