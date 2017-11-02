import sys
sys.path.append("fitness/")
from fitness import fitness
import numpy as np
from sklearn import linear_model
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import matplotlib.pyplot as plt
import random
import copy

dataSize=12
nbPotentialParents=range(1)
offsetPP=100
nbAllowedParents=range(5)
nbRepet=10
rdmOMP=False
nbRepetrdmOMP=1000

f=np.zeros((len(nbPotentialParents),len(nbAllowedParents)))
for nbPP in nbPotentialParents:
    for nbAP in nbAllowedParents:
        if(nbAP>nbPP+offsetPP):
            nbAPr=nbPP+offsetPP
        else:
            nbAPr=nbAP
        meanf=0
        print("nbPP:"+str(nbPP+1+offsetPP)+ " nbAP:"+str(nbAPr+1))
        for i in range(nbRepet):
            X=np.random.rand(dataSize)
            P=np.random.rand(dataSize,nbPP+1+offsetPP)
            if rdmOMP:
                meanf=1
                P2=copy.deepcopy(P)
                for nbR in range(nbRepetrdmOMP):
                    P=P2[:, random.sample(range(P2.shape[1]), nbAPr+1)]
                    clf = linear_model.OrthogonalMatchingPursuit(n_nonzero_coefs=nbAPr + 1)
                    clf.fit(P, X)
                    Y = clf.predict(P)
                    fAct=fitness(X,Y)
                    if(fAct<meanf):
                        meanf=fAct

            else:
                clf = linear_model.OrthogonalMatchingPursuit(n_nonzero_coefs=nbAPr+1)
                clf.fit(P, X)
                Y=clf.predict(P)
                meanf+=fitness(X,Y)/nbRepet
        f[nbPP,nbAP]=meanf

f.tofile('ds'+str(dataSize+1)+'npp'+str(nbPotentialParents[-1]+1)+'nba'+str(nbAllowedParents[-1]+1)+'nbr'+str(nbRepet))
f2=np.fromfile('ds'+str(dataSize+1)+'npp'+str(nbPotentialParents[-1]+1)+'nba'+str(nbAllowedParents[-1]+1)+'nbr'+str(nbRepet))
f2=f2.reshape(nbPotentialParents[-1]+1,nbAllowedParents[-1]+1)
aggr1=0.2
mp = LinearSegmentedColormap.from_list('fitness_map',[(0, 1-aggr1, 0), (1-aggr1, 1-aggr1, 0), (1-aggr1, 0, 0)])
ax=sns.heatmap(f2,cmap=mp,annot=True,vmin=0,vmax=1)
ax.invert_yaxis()
plt.show()
a=5

