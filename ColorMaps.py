import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
class colorm:
    def __init__(self):
        aggr1=0.4
        aggr2 = 0.3
        fitnessCmap=LinearSegmentedColormap.from_list('fitness_map',[(aggr1,1,aggr1),(1,1,aggr1),(1,aggr1,aggr1)])
        complexityCmap = LinearSegmentedColormap.from_list('complexity_map', [(1,1,1),(aggr2, 1, 1), (aggr2,aggr2,1),(aggr2, aggr2, aggr2)])

        self.complexity = complexityCmap#plt.get_cmap("cool")
        self.globalm = fitnessCmap
        self.localm = fitnessCmap#plt.get_cmap("RdYlGn")


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