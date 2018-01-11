import numpy as np
from sklearn.cluster import DBSCAN
import copy

X = np.genfromtxt('data/resultats_tri_entier_sansribosomauxTCnorm.csv', delimiter=';')
X=X[1:,[1,2,3,4,5,6,13,14,15,16,17,18]]
X=np.delete(X,(2141),axis=0)
for i in range(len(X)):
    X[i,:]=X[i,:]/np.mean(X[i,:])

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

f=np.where(rv>1)[0]
Xf=X[f,:]

db = DBSCAN(eps=0.5, min_samples=3).fit(Xf)
labels = db.labels_
dn_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print('nbclusters:',dn_clusters_ )
Xb=copy.deepcopy(Xf)
offset=0
for i in range(-1,dn_clusters_ ):

    w=np.where(labels==i)
    print('class ',i,' ',len(w[0]))
    if i>-10 :
        print(w)
    Xb[offset:(offset+len(w[0])),:]=X[w[0],:]


a=5