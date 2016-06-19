#-*- coding: utf-8
import random
import numpy as np
from numpy import genfromtxt
import copy
import networkx as nx
#nx.use('qt4agg')
from ArrayConverter import ArrayConverter
import re

# TODO  Définie la position des noeuds et les initialise
class RFGraph_Model:

    def __init__(self):

        equacolPdata = []
        eureqafile=open('data/eureqa_sans_calc.txt','r')
        for line in eureqafile:
            line = line.replace("\t", ",")
            line=line.replace("\"","")
            line=line.replace(" = ",",")
            line=line.replace(" ","")
            line=line.replace("\n","")
            line=line.split(',')
            equacolPdata.append(line)
        self.equacolO=ArrayConverter.convertP(equacolPdata)
        self.nbequa=len(self.equacolO)
        self.dataDict,self.identvarDict,self.dataset=self.loadDataFile("data/dataset_cell_pop_nocalc.csv")
        self.varnames=np.array(list(self.dataDict[0].keys()))
        self.nbVar=len(self.varnames)
        self.adj_simple=np.zeros((self.nbVar,self.nbVar))
        self.adj_fit=np.ones((self.nbVar,self.nbVar))
        self.adj_cmplx=np.ones((self.nbVar,self.nbVar))
        self.nbeq=np.zeros(self.nbVar)
        self.equacolPO=[]

        for l in range(self.nbequa):
            for h in range(self.nbVar):       #Possible parents for the equations
                cont_h=len(re.findall(r'\b%s\b' % re.escape(self.varnames[h]),self.equacolO[l,3]))  #How many times the variable self.varname[h] is found in the equation self.
                if(cont_h>0):
                    ind_parent=h
                    ind_offspring=list(self.varnames).index(self.equacolO[l,2])
                    self.adj_simple[ind_offspring,ind_parent]+=1
                    self.adj_cmplx[ind_offspring,ind_parent]*=self.equacolO[l,0] # Moyenne GEOMETRIQUE
                    self.adj_fit[ind_offspring,ind_parent]*=self.equacolO[l,1] # Moyenne GEOMETRIQUE
                    self.equacolPO.append([self.equacolO[l,0],self.equacolO[l,1],self.equacolO[l,2],self.varnames[h],self.equacolO[l,3]])
            self.nbeq[list(self.varnames).index(self.equacolO[l,2])]+=1 # Comptage du nombre d'équations pour chaque enfant

        self.equacolPO=ArrayConverter.convertPO(self.equacolPO)
        self.adj_cmplx=np.power(self.adj_cmplx,1/self.adj_simple)
        self.adj_cmplx[self.adj_simple==0]=0
        self.adj_fit = np.power(self.adj_fit, 1 / self.adj_simple)
        self.adj_fit[self.adj_simple == 0] = 0

        self.adj_contrGraph=self.createConstraintsGraph()
        self.adj_contr=self.createConstraints()

        self.pos=self.pos_graph()
        #self.pos = []
        #self.adj_simple = genfromtxt('data/adj_simple_withMol.csv', delimiter=',')
        #self.adj_cmplx = genfromtxt('data/adj_cmplx_withMol.csv', delimiter=',')
        #self.adj_fit = genfromtxt('data/adj_fit_withMol.csv', delimiter=',')
        #self.adj_contr = genfromtxt('data/adj_contraintes_withMol.csv', delimiter=',')
        #self.varnames = genfromtxt('data/varnames_withMol.csv', dtype='str', delimiter=',')
        #self.nbeq = genfromtxt('data/nbeq_withMol.csv', delimiter=',')
        #self.equacolPOf = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv', 'float', delimiter=',')
        #self.equacolPOs = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv', 'str', delimiter=',')
        #self.equacolOf = genfromtxt('data/equa_with_col_Parent_withMol.csv', 'float', delimiter=',')
        #self.equacolOs = genfromtxt('data/equa_with_col_Parent_withMol.csv', 'str', delimiter=',')
        #self.dataset_cell_popS = genfromtxt('data/dataset_cell_pop.csv', 'str', delimiter=',')
        #self.dataset_mol_cellS = genfromtxt('data/dataset_mol_cell.csv', 'str', delimiter=',')
        #self.dataset_cell_popF = genfromtxt('data/dataset_cell_pop.csv', 'float', delimiter=',')
        #self.dataset_mol_cellF = genfromtxt('data/dataset_mol_cell.csv', 'float', delimiter=',')
        self.varsIn = ['Temperature','Age']
        self.NodeConstraints = []
        self.showGlobalModel = False
        self.lastNodeClicked = ""
        self.last_clicked = None
        self.mode_cntrt = False
        self.cntrt_FirstClick = ''
        self.cntrt_SecondClick = ''
        self.forbidden_edge = []
        self.curr_tabl=[]
        self.adjThresholdVal=0.5
        self.comprFitCmplxVal=0.5
        self.opt_params= []
        self.error_paramas= []
        self.help_params= []
        self.clicked_line=-1
        self.old_color=[]
        self.nodeColor = []
        self.edgeColor = []
        self.nodeWeight = []
        self.cmplxMin = np.amin(self.equacolPO[:, 0])
        self.cmplxMax = np.amax(self.equacolPO[:, 0])
        self.pareto = []
        #Necessaire de faire une deepcopy ?
        self.lpos= copy.deepcopy(self.pos)
        for p in self.lpos:  # raise text positions
        # self.modApp.lpos[p] = (self.modApp.lpos[p][0],self.modApp.lpos[p][1]+0.04)
            self.lpos[p][1] +=0.04

        # Charge la base de données d'équations à afficher après chargement
        # TODO: Base de données d'équations à changer
        self.data = []
        for i in range(len(self.equacolPO)):
            self.data.append(self.equacolPO[i, np.ix_([0, 1, 4])][0])

        self.labels = {}
        self.edges = None
        self.initGraph()

    def pos_graph(self):
        pos = {}
        pos['Age'] = np.array([0.66, 15.0 / 15.0])
        pos['Temperature'] = np.array([0.33, 15.0 / 15.0])
        #pos['AMACBIOSYNTH'] = np.array([random.random() * 0.1 + 0.05,14.0/15.0])
        #pos['BIOSYNTH_CARRIERS'] = np.array([random.random() * 0.1 + 0.25,14.0/15.0])
        #pos['CELLENVELOPE'] = np.array([random.random() * 0.1 + 0.45,14.0/15.0])
        #pos['CELLPROCESSES'] = np.array([random.random() * 0.1 + 0.65,14.0/15.0])
        #pos['CENTRINTMETABO'] = np.array([random.random() * 0.1 + 0.85,14.0/15.0])
        #pos['ENMETABO'] = np.array([random.random() * 0.1 + 0.05,13.0/15.0])
        #pos['FATTYACIDMETABO'] = np.array([random.random() * 0.1 + 0.25,13.0/15.0])
        #pos['Hypoprot'] = np.array([random.random() * 0.1 + 0.45,13.0/15.0])
        #pos['OTHERCAT'] = np.array([random.random() * 0.1 + 0.65,13.0/15.0])
        #pos['PURINES'] = np.array([random.random() * 0.1 + 0.85,13.0/15.0])
        #pos['REGULFUN'] = np.array([random.random() * 0.1 + 0.05,12.0/15.0])
        #pos['REPLICATION'] = np.array([random.random() * 0.1 + 0.25,12.0/15.0])
        #pos['TRANSCRIPTION'] = np.array([random.random() * 0.1 + 0.45,12.0/15.0])
        #pos['TRANSLATION'] = np.array([random.random() * 0.1 + 0.65,12.0/15.0])
        #pos['TRANSPORTPROTEINS'] = np.array([random.random() * 0.1 + 0.85,12.0/15.0])
        #pos['UFA'] = np.array([1 / 4.0, 11.0 / 15.0])
        #pos['SFA'] = np.array([2 / 4.0, 11.0 / 15.0])
        #pos['CFA'] = np.array([3 / 4.0, 11.0 / 15.0])
        pos['C140'] = np.array([random.random() * 0.1 + 0.05,13.0/15.0])
        pos['C150'] = np.array([random.random() * 0.1 + 0.25,13.0/15.0])
        pos['C160'] = np.array([random.random() * 0.1 + 0.45,13.0/15.0])
        pos['C161cis'] = np.array([random.random() * 0.1 + 0.65,13.0/15.0])
        pos['C170'] = np.array([random.random() * 0.1 + 0.05,12.0/15.0])
        pos['C180'] = np.array([random.random() * 0.1 + 0.25,12.0/15.0])
        pos['C181trans9'] = np.array([random.random() * 0.1 + 0.45,12.0/15.0])
        pos['C181trans11'] = np.array([random.random() * 0.1 + 0.65,12.0/15.0])
        pos['C181cis9'] = np.array([random.random() * 0.1 + 0.05,11.0/15.0])
        pos['C181cis11'] = np.array([random.random() * 0.1 + 0.25,11.0/15.0])
        pos['C19cyc'] = np.array([random.random() * 0.1 + 0.45,11.0/15.0])
        pos['C220'] = np.array([random.random() * 0.1 + 0.65,11.0/15.0])
        pos['Anisotropie'] = np.array([random.random() * 0.15 + 0.05, 10.0 / 15.0])
        #pos['UFAdivSFA'] = np.array([random.random() * 0.15 + 0.3, 10.0 / 15.0])
        #pos['CFAdivSFA'] = np.array([random.random() * 0.15 + 0.55, 10.0 / 15.0])
        #pos['CFAdivUFA'] = np.array([random.random() * 0.15 + 0.8, 10.0 / 15.0])
        pos['UFCcentri'] = np.array([random.random() * 0.15 + 0.05, 9.0 / 15.0])
        pos['tpH07centri'] = np.array([random.random() * 0.15 + 0.3, 9.0 / 15.0])
        #pos['tpH07scentri'] = np.array([random.random() * 0.15 + 0.55, 9.0 / 15.0])
        #pos['tpH07spe2centri'] = np.array([random.random() * 0.15 + 0.85, 9.0 / 15.0])
        pos['UFCcong'] = np.array([random.random() * 0.15 + 0.05, 8.0 / 15.0])
        pos['tpH07cong'] = np.array([random.random() * 0.15 + 0.3, 8.0 / 15.0])
        #pos['tpH07scong'] = np.array([random.random() * 0.15 + 0.55, 8.0 / 15.0])
        #pos['tpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 8.0 / 15.0])
        #pos['dUFCcong'] = np.array([random.random() * 0.15 + 0.05, 7.0 / 15.0])
        #pos['dtpH07cong'] = np.array([random.random() * 0.15 + 0.3, 7.0 / 15.0])
        #pos['dtpH07scong'] = np.array([random.random() * 0.15 + 0.55, 7.0 / 15.0])
        #pos['dtpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 7.0 / 15.0])
        pos['UFClyo'] = np.array([random.random() * 0.15 + 0.05, 6.0 / 15.0])
        pos['TpH07lyo'] = np.array([random.random() * 0.15 + 0.2, 6.0 / 15.0])
        #pos['tpH07slyo'] = np.array([random.random() * 0.15 + 0.55, 6.0 / 15.0])
        #pos['tpH07spe2lyo'] = np.array([random.random() * 0.15 + 0.8, 6.0 / 15.0])
        #pos['dUFCdes'] = np.array([random.random() * 0.15 + 0.05, 5.0 / 15.0])
        #pos['dtpH07des'] = np.array([random.random() * 0.15 + 0.3, 5.0 / 15.0])
        #pos['dtpH07sdes'] = np.array([random.random() * 0.15 + 0.55, 5.0 / 15.0])
        #pos['dtpH07spe2des'] = np.array([random.random() * 0.15 + 0.8, 5.0 / 15.0])
        #pos['dtUFClyo'] = np.array([random.random() * 0.15 + 0.05, 4.0 / 15.0])
        #pos['dtpH07lyo'] = np.array([random.random() * 0.15 + 0.3, 4.0 / 15.0])
        #pos['dtpH07slyo'] = np.array([random.random() * 0.15 + 0.55, 4.0 / 15.0])
        #pos['dtpH07spe2lyo'] = np.array([random.random() * 0.15 + 0.8, 4.0 / 15.0])
        pos['UFCsto3'] = np.array([random.random() * 0.15 + 0.05, 3.0 / 15.0])
        pos['tpH07sto3'] = np.array([random.random() * 0.15 + 0.3, 3.0 / 15.0])
        #pos['tpH07ssto3'] = np.array([random.random() * 0.15 + 0.55, 3.0 / 15.0])
        #pos['tpH07spe2sto3'] = np.array([random.random() * 0.15 + 0.8, 3.0 / 15.0])
        #pos['dUFCsto3'] = np.array([random.random() * 0.15 + 0.05, 2.0 / 15.0])
        #pos['dtpH07sto3'] = np.array([random.random() * 0.15 + 0.3, 2.0 / 15.0])
        #pos['dtpH07ssto3'] = np.array([random.random() * 0.15 + 0.55, 2.0 / 15.0])
        #pos['dtpH07spe2sto3'] = np.array([random.random() * 0.15 + 0.8, 2.0 / 15.0])
        #pos['dUFCtot'] = np.array([random.random() * 0.15 + 0.05, 1.0 / 15.0])
        #pos['dtpH07tot'] = np.array([random.random() * 0.15 + 0.3, 1.0 / 15.0])
        #pos['dtpH07stot'] = np.array([random.random() * 0.15 + 0.55, 1.0 / 15.0])
        #pos['dtpH07spe2tot'] = np.array([random.random() * 0.15 + 0.8, 1.0 / 15.0])
        return pos

    def initGraph(self):
        self.G = nx.DiGraph()

        for v in self.varnames:
            self.G.add_node(v)
            self.labels[v] = v

        for i in range(len(self.adj_simple)):
            self.pareto.append([])
            for j in range(len(self.adj_simple[i])):
                self.pareto[i].append((self.equacolPO[np.ix_(
                    np.logical_and(self.equacolPO[:, 2] == self.varnames[i],
                                   self.equacolPO[:, 3] == self.varnames[j])), 0:2][0]).astype('float64'))

        for i in range(len(self.varnames)):
            if ((len(self.varnames) - np.sum(self.adj_contr, axis=0)[i]) != 0):
                self.nodeWeight.append(
                    np.sum(self.adj_simple, axis=0)[i] / (
                    len(self.varnames) - np.sum(self.adj_contr, axis=0)[i]))
            else:
                self.nodeWeight.append(0)
        for i in range(len(self.varnames)):
            self.nodeColor.append(
                (0.5, 0.5 + 0.5 * self.nodeWeight[i] / np.amax(self.nodeWeight), 0.5))


    def loadDataFile(self,datafile):
        # datadict ans self.mol_cell are dictionary lists.
        # Each dictionary represents the results for every variables of an experiment.
        dataset=genfromtxt(datafile, 'str', delimiter=',')
        datadict = []
        datafileReader = open(datafile)
        line = datafileReader.readline()  # First line are the variables name
        variables = []
        for i in line.split(','):
            variables.append(i.strip())
        line =  datafileReader.readline() # Second line is variables scale/step identifiers
        identvar = []
        for i in line.split(','):
            identvar.append(i.strip())

        for line in datafileReader:
            line = zip(variables, [float(i.strip()) for i in line.split(',')])
            datadict.append(dict(line))
        identvarDict={}
        for i in range(len(variables)):
            identvarDict[variables[i]]=identvar[i]

        return datadict,identvarDict,dataset

    def createConstraintsGraph(self):
        graph = nx.DiGraph()
        for i in np.unique(list(self.identvarDict.values())):
            print(i)
            graph.add_node(i)

        graph.add_edge('condition','Cell')
        graph.add_edge('Cell','PopCentri')
        graph.add_edge('Cell','PopCong')
        graph.add_edge('Cell','PopLyo')
        graph.add_edge('Cell','PopSto3')
        graph.add_edge('condition','PopCentri')
        graph.add_edge('condition','PopCong')
        graph.add_edge('condition','PopLyo')
        graph.add_edge('condition','PopSto3')
        graph.add_edge('PopCentri','PopCong')
        graph.add_edge('PopCentri','PopLyo')
        graph.add_edge('PopCentri','PopSto3')
        graph.add_edge('PopCong','PopLyo')
        graph.add_edge('PopCong', 'PopSto3')
        graph.add_edge('PopLyo','PopSto3')
        nx.draw(graph,with_labels=True)

        return graph


    def createConstraints(self):
        adj_contr=np.ones((self.nbVar,self.nbVar))
        for edge in self.adj_contrGraph.edges():
            for var1 in range(len(self.varnames)):
                for var2 in range(len(self.varnames)):
                    if(self.identvarDict[self.varnames[var1]]==edge[0] and self.identvarDict[self.varnames[var2]]==edge[1]):
                        adj_contr[var2][var1]-=1
        return adj_contr