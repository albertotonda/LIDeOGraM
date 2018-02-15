import numpy as np
from sklearn.cluster import DBSCAN
import copy
import pandas as pd

import csv
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#X = np.genfromtxt('data/resultats_tri_entier_sansribosomauxTCnorm.csv', delimiter=';')
X = np.genfromtxt('data/resultats_tri_entier4cond_normDESeq.csv', delimiter=';')
r= pd.read_csv('data/resultats_tri_entierTCnorm.csv',sep=';',encoding = "ISO-8859-1")
blt= pd.read_csv('data/ResultListbis_classification(2).csv',sep=' ',encoding = "ISO-8859-1")

loc=[]
torm=[]
for i in range(1,len(X)):
    print(i)
    infos=[]
    locid=r.iloc[np.where(r.iloc[:,0] == X[i,0])[0][0],1]
    infos.append(locid)
    p=np.where(blt.iloc[:,3]==locid)[0]
    if not p.tolist() == []:
        l=list(blt.iloc[p,4:8].values[0])
        infos.extend(l)
        if( l[1]=='Hypotheticalprotein'):
            torm.append(i)
    else:
        infos.extend([[],[],[],[],[]])
    loc.append(infos)

np.where(r.iloc[:,1] == 'O208_01742')
torm.append(2141)
X=np.delete(X,torm ,axis=0)
torm2=[t -1 for t in torm]
loc=np.delete(loc,torm2,axis=0)

#X=X[1:,[1,2,3,4,5,6,13,14,15,16,17,18]]
X=X[1:,[1,2,3,4,5,6,7,8,9,10,11,12]]
X2=X2=copy.deepcopy(X)
#X=np.delete(X,(2141),axis=0)
for i in range(len(X)):
    #X[i,:]=X[i,:]/np.mean(X[i,:])
    #X[i, :] = (X[i, :] - np.mean(X[i, :]))/np.std(X[i, :])
    #X[i, :] = (X[i, :] - np.mean(X[i, :])) / np.mean(X[i, :])
    X[i, :] = np.log((X[i, :] / np.mean(X[i, :])))
    X[i, :] = (X[i, :] - np.mean(X[i, :]))/np.std(X[i, :])




rv=np.zeros(len(X))
for i in range(len(X)):
    i1 = [0,1,2];
    i2 = [3,4,5];
    i3 = [6,7,8];
    i4 = [9,10,11];

    v1 = np.var(X[i,i1]);
    v2 = np.var(X[i, i2]);
    v3 = np.var(X[i, i3]);
    v4 = np.var(X[i, i4]);

    m1 = np.mean(X[i,i1]);
    m2 = np.mean(X[i, i2]);
    m3 = np.mean(X[i, i3]);
    m4 = np.mean(X[i, i4]);

    vm = np.var([m1,m2,m3,m4]);
    rv[i] = vm / np.max([v1,v2,v3,v4]);

f=np.where(rv>0)[0] #Indices respectant cette contrainte
Xf=X[f,:]
alrdplt=[]

for epsdb in np.arange(0.1, 1.5, 0.2):

    minsample=2
    db = DBSCAN(eps=epsdb, min_samples=minsample).fit(Xf)
    labels = db.labels_
    dn_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('nbclusters:',dn_clusters_ )
    Xb=copy.deepcopy(Xf)
    offset=0
    todata=[]
    for i in range(-1,dn_clusters_ ): #Parcours toute les classes

        w=np.where(labels==i)[0]
        print('class ',i,' ',len(w))
        if i>-1 :
            todataclass=[0]*12
            for j in w: #Parcours les indices dans f de la classe courante
                print(loc[f[j]])
                #print(X2[f[j]])
                todataclass+=X2[f[j]] #Les 12 points de données correspondant à un gène de cette classe

            if not  np.any(alrdplt==w):
                fig, ax = plt.subplots()
                for j in w:
                    ax.plot(Xf[j], 'o-',c=np.random.rand(3,1),label=loc[f[j]][1] + ' ' + loc[f[j]][0][5:] )
                ax.set_ylim((np.minimum(-3,ax.get_ylim()[0]),np.maximum(3,ax.get_ylim()[1])))
                score=np.std(Xf[w])
                ax.set_title("class : "+str(i)+ ' nbGene:' + str(len(w)) + ' epsdb:' +str(epsdb)+ ' minsample:'+ str(minsample)  + ' score:' + str(score))

                ax.legend(fontsize = 'xx-small')
                #fig.show()
                fig.savefig('fig3/'+"class  "+str(i)+  ' nbGene ' + str(len(w)) +' epsdb' +str(epsdb)+ ' minsample'+ str(minsample)  + ' score' + str(score)+'.png',dpi=400)
                alrdplt.append(w)
            # plt.plot(Xf[w[1]], 'bo-')
            # plt.plot(Xf[w[2]], 'go-')
            # plt.plot(Xf[w[3]], 'yo-')
            #distance.euclidean(Xf[w[0][2]],Xf[w[0][3]])

            todataline=[]
            todataline.append('Class'+str(i))
            todataline.append('Genes')
            todataline.append('0')
            todataline.extend(todataclass)
            todata.append(todataline)
            #print(todataline)

        Xb[offset:(offset+len(w)),:]=X[w,:]


fig, ax = plt.subplots()
l=np.where(loc[:,0]=='O208_01367' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01367')
l=np.where(loc[:,0]=='O208_01368' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01368')
l=np.where(loc[:,0]=='O208_01369' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01367')
l=np.where(loc[:,0]=='O208_01367' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01369')
l=np.where(loc[:,0]=='O208_01370' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01370')
l=np.where(loc[:,0]=='O208_01371' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='atpA')
l=np.where(loc[:,0]=='O208_01372' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01372')
#l=np.where(loc[:,0]=='O208_01373' )[0]
#ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01373')
l=np.where(loc[:,0]=='O208_01374' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='atpD')
l=np.where(loc[:,0]=='O208_01375' )[0]
ax.plot(X[l][0], 'o-',c=np.random.rand(3,1),label='O208_01375')
ax.legend()
fig.show()

# todata=np.transpose(todata)
# #todata=todata[[0,1,2,3,5,6,8,9,10,13,14,4,7,11,12],:]
# todata=todata[[0,1,2,3,4,5,6,7,8,9,10,11,12],:]
# with open("testdatagenes3.csv", 'w',newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(todata)

#np.savetxt("testdatagenes.csv", todata, delimiter=",")
a=5