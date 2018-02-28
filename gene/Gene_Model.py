import numpy as np
from sklearn.cluster import DBSCAN
import copy
import pandas as pd
import seaborn as sns
import hdbscan
import csv
from scipy.spatial import distance
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import networkx as nx
import dill
from Gene_View import Gene_View
from QtConnectorGene import QtConnectorGene
import random
import sklearn as sk
from scipy.spatial import distance

class Gene_Model():

    def __init__(self):

        filename = 'globalsavesup1.pkl'
        #dill.load_session(filename)
        self.lastNodeClicked=None
        self.radius = 0.002
        self.highlightNode=-1
        self.currGeneExpPlt=None
        self.currprof=None

        self.thresholdVar=None
        self.minClusterSize=None
        self.activCond=None
        self.activCondShow=None

    def searchClusters(self):


        #X = np.genfromtxt('../data/resultats_tri_entier_sansribosomauxTCnorm.csv', delimiter=';')


        #X = np.genfromtxt('../data/resultats_tri_entier4cond_normDESeq.csv', delimiter=';')
        Xp = pd.read_csv('../data/resultats_tri_entier4cond_normDESeq.csv', sep=';')

        r= pd.read_csv('../data/resultats_tri_entierTCnorm.csv',sep=';',encoding = "ISO-8859-1")
        blt= pd.read_csv('../data/ResultListbis_classification(2).csv',sep=' ',encoding = "ISO-8859-1")

        loc=[]
        torm=[]
        #i=0
        for XpRow_index,XpRow in Xp.iterrows():
        #for i in range(1,len(Xp.loc)):
            print(XpRow_index)
            infos=[]
            locid = XpRow.cds_locustag
            #locid=r.iloc[np.where(r.iloc[:,0] == X[i,0])[0][0],1]
            infos.append(locid)

            l=blt[blt.LocusID==locid][['Genename','Function','ECNumber','Class1','Class2']].values[0]
            infos.extend(l)
            #p=np.where(blt.LocusID==locid)[0]
            #if not p.tolist() == []:
                #l=list(blt.iloc[p,4:8].values[0])
                #infos.extend(l)
                #if( l[1]=='Hypotheticalprotein'):
                #    torm.append(i)
            #else:
            #    infos.extend([[],[],[],[],[]])
            loc.append(infos)
            #i+=1

        #np.where(r.iloc[:,1] == 'O208_01742')

        X = Xp.drop(Xp[(Xp == 0).any(1)].index)

        #torm.append(2141)
        #torm.append(451)
        #X=np.delete(X,torm ,axis=0)
        #torm2=[t -1 for t in torm]

        self.loc=np.delete(np.array(loc),np.where((Xp == 0).any(1))[0],axis=0)

        #X=X[1:,[1,2,3,4,5,6,13,14,15,16,17,18]]
        X=X[['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18']].as_matrix()
        #X=X[1:,[1,2,3,4,5,6,7,8,9,10,11,12]]
        self.X2=copy.deepcopy(X)
        self.X2=self.X2[:,self.activCond]
        #X=np.delete(X,(2141),axis=0)





        rv=np.zeros(len(self.X2))
        for i in range(len(self.X2)):
            nbcond=len(self.X2[0])/3
            print(nbcond,int(nbcond))

            v=[]
            m=[]
            for j in range(int(nbcond)):
                ci=[k+3*j for k in range(3)]
                v.append(np.var(self.X2[i,ci]))
                m.append(np.mean(self.X2[i,ci]))
            vm=np.var(m)
            rv[i] = vm / np.max(v)


            # i1 = [0,1,2];
            # i2 = [3,4,5];
            # i3 = [6,7,8];
            # i4 = [9,10,11];
            #
            # v1 = np.std(self.X2[i,i1]);
            # v2 = np.std(self.X2[i, i2]);
            # v3 = np.std(self.X2[i, i3]);
            # v4 = np.std(self.X2[i, i4]);
            #
            # m1 = np.mean(self.X2[i,i1]);
            # m2 = np.mean(self.X2[i, i2]);
            # m3 = np.mean(self.X2[i, i3]);
            # m4 = np.mean(self.X2[i, i4]);
            #
            # vm = np.std([m1,m2,m3,m4]);
            # rv[i] = vm / np.max([v1,v2,v3,v4]);

        for i in range(len(X)):
            #X[i,:]=X[i,:]/np.mean(X[i,:])
            #X[i, :] = (X[i, :] - np.mean(X[i, :]))/np.std(X[i, :])
            #X[i, :] = (X[i, :] - np.mean(X[i, :])) / np.mean(X[i, :])
            X[i, :] = np.log((X[i, :] / np.mean(X[i, :])))
            X[i, :] = (X[i, :] - np.mean(X[i, :]))/np.std(X[i, :])

        self.f=np.where(rv>self.thresholdVar)[0] #Indices respectant cette contrainte
        self.Xf=X[self.f,:]
        alrdplt=[]

        # dill.dump_session(filename)

        #clusterer = hdbscan.HDBSCAN(min_cluster_size=5,min_samples=1,gen_min_span_tree=True)
        #clusterer.fit(self.Xf)

        #self.TXf = sk.manifold.TSNE().fit_transform(self.Xf)   n_iter =50000 ,

        self.TXf = sk.manifold.TSNE( n_iter =50000000 ,learning_rate = 200,metric='manhattan',perplexity=15,random_state =1234).fit_transform(self.Xf)

        clusterer = hdbscan.HDBSCAN(min_cluster_size=self.minClusterSize, min_samples=1, gen_min_span_tree=True)
        clusterer.fit(self.Xf)

        labels=clusterer.labels_
        nbLabels=clusterer.labels_.max()
        fig, ax = plt.subplots()
        clusterer.condensed_tree_.plot(select_clusters=True, selection_palette=sns.color_palette())
        #fig.savefig('fighdbscan3/'+'tree.png',dpi=400)
        #g = clusterer.condensed_tree_.to_networkx()

        self.tree=clusterer.condensed_tree_.to_pandas()

        self.parents=self.tree.parent.unique()
        self.childs=self.tree.child.unique()
        self.leafs=self.tree[self.tree.child_size == 1].child
        self.p0=[p for p in self.parents if p not in self.childs]



        self.G = nx.DiGraph()
        self.labels={}
        for p in self.parents:
            self.G.add_node(p)
            self.labels[p]=len(self.getallchildfrom([p]))

        for index, row in self.tree.iterrows():
            if row.child in self.parents:
                self.G.add_edge(row.parent,row.child)

        self.pos = self.hierarchy_pos(self.G, self.p0[0])

        self.pos=self.posbetween0and1(self.pos)

        self.lpos = copy.deepcopy(self.pos)
        for p in self.lpos:  # raise text positions
            self.lpos[p] = (self.lpos[p][0], self.lpos[p][1] + 0.0)




    def getallchildfrom(self,parentSearch):
        leafs = [sp for p in parentSearch for sp in self.tree[self.tree.parent == p].child if not sp in self.parents]
        newp = [sp for p in parentSearch for sp in self.tree[self.tree.parent == p].child if sp in self.parents]
        if len(newp) > 0:
            leafs.extend(self.getallchildfrom(newp))
        return leafs


    def profondeur(self,p):
        newp = self.tree[self.tree.child == p].parent
        if newp.empty:
            prof = 0
        else:
            prof = 1 + self.profondeur(newp.values[0])
        return prof

    def posbetween0and1(self,pos):

        minx = np.inf
        maxx = -np.inf
        miny = np.inf
        maxy = -np.inf
        for k, p in list(pos.items()):
            if (minx > p[0]):
                minx = p[0]
            if (maxx < p[0]):
                maxx = p[0]
            if (miny > p[1]):
                miny = p[1]
            if (maxy < p[1]):
                maxy = p[1]
        if(miny==maxy):
            for k in list(pos.keys()):
                pos[k]=(pos[k][0],random.random()*300)
            for k, p in list(pos.items()):
                if (minx > p[0]):
                    minx = p[0]
                if (maxx < p[0]):
                    maxx = p[0]
                if (miny > p[1]):
                    miny = p[1]
                if (maxy < p[1]):
                    maxy = p[1]
        for k in pos:
            pos[k] = ((pos[k][0] - minx) / (maxx - minx), (pos[k][1] - miny) / (maxy - miny))
        return pos

    def hierarchy_pos(self,G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5,
                      pos=None, parent=None,go=None):
        '''If there is a cycle that is reachable from root, then this will see infinite recursion.
           G: the graph
           root: the root node of current branch
           width: horizontal space allocated for this branch - avoids overlap with other branches
           vert_gap: gap between levels of hierarchy
           vert_loc: vertical location of root
           xcenter: horizontal location of root
           pos: a dict saying where all nodes go if they have been assigned
           parent: parent of this branch.'''
        if pos == None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        neighbors = G.neighbors(root)
        #if parent != None:  # this should be removed for directed graphs.
        #    neighbors.remove(parent)  # if directed, then parent not in neighbors.
        if len(neighbors) != 0:
            dx = width / len(neighbors)
            nextx = xcenter - width / 2 - dx / 2



            # if len(G.neighbors(neighbors[1])) ==0: #If the right neighbor has no child
            #     nextx = xcenter
            #     pos = self.hierarchy_pos(G, neighbors[0], width=dx, vert_gap=vert_gap,
            #                         vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
            #                         parent=root)
            #     nextx = xcenter + dx
            #     pos = self.hierarchy_pos(G, neighbors[1], width=dx, vert_gap=vert_gap,
            #                              vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
            #                              parent=root)
            #
            # elif len(G.neighbors(neighbors[0])) ==0: #If the left neighbor has no child
            #     nextx = xcenter - dx
            #     pos = self.hierarchy_pos(G, neighbors[0], width=dx, vert_gap=vert_gap,
            #                         vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
            #                         parent=root)
            #     nextx = xcenter
            #     pos = self.hierarchy_pos(G, neighbors[1], width=dx, vert_gap=vert_gap,
            #                              vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
            #                              parent=root)
            # else:
            if go==None:
                for neighbor in neighbors:
                    nextx += dx
                    if len(G.neighbors(neighbors[0])) == 0:  # If the left neighbor has no child
                        pos = self.hierarchy_pos(G, neighbor, width=dx , vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root, go='Left')
                    elif len(G.neighbors(neighbors[1])) == 0:  # If the right neighbor has no child
                        pos = self.hierarchy_pos(G, neighbor, width=dx , vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root, go='Right')
                    else:
                        pos = self.hierarchy_pos(G, neighbor, width=dx , vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root)
            elif go=='Left':
                nextx = xcenter - dx *4
                for neighbor in neighbors:
                    nextx += dx*2
                    if len(G.neighbors(neighbors[0])) == 0:  # If the left neighbor has no child
                        pos = self.hierarchy_pos(G, neighbor, width=dx * 2, vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root, go='Left')
                    elif len(G.neighbors(neighbors[1])) == 0:  # If the right neighbor has no child
                        pos = self.hierarchy_pos(G, neighbor, width=dx * 2, vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root, go='Right')
                    else:
                        pos = self.hierarchy_pos(G, neighbor, width=dx * 2, vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root)
            elif go=='Right':
                nextx=xcenter-dx*2
                for neighbor in neighbors:
                    nextx += dx*2
                    if len(G.neighbors(neighbors[0])) ==0: #If the left neighbor has no child
                        pos = self.hierarchy_pos(G, neighbor, width=dx*2, vert_gap=vert_gap,
                                        vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                        parent=root,go='Left')
                    elif len(G.neighbors(neighbors[1]))==0: #If the right neighbor has no child
                        pos = self.hierarchy_pos(G, neighbor, width=dx * 2, vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root,go='Right')
                    else:
                        pos = self.hierarchy_pos(G, neighbor, width=dx * 2, vert_gap=vert_gap,
                                                 vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                                 parent=root)
        return pos


