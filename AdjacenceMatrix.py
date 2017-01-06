import numpy as np
class AdjacenceMatrix:
    def __init__(self,corr,initval):
        self.corr=corr
        size=len(self.corr)
        self.mat=np.full((size,size),initval)

    def set(self,x,y,val):
        self.mat[self.corr.index(x), self.corr.index(y)]=val

    def get(self,x,y):
        return self.mat[self.corr.index(x),self.corr.index(y)]