import numpy as np
import matplotlib.pyplot as plt

class colorm:
    def __init__(self):
        self.complexity = plt.get_cmap("cool")
        self.globalm = plt.get_cmap("winter")
        self.localm = plt.get_cmap("summer")


    def multiply(self,cmap):
        f = list(map(lambda x : int(x*255), cmap))
        return f

    def get(self, type, normalizedValue):
        if type == "complexity":
            return self.multiply(self.complexity(normalizedValue)[0:3])

        if type == "global":
            return self.multiply(self.globalm(normalizedValue)[0:3])

        if type == "local":
            return self.multiply(self.localm(normalizedValue)[0:3])