import sys
sys.path.append("fitness/")
import fitness
import numpy as np
from sklearn import linear_model
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import matplotlib.pyplot as plt
import random
import copy
import matplotlib




def evalfit(nbAP,nbPP,dataSize,nbRepet=1000):
        if(nbAP>nbPP):
            nbAPr=nbPP
        else:
            nbAPr=nbAP
        meanf=0
        print("nbPP:"+str(nbPP)+ " nbAP:"+str(nbAPr))
        for i in range(nbRepet):
            X=np.random.rand(dataSize)
            P=np.random.rand(dataSize,nbPP)
            clf = linear_model.OrthogonalMatchingPursuit(n_nonzero_coefs=nbAPr)
            clf.fit(P, X)
            Y=clf.predict(P)
            meanf+= fitness(X, Y) / nbRepet
        return meanf




evalfit(2,50,12)







dataSize=12
nbPotentialParents=range(20)
offsetPP=0
nbAllowedParents=range(6)
nbRepet=5000
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
                    fAct= fitness(X, Y)
                    if(fAct<meanf):
                        meanf=fAct

            else:
                clf = linear_model.OrthogonalMatchingPursuit(n_nonzero_coefs=nbAPr+1)
                clf.fit(P, X)
                Y=clf.predict(P)
                meanf+= fitness(X, Y) / nbRepet
        f[nbPP,nbAP]=meanf

f.tofile('ds'+str(dataSize+1)+'npp'+str(nbPotentialParents[-1]+1)+'nba'+str(nbAllowedParents[-1]+1)+'nbr'+str(nbRepet))
f2=np.fromfile('ds'+str(dataSize+1)+'npp'+str(nbPotentialParents[-1]+1)+'nba'+str(nbAllowedParents[-1]+1)+'nbr'+str(nbRepet))
f2=f2.reshape(nbPotentialParents[-1]+1,nbAllowedParents[-1]+1)
aggr1=0.2
mp = LinearSegmentedColormap.from_list('fitness_map',[(1,1,1),(0, 1-aggr1, 0), (1-aggr1, 1-aggr1, 0), (1-aggr1, 0, 0), ])

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 8}

matplotlib.rc('font', **font)

ax=sns.heatmap(f2,cmap=mp,annot=True,vmin=0,vmax=1)

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)
ax.invert_yaxis()
ax.set_xticks(np.arange(0.5,nbAllowedParents[-1]+1.5,1))
ax.set_xticklabels(range(1,len(nbAllowedParents)+1))
ax.set_xlim((0,nbAllowedParents[-1]+1))
ax.set_yticklabels(range(offsetPP+1,nbPotentialParents[-1]+2+offsetPP))
ax.set_yticks(np.arange(0.5,nbPotentialParents[-1]+1.5,1))
ax.set_xlabel('Number of components in equation')
ax.set_ylabel('Number of candidate components')
ax.set_title('Heatmap of the mean fitness for '+str(nbRepet)+' runs and using '+str(dataSize) +' datapoints')


plt.show(block=True)
a=5
#print(a)

