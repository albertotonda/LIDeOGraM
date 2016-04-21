#-*- coding: utf-8


import random

import networkx as nx
import numpy as np
from numpy import genfromtxt

adj_simple = genfromtxt('data/adj_simple_withMol.csv', delimiter=',')
adj_cmplx  = genfromtxt('data/adj_cmplx_withMol.csv', delimiter=',')
adj_fit    = genfromtxt('data/adj_fit_withMol.csv', delimiter=',')
adj_contr  = genfromtxt('data/adj_contraintes_withMol.csv', delimiter=',')
varnames   = genfromtxt('data/varnames_withMol.csv',dtype='str',delimiter=',')
nbeq       = genfromtxt('data/nbeq_withMol.csv',delimiter=',')
equacolPOf  = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv','float',delimiter=',')
equacolPOs  = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv','str',delimiter=',')
equacolOf  = genfromtxt('data/equa_with_col_Parent_withMol.csv','float',delimiter=',')
equacolOs  = genfromtxt('data/equa_with_col_Parent_withMol.csv','str',delimiter=',')
dataset_cell_popS=genfromtxt('data/dataset_cell_pop.csv','str',delimiter=',')
dataset_mol_cellS=genfromtxt('data/dataset_mol_cell.csv','str',delimiter=',')
dataset_cell_popF=genfromtxt('data/dataset_cell_pop.csv','float',delimiter=',')
dataset_mol_cellF=genfromtxt('data/dataset_mol_cell.csv','float',delimiter=',')


#ts : Slider entre 0 et 1 pour afficher les arrêtes selon les poids sur la matrice d'adjacence simple
#ds : Slider entre 0 et 1 pour la couleur des arrêtes selon la distance à la meilleure équation-compromis
def draw_graph(fig, G, pos, ts, ds):
    edgecolor = []
    edgelist_inOrder = []
    cmplxMin=np.amin(equacolPOf[:, 0]) #Complexite la plus petite sur toutes les equations de tout les noeuds
    cmplxMax=np.amax(equacolPOf[:, 0]) #Complexite la plus grande sur toutes les equations de tout les noeuds

    for v in varnames:
        G.add_node(v)

    for i in range(len(adj_simple)):
        for j in range(len(adj_simple[i])):
            #lIdxColPareto:liste des equations correspondant au couple parent/enfant
            lIdxColPareto = equacolPOf[np.ix_(np.logical_and(equacolPOs[:,2]==varnames[i],equacolPOs[:,3]==varnames[j])),0:2][0]
            if(len(lIdxColPareto)>0): #il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                lIdxColPareto[:,0]=(lIdxColPareto[:,0]-cmplxMin)/(cmplxMax-cmplxMin) #Normalisation de la complexité
                dist_lIdxColPareto=np.sqrt(np.power(np.cos(ds*(np.pi/2))*lIdxColPareto[:,0],2)+
                                          np.power(np.sin(ds*(np.pi/2))*lIdxColPareto[:,1],2))
                dist_lIdxColPareto_idxMin=np.argmin(dist_lIdxColPareto) #Indice dans dist_lIdxColPareto correspondant au meilleur compromi
                dist_lIdxColPareto_valMin=dist_lIdxColPareto[dist_lIdxColPareto_idxMin] #Distance meilleur compromi
                r=adj_simple[i,j]/nbeq[i] #Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                if(r>ts):
                    G.add_edge(varnames[j],varnames[i],adjsimple=adj_simple[i,j],adjfit=
                               adj_fit[i,j],adjcmplx=adj_cmplx[i,j],adjcontr=adj_contr[i,j])
                    edgelist_inOrder.append((varnames[j],varnames[i]))
                    edgecolor.append((dist_lIdxColPareto_valMin + (1-dist_lIdxColPareto_valMin)*(1-r)
                                      ,(1-dist_lIdxColPareto_valMin)+dist_lIdxColPareto_valMin*(1-r)
                                      ,1-r))
    col = []
    nodeWeight = []
    for i in range(len(varnames)):
        if ((len(varnames) - np.sum(adj_contr, axis=0)[i]) != 0):
            # somme du nombre d'équations dans lesquels le noeud-parent intervient divisé par le nombre d'enfant possible du noeud parent
            nodeWeight.append(np.sum(adj_simple, axis=0)[i] / (len(varnames) - np.sum(adj_contr, axis=0)[i]))
        else:
            nodeWeight.append(0)
    for i in range(len(varnames)):
        col.append((0.5, 0.5 + 0.5 * nodeWeight[i] / np.amax(nodeWeight), 0.5))

    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    nx.draw_networkx_nodes(G, pos, nodelist=varnames.tolist(), node_color=col, with_labels=False,
                            edge_color=edgecolor,ax=fig.axes)
    nx.draw_networkx_edges(G, pos, edgelist=edgelist_inOrder, edge_color=edgecolor,ax=fig.axes)

    for p in pos:  # raise text positions
        pos[p][1] += 0.04
    nx.draw_networkx_labels(G, pos,ax=fig.axes)

    for p in pos:  # raise text positions
        pos[p][1] -= 0.04



def pos_graph():
    pos = {}
    pos['Age'] = np.array([0.66, 15.0 / 15.0])
    pos['Temperature'] = np.array([0.33, 15.0 / 15.0])
    pos['AMACBIOSYNTH'] = np.array([random.random() * 0.1 + 0.05,14.0/15.0])
    pos['BIOSYNTH_CARRIERS'] = np.array([random.random() * 0.1 + 0.25,14.0/15.0])
    pos['CELLENVELOPE'] = np.array([random.random() * 0.1 + 0.45,14.0/15.0])
    pos['CELLPROCESSES'] = np.array([random.random() * 0.1 + 0.65,14.0/15.0])
    pos['CENTRINTMETABO'] = np.array([random.random() * 0.1 + 0.85,14.0/15.0])
    pos['ENMETABO'] = np.array([random.random() * 0.1 + 0.05,13.0/15.0])
    pos['FATTYACIDMETABO'] = np.array([random.random() * 0.1 + 0.25,13.0/15.0])
    pos['Hypoprot'] = np.array([random.random() * 0.1 + 0.45,13.0/15.0])
    pos['OTHERCAT'] = np.array([random.random() * 0.1 + 0.65,13.0/15.0])
    pos['PURINES'] = np.array([random.random() * 0.1 + 0.85,13.0/15.0])
    pos['REGULFUN'] = np.array([random.random() * 0.1 + 0.05,12.0/15.0])
    pos['REPLICATION'] = np.array([random.random() * 0.1 + 0.25,12.0/15.0])
    pos['TRANSCRIPTION'] = np.array([random.random() * 0.1 + 0.45,12.0/15.0])
    pos['TRANSLATION'] = np.array([random.random() * 0.1 + 0.65,12.0/15.0])
    pos['TRANSPORTPROTEINS'] = np.array([random.random() * 0.1 + 0.85,12.0/15.0])
    pos['UFA'] = np.array([1 / 4.0, 11.0 / 15.0])
    pos['SFA'] = np.array([2 / 4.0, 11.0 / 15.0])
    pos['CFA'] = np.array([3 / 4.0, 11.0 / 15.0])
    pos['Anisotropie'] = np.array([random.random() * 0.15 + 0.05, 10.0 / 15.0])
    pos['UFAdivSFA'] = np.array([random.random() * 0.15 + 0.3, 10.0 / 15.0])
    pos['CFAdivSFA'] = np.array([random.random() * 0.15 + 0.55, 10.0 / 15.0])
    pos['CFAdivUFA'] = np.array([random.random() * 0.15 + 0.8, 10.0 / 15.0])
    pos['UFCcentri'] = np.array([random.random() * 0.15 + 0.05, 9.0 / 15.0])
    pos['tpH07centri'] = np.array([random.random() * 0.15 + 0.3, 9.0 / 15.0])
    pos['tpH07scentri'] = np.array([random.random() * 0.15 + 0.55, 9.0 / 15.0])
    pos['tpH07spe2centri'] = np.array([random.random() * 0.15 + 0.85, 9.0 / 15.0])
    pos['UFCcong'] = np.array([random.random() * 0.15 + 0.05, 8.0 / 15.0])
    pos['tpH07cong'] = np.array([random.random() * 0.15 + 0.3, 8.0 / 15.0])
    pos['tpH07scong'] = np.array([random.random() * 0.15 + 0.55, 8.0 / 15.0])
    pos['tpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 8.0 / 15.0])
    pos['dUFCcong'] = np.array([random.random() * 0.15 + 0.05, 7.0 / 15.0])
    pos['dtpH07cong'] = np.array([random.random() * 0.15 + 0.3, 7.0 / 15.0])
    pos['dtpH07scong'] = np.array([random.random() * 0.15 + 0.55, 7.0 / 15.0])
    pos['dtpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 7.0 / 15.0])
    pos['UFClyo'] = np.array([random.random() * 0.15 + 0.05, 6.0 / 15.0])
    pos['TpH07lyo'] = np.array([random.random() * 0.15 + 0.2, 6.0 / 15.0])
    pos['tpH07slyo'] = np.array([random.random() * 0.15 + 0.55, 6.0 / 15.0])
    pos['tpH07spe2lyo'] = np.array([random.random() * 0.15 + 0.8, 6.0 / 15.0])
    pos['dUFCdes'] = np.array([random.random() * 0.15 + 0.05, 5.0 / 15.0])
    pos['dtpH07des'] = np.array([random.random() * 0.15 + 0.3, 5.0 / 15.0])
    pos['dtpH07sdes'] = np.array([random.random() * 0.15 + 0.55, 5.0 / 15.0])
    pos['dtpH07spe2des'] = np.array([random.random() * 0.15 + 0.8, 5.0 / 15.0])
    pos['dtUFClyo'] = np.array([random.random() * 0.15 + 0.05, 4.0 / 15.0])
    pos['dtpH07lyo'] = np.array([random.random() * 0.15 + 0.3, 4.0 / 15.0])
    pos['dtpH07slyo'] = np.array([random.random() * 0.15 + 0.55, 4.0 / 15.0])
    pos['dtpH07spe2lyo'] = np.array([random.random() * 0.15 + 0.8, 4.0 / 15.0])
    pos['UFCsto3'] = np.array([random.random() * 0.15 + 0.05, 3.0 / 15.0])
    pos['tpH07sto3'] = np.array([random.random() * 0.15 + 0.3, 3.0 / 15.0])
    pos['tpH07ssto3'] = np.array([random.random() * 0.15 + 0.55, 3.0 / 15.0])
    pos['tpH07spe2sto3'] = np.array([random.random() * 0.15 + 0.8, 3.0 / 15.0])
    pos['dUFCsto3'] = np.array([random.random() * 0.15 + 0.05, 2.0 / 15.0])
    pos['dtpH07sto3'] = np.array([random.random() * 0.15 + 0.3, 2.0 / 15.0])
    pos['dtpH07ssto3'] = np.array([random.random() * 0.15 + 0.55, 2.0 / 15.0])
    pos['dtpH07spe2sto3'] = np.array([random.random() * 0.15 + 0.8, 2.0 / 15.0])
    pos['dUFCtot'] = np.array([random.random() * 0.15 + 0.05, 1.0 / 15.0])
    pos['dtpH07tot'] = np.array([random.random() * 0.15 + 0.3, 1.0 / 15.0])
    pos['dtpH07stot'] = np.array([random.random() * 0.15 + 0.55, 1.0 / 15.0])
    pos['dtpH07spe2tot'] = np.array([random.random() * 0.15 + 0.8, 1.0 / 15.0])
    return pos