#a = 5
# fig, ax = plt.subplots()
# nx.draw(self.G, self.pos, with_labels=True)


# p1=[sp for p in p0 for sp in tree[tree.parent==p].child]
# p2=[sp for p in p1 for sp in tree[tree.parent==p].child]
# p3=[sp for p in p2 for sp in tree[tree.parent==p].child]
# p4=[sp for p in p3 for sp in tree[tree.parent==p].child]
# p5=[sp for p in p4 for sp in tree[tree.parent==p].child]
# p6=[sp for p in p5 for sp in tree[tree.parent==p].child]


# for p in self.parents:
#     prof=self.profondeur(p)
#
#
#     w=self.getallchildfrom([p])
#     print(len(w))
#
#     todataclass=[0]*12
#     for j in w: #Parcours les indices dans f de la classe courante
#         print(loc[f[j]])
#         #print(X2[f[j]])
#         todataclass+=X2[f[j]] #Les 12 points de données correspondant à un gène de cette classe
#
#     if not  np.any(alrdplt==w):
#         fig, ax = plt.subplots()
#         ax.set_position([0.1, 0.1, 0.7, 0.8])
#         for j in w:
#             ax.plot(Xf[j], 'o-',c=np.random.rand(3,1),label=loc[f[j]][1] + ' ' + loc[f[j]][0][5:] )
#         ax.set_ylim((np.minimum(-3,ax.get_ylim()[0]),np.maximum(3,ax.get_ylim()[1])))
#         score=np.std(Xf[w])
#         ax.set_title("prof : "+str(prof)+ 'nbGene:' + str(len(w)) +  ' score:' + str(score))
#
#         ax.legend(fontsize = 'xx-small',bbox_to_anchor=(1.25, 1))
#         #fig.show()
#         fig.savefig('fighdbscan3/'+"prof  "+str(prof)+  ' nbGene ' + str(len(w)) + ' score' + str(score)+'.png',dpi=400)
#         alrdplt.append(w)
#
#
#
# g = clusterer.condensed_tree_.to_networkx()
# fig, ax = plt.subplots()
# posG = nx.nx_pydot.graphviz_layout(g, prog='dot',ax=ax)
# nx.draw(g,posG,with_labels=True)
# fig.savefig('fighdbscan3/'+'nx.png',dpi=400)
# a=5