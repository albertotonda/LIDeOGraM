import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
class colorm:
    def __init__(self):
        aggr1=0.2
        aggr2 = 0.5
        #fitnessCmap=LinearSegmentedColormap.from_list('fitness_map',[(aggr1,1,aggr1),(1,1,aggr1),(1,aggr1,aggr1)])
        fitnessCmap = LinearSegmentedColormap.from_list('fitness_map',[(0, 1-aggr1, 0), (1-aggr1, 1-aggr1, 0), (1-aggr1, 0, 0)])
        #complexityCmap = LinearSegmentedColormap.from_list('complexity_map', [(1,1,1),(aggr2, 1, 1), (aggr2,aggr2,1),(aggr2, aggr2, aggr2)])
        complexityCmap = LinearSegmentedColormap.from_list('complexity_map',[(0.8, 0.8, 0.95),(0.2, 0.2, 0.95),(0,0,0)])
        # saCmap = LinearSegmentedColormap.from_list('sa_map', [(0, 1 - aggr1, 0),
        #                                                       ((1 - aggr1) * 0.2, 1 - aggr1, 0),
        #                                                       ((1 - aggr1) * 0.4, 1 - aggr1, 0),
        #                                                       ((1 - aggr1) * 0.6, 1 - aggr1, 0),
        #                                                       ((1 - aggr1) * 0.8, 1 - aggr1, 0),
        #                                                       (1 - aggr1, 1 - aggr1, 0),
        #                                                                 (1 - aggr1, 0, 0)])
        vCol=(0.65,0.2,0.65)
        gCol=(0.9,0.9,0.9)
        grnCol=(0.35, 0.8, 0.35)
        saCmap = LinearSegmentedColormap.from_list('sa_map', [vCol,
                                                              (vCol[0]*0.5+gCol[0]*0.5,vCol[1]*0.5+gCol[1]*0.5,vCol[2]*0.5+gCol[2]*0.5),
                                                              gCol,
                                                              gCol,
                                                              grnCol])

        psCmap = LinearSegmentedColormap.from_list('Pearson_map', [(0.9,0.5,0.0),(0.9,0.9,0.9),(0.9,0.9,0.9),(0.9,0.9,0.9),(0.0,0.5,0.9)])

        self.complexity = complexityCmap#plt.get_cmap("cool")
        self.globalm = fitnessCmap
        self.localm = fitnessCmap
        self.sam = saCmap#plt.get_cmap("RdYlGn")
        self.psm=psCmap
        #self.selectionColor=(0.5,0.5,0.9)


    def multiply(self,cmap):
        f = list(map(lambda x : int(x*255), cmap))
        return f

    @staticmethod
    def selection(normed=False):
        if normed:
            return (0.5,0.5,0.5)
        return (125,125,125)


    def get(self, type, normalizedValue):
        if type == "complexity":
            return self.multiply(self.complexity(normalizedValue)[0:3])

        if type == "global":
            return self.multiply(self.globalm(normalizedValue)[0:3])

        if type == "local":
            return self.multiply(self.localm(normalizedValue)[0:3])
        if type == "SA":
            return self.multiply(self.sam(normalizedValue)[0:3])
        if type == "Pearson":
            return self.multiply(self.psm(normalizedValue)[0:3])