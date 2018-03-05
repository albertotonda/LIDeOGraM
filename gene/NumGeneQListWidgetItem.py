from PyQt4.QtGui import *

class NumGeneQListWidgetItem(QListWidgetItem):

    def __init__(self,lab,numGene):
        self.numGene=numGene
        QListWidgetItem.__init__(self,lab)