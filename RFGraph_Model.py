#-*- coding: utf-8
import random
import matplotlib as mpl
import numpy as np
from numpy import genfromtxt
import copy
import networkx as nx
#nx.use('qt4agg')
from ArrayConverter import ArrayConverter
import re
import sys
sys.path.append("fitness/")
#from fitness import fitness
from fitness import Individual
import pandas as pd
from Dataset import Dataset
from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify
import pickle
from PyQt4.QtGui import *
import ColorMaps
from collections import OrderedDict
from sklearn import linear_model
from fitness import fitness
import logging

# TODO  Définie la position des noeuds et les initialise
class RFGraph_Model:

    def __init__(self):

        lfile = 'data/branchednormalizied.ldg'
        self.dataset=Dataset(lfile)
        logging.info("Loaded {}".format(lfile))
        self.adj_contrGraph = self.createConstraintsGraph()
        self.equacolO = self.findLassoEqs()
        self.nbequa = len(self.equacolO)  # Number of Equation for all variables taken together

        self.adj_simple=np.zeros((self.dataset.nbVar,self.dataset.nbVar))
        self.adj_fit=np.ones((self.dataset.nbVar,self.dataset.nbVar))
        self.adj_cmplx=np.ones((self.dataset.nbVar,self.dataset.nbVar))
        self.nbeq=np.zeros(self.dataset.nbVar) # Number of equations for each variables

        self.equacolPO=[]
        for l in range(self.nbequa):
            for h in range(self.dataset.nbVar):
                #Possible parents for the equations
                cont_h=len(re.findall(r'\b%s\b' % re.escape(self.dataset.varnames[h]),self.equacolO[l,3]))  #How many times the variable self.varname[h] is found in the equation self.equacolO[l,3]
                if(cont_h>0): #If present, add infos in adjacence matrix
                    ind_parent=h
                    ind_offspring=list(self.dataset.varnames).index(self.equacolO[l,2])
                    self.adj_simple[ind_offspring,ind_parent]+=1
                    self.adj_cmplx[ind_offspring,ind_parent]*=self.equacolO[l,0] #  GEOMETRIC mean
                    self.adj_fit[ind_offspring,ind_parent]*=self.equacolO[l,1] #  GEOMETRIC mean
                    self.equacolPO.append([self.equacolO[l,0],self.equacolO[l,1],self.equacolO[l,2],self.dataset.varnames[h],self.equacolO[l,3], self.equacolO[l,4]])
            self.nbeq[list(self.dataset.varnames).index(self.equacolO[l,2])]+=1 # Comptage du nombre d'équations pour chaque enfant

        #self.equacolPO=ArrayConverter.convertPO(self.equacolPO)
        self.equacolPO =np.array(self.equacolPO, dtype=object)
        self.adj_cmplx=np.power(self.adj_cmplx,1/self.adj_simple)
        self.adj_cmplx[self.adj_simple==0]=0
        self.adj_fit = np.power(self.adj_fit, 1 / self.adj_simple)
        self.adj_fit[self.adj_simple == 0] = 0


        self.adj_contr=self.createConstraints()

        #self.pos=self.pos_graph()
        self.pos = []
        self.varsIn = ["GECA24s00615g","GECA20s01396g","GECA09s03013g","KLLA0A10307g","HAAL_v1_70428","GECA12s03519g","GECA05s06643g","DEHA2F00792g","GECA12s00527g","GECA18s01209g","LALA_v1_830008","DEHA2G21032g","GECA15s00593g","KLLA0C12243g","GECA01s06874g","GECA02s02694g","KLLA0E19889g","GECA01s10493g","GECA09s00098g","KLLA0F00440g","GECA01s06104g","GECA20s00208g","GECA18s01803g","GECA01s04487g","KLLA0A02673g","KLLA0F22022g","KLLA0B12584g","GECA02s07072g","GECA11s00197g","GECA15s00373g","KLLA0C04774g","GECA32s02474g","GECA07s02430g","GECA10s00109g","KLLA0F12364g","KLLA0D10593g","GECA07s02870g","GECA19s01275g","DEHA2F09570g","GECA03s03733g","KLLA0C07777g","HAAL_v1_800100","KLLA0F15202g","CAJL_v1_250038","KLLA0F07073g","DEHA2G03740g","KLLA0B00451g","KLLA0D09999g","KLLA0A10791g","GECA08s02584g","GECA11s03343g","GECA19s01407g","CAFW_v1_410017","KLLA0C19382g","KLLA0F21010g","KLLA0E23057g"]
        self.NodeConstraints = []
        self.lastNodeClicked = None
        self.last_clicked = None
        self.mode_cntrt = False
        self.cntrt_FirstClick = ''
        self.cntrt_SecondClick = ''
        self.forbidden_edge = []
        self.curr_tabl=[]
        self.adjThresholdVal=0.0
        self.comprFitCmplxVal=0.5
        self.opt_params= []
        self.error_paramas= []
        self.help_params= []
        self.clicked_line=-1
        self.old_color=[]
        self.nodeColor = []
        self.edgeColor = []
        self.nodeWeight = []
        self.cmplxMin = np.amin(self.equacolO[:, 0])
        self.cmplxMax = np.amax(self.equacolO[:, 0])
        self.dataMaxFitness = np.amax(self.equacolO[:, 1])
        self.pareto = []
        self.scrolledList=[]
        self.scrolledList.append("Select link to reinstate")
        self.edgelist_inOrder = []
        self.edgeColor = []
        self.edgeColorCompr=[]
        self.edgeColorFit=[]
        self.edgeColorCmplx=[]
        self.ColorMode='Fit'
        self.transparentEdges=False
        self.edgeBoldfull=[]
        self.adj_cmplx_max = np.amax(self.adj_cmplx)
        self.best_indv=[]
        self.globalModelView = False
        self.selectedEq={}
        self.global_Edge_Color = []
        self.mode_changeEq=False
        self.colors = ColorMaps.colorm()
        self.radius=0.002
        self.lastHover=''
        self.fitCmplxPos={}
        self.fitCmplxfPos = {}
        self.fitCmplxlPos = {}
        self.rmByRmEq = []
        self.rmByRmEdge = []
        self.rmByRmNode = []
        self.invisibleTup = []
        self.forbiddenNodes = []
        self.nodesWithNoEquations=[]

        self.data = []

        for i in range(len(self.equacolO)):
            self.data.append(self.equacolO[i, np.ix_([0, 1, 3, 4])][0])

        self.labels = {}
        self.edges = None

        self.varEquasize=OrderedDict(list(zip(self.dataset.varnames,self.nbeq)))
        self.varEquasizeOnlyTrue=self.varEquasize.copy()
        self.computeEquaPerNode()

        ##########################
        #self.datumIncMat = pd.read_csv("data/equa_with_col_Parent_withMol.csv", header=None)
        #self.datumIncMat = self.datumIncMat.sort(2)
        self.datumIncMat=pd.DataFrame(self.equacolO)

        self.df_IncMat = pd.DataFrame(index=self.datumIncMat[2], columns=self.varsIn + self.datumIncMat[2].unique().tolist())
        for row in range(self.df_IncMat.shape[0]):
            v = self.df_IncMat.index.values[row]
            self.df_IncMat.ix[row] = self.getV(self.df_IncMat.columns.values, self.datumIncMat.iloc[row][3], v)

        self.dataIncMat = self.df_IncMat
        self.shapeIncMat = self.dataIncMat.shape

        #self.dataIncMat.to_csv('debugMat.csv',header = True, index = True)

        ##########################



        self.initGraph()


    def findLassoEqs(self):
        equacolOtmp=[]
        for i in range(len(self.dataset.varnames)):
            print('computing : ' + self.dataset.varnames[i])
            iClass = self.dataset.variablesClass[self.dataset.varnames[i]]
            if(iClass!='gene'): #TODO generalize
                parIClass=[]
                for (e1,e2) in self.adj_contrGraph.edges():
                    if(e2 ==iClass and not e1 in parIClass):
                        parIClass.append(e1)
                #parIClass=list(self.adj_contrGraph.edge[iClass].keys())
                par=[]
                for v in self.dataset.varnames:
                    if(self.dataset.variablesClass[v] in parIClass):
                        par.append(v)
                Y = list(self.dataset.data[:, i])
                X=[]

                idx=[list(self.dataset.varnames).index(v) for v in par]
                X=self.dataset.data[:,idx]

                params = [(0.5, True),(0.05, False),(0.01, False), (0.005,False),(0.001,False)]
                for a,f in params:#[0.5,0.05,0.01, 0.005,0.001]:
                    clf = linear_model.Lasso(alpha=a, fit_intercept = f)
                    clf.fit(X, Y)
                    pred=clf.predict(X)

                    equacolOtmp.extend(self.regrToEquaColO(clf,par,self.dataset.varnames[i],Y,pred))

        equacolOtmp = np.array(equacolOtmp, dtype=object)
        equacolOtmp = equacolOtmp.reshape(len(equacolOtmp)/5,5) #TODO int()


        return equacolOtmp

    def regrToEquaColO(self,clf,parNode,childNode,Y,pred):
        line=[]
        s=''
        cmplx = 0
        hasCoef=False


        for i in range(len(parNode)):
            if(clf.coef_[i] > 0  ):
                hasCoef=True
                s += ' + ' + str(clf.coef_[i]) + ' * ' + parNode[i] + ' '
                cmplx += 3
            elif(clf.coef_[i] < 0 ):
                hasCoef=True
                s +=  str(clf.coef_[i]) + ' * ' + parNode[i] + ' '
                cmplx += 3

        if (clf.intercept_ != 0 and hasCoef):
            s = str(clf.intercept_) + ' ' + s
            cmplx += 2;

        if (clf.intercept_ != 0 and not hasCoef):
            s += str(clf.intercept_)
            cmplx += 1;

        fit=fitness(Y,pred)

        line.append(cmplx)
        line.append(fit)
        line.append(childNode)
        line.append(s)
        line.append(True)



        return line

    def computeEquaPerNode(self):
        self.equaPerNode = {}
        for v in self.dataset.varnames:
            if (not v in self.varsIn):
                self.equaPerNode[v] = self.equacolO[np.ix_(self.equacolO[:, 2] == [v], [0, 1, 2, 3, 4])]

    def readEureqaResults(self,file):
        #Read eureqa file
        stringTab=[]
        eureqafile = open(file, 'r')
        for line in eureqafile:
            line = line.replace("\t", ",")
            line=line.replace("\"","")
            line=line.replace(" = ",",")
            #line=line.replace(" ","")
            line=line.replace("*"," * ")
            line=line.replace("/"," / ")
            line=line.replace("("," ( ")
            line = line.replace(")", " ) ")
            line=line.replace("\n","")
            line=line.split(',')
            stringTab.append(line)

        #Convert the table of String to a nice table with float and String
        convertArr = []
        for s in stringTab:
            convertArr.append(np.float32(s[0]))
            #xr=self.dataset.getAllExpsforVar(s[2])
            #yr=[]
            #for numExp in range(self.dataset.nbExp):
            #    yr.append(parse_expr(s[3], local_dict=self.dataset.getAllVarsforExp(numExp)))
            #try:
            #    recomputedFitness=fitness(xr,yr)
            #except:
            #    pass
            convertArr.append(np.float32(s[1]))
            #convertArr.append(recomputedFitness)
            convertArr.append(s[2])
            convertArr.append(s[3])
            convertArr.append(True)
            #convertArr.append(sympify(s[3]))


        finalTab = np.array(convertArr, dtype=object)
        shp = np.shape(stringTab)
        finalTab = finalTab.reshape((shp[0], shp[1] + 1))
        return finalTab

    def getV(self,variables, line, v):
        table = []
        for i in variables:
            # g = "\W"+i+"\W"
            # if re.search(g, line):
            if (re.findall(r'\b%s\b' % re.escape(i), line)):
                # if i in line:
                table.append(1)
            elif v == i:
                table.append(-1)
            else:
                table.append(0)
        # print(v)
        # print(table)
        return table

    def pos_graph(self):
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
        pos['C140'] = np.array([random.random() * 0.15 + 0.05,9.0/15.0])
        pos['C150'] = np.array([random.random() * 0.15 + 0.30,9.0/15.0])
        pos['C160'] = np.array([random.random() * 0.15 + 0.55,9.0/15.0])
        pos['C161cis'] = np.array([random.random() * 0.15 + 0.80,9.0/15.0])
        pos['C170'] = np.array([random.random() * 0.15 + 0.05,8.0/15.0])
        pos['C180'] = np.array([random.random() * 0.15 + 0.30,8.0/15.0])
        pos['C181trans'] = np.array([random.random() * 0.15 + 0.55,8.0/15.0])
        pos['C181trans11'] = np.array([random.random() * 0.15 + 0.80,8.0/15.0])
        pos['C181cis'] = np.array([random.random() * 0.1 + 0.05,7.0/15.0])
        pos['C181cis11'] = np.array([random.random() * 0.1 + 0.25,7.0/15.0])
        pos['C19cyc'] = np.array([random.random() * 0.1 + 0.45,7.0/15.0])
        pos['C220'] = np.array([random.random() * 0.1 + 0.65,7.0/15.0])
        pos['Anisotropie'] = np.array([random.random() * 0.1 + 0.85, 7.0 / 15.0])
        #pos['UFAdivSFA'] = np.array([random.random() * 0.15 + 0.3, 10.0 / 15.0])
        #pos['CFAdivSFA'] = np.array([random.random() * 0.15 + 0.55, 10.0 / 15.0])
        #pos['CFAdivUFA'] = np.array([random.random() * 0.15 + 0.8, 10.0 / 15.0])
        pos['UFCcentri'] = np.array([random.random() * 0.2 + 0.15, 4.0 / 15.0])
        pos['tpH07centri'] = np.array([random.random() * 0.2 + 0.65, 4.0 / 15.0])
        #pos['tpH07scentri'] = np.array([random.random() * 0.15 + 0.55, 9.0 / 15.0])
        #pos['tpH07spe2centri'] = np.array([random.random() * 0.15 + 0.85, 9.0 / 15.0])
        pos['UFCcong'] = np.array([random.random() * 0.2 + 0.15, 3.00 / 15.0])
        pos['tpH07cong'] = np.array([random.random() * 0.2 + 0.65, 3.0 / 15.0])
        #pos['tpH07scong'] = np.array([random.random() * 0.15 + 0.55, 8.0 / 15.0])
        #pos['tpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 8.0 / 15.0])
        #pos['dUFCcong'] = np.array([random.random() * 0.15 + 0.05, 7.0 / 15.0])
        #pos['dtpH07cong'] = np.array([random.random() * 0.15 + 0.3, 7.0 / 15.0])
        #pos['dtpH07scong'] = np.array([random.random() * 0.15 + 0.55, 7.0 / 15.0])
        #pos['dtpH07spe2cong'] = np.array([random.random() * 0.15 + 0.8, 7.0 / 15.0])
        pos['UFClyo'] = np.array([random.random() * 0.2 + 0.15, 2.0 / 15.0])
        pos['TpH07lyo'] = np.array([random.random() * 0.2 + 0.65, 2.0 / 15.0])
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
        pos['UFCsto3'] = np.array([random.random() * 0.2 + 0.15, 1.0 / 15.0])
        pos['tpH07sto3'] = np.array([random.random() * 0.2 + 0.65, 1.0 / 15.0])
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

        for v in self.dataset.varnames:
            self.G.add_node(v)
            self.labels[v] = v

        for i in range(len(self.adj_simple)):
            self.pareto.append([])
            for j in range(len(self.adj_simple[i])):
                self.pareto[i].append((self.equacolPO[np.ix_(
                    np.logical_and(self.equacolPO[:, 2] == self.dataset.varnames[i],
                                   self.equacolPO[:, 3] == self.dataset.varnames[j])), 0:2][0]).astype('float64'))

        for i in range(len(self.dataset.varnames)):
            if ((len(self.dataset.varnames) - np.sum(self.adj_contr, axis=0)[i]) != 0):
                self.nodeWeight.append(
                    np.sum(self.adj_simple, axis=0)[i] / (
                    len(self.dataset.varnames) - np.sum(self.adj_contr, axis=0)[i]))
            else:
                self.nodeWeight.append(0)
        for i in range(len(self.dataset.varnames)):
            #self.nodeColor.append((0.5, 0.5 + 0.5 * self.nodeWeight[i] / np.amax(self.nodeWeight), 0.5))
            #if(self.dataset.varnames[i])
            #self.
            #TODO generalize
            if(self.dataset.variablesClass[self.dataset.varnames[i]]== 'gene'):
                self.nodeColor.append((0.5, 0.5, 0.9))
            if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'ester'):
                self.nodeColor.append((0.9, 0.55, 0.55))
            if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'alcohol'):#CellAniso
                self.nodeColor.append((0.3, 0.9, 0.9))
            if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'aldehyde'):
                self.nodeColor.append((0.7, 0.7, 0.5))
            if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'other'):
                self.nodeColor.append((0.8, 0.8, 0.2))

        self.computeInitialPos()
        self.computeFitandCmplxEdgeColor()
        self.computeComprEdgeColor()

        self.computeNxGraph()



    def createConstraintsGraph(self):
        graph = nx.DiGraph()
        for i in np.unique(list(self.dataset.variablesClass.values())):
#            print(i)
            graph.add_node(i)
        graph.add_edge("gene",'alcohol')
        graph.add_edge('gene', 'aldehyde') #TODO Generalize
        graph.add_edge('gene','other')
        graph.add_edge('gene','ester')
        graph.add_edge('aldehyde', 'alcohol')


        #nx.draw(graph,with_labels=True)

        return graph

    def createConstraints(self):
        adj_contr=np.ones((self.dataset.nbVar,self.dataset.nbVar))
        for edge in self.adj_contrGraph.edges():
            for var1 in range(len(self.dataset.varnames)):
                for var2 in range(len(self.dataset.varnames)):
                    if(self.dataset.variablesClass[self.dataset.varnames[var1]]==edge[0] and self.dataset.variablesClass[self.dataset.varnames[var2]]==edge[1]):
                        adj_contr[var2][var1]-=1
        return adj_contr

    # def computeBoldNodes(self):
    #
    #     self.edgelist_inOrder = []
    #     self.edgeBold = []
    #
    #     for i in range(len(self.pareto)):  # i is child
    #         for j in range(len(self.pareto[i])):  # j is parent
    #             lIdxColPareto = self.pareto[i][j]
    #             if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
    #                 #if self.nbeq[i] == np.float64(0.0): continue
    #                 r = self.adj_simple[i, j] / self.nbeq[
    #                     i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
    #                 if (r > self.adjThresholdVal):
    #
    #                     self.edgelist_inOrder.append((self.data.varnames[j], self.data.varnames[i]))
    #
    #                     if (self.lastNodeClicked == self.data.varnames[i]):
    #                         self.edgeBold.append(True)
    #                     else:
    #                         self.edgeBold.append(False)
    #
    #
    #                 n1 = self.data.varnames[i] + ' - ' + self.data.varnames[j]
    #                 n2 = self.data.varnames[j] + ' - ' + self.data.varnames[i]
    #                 allItems = [self.scrolledList[i] for i in range(len(self.scrolledList))]
    #                 if n1 in allItems or n2 in allItems:
    #                     try:
    #                         index = self.edgelist_inOrder.index((self.data.varnames[i], self.data.varnames[j]))
    #                     except:
    #                         index = self.edgelist_inOrder.index((self.data.varnames[j], self.data.varnames[i]))
    #                     self.edgelist_inOrder.pop(index)



    def removeForbiddenEdges(self):
        self.forbiddenEdges = []
        for i in range(len(self.pareto)):  # i is child
            for j in range(len(self.pareto[i])):  # j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto

                    n1 = self.dataset.varnames[i] + ' - ' + self.dataset.varnames[j]
                    n2 = self.dataset.varnames[j] + ' - ' + self.dataset.varnames[i]
                    allItems = [self.scrolledList[i] for i in range(len(self.scrolledList))]
                    if n1 in allItems or n2 in allItems:
                        try:
                            index = self.edgelist_inOrder.index((self.dataset.varnames[i], self.dataset.varnames[j]))
                        except:
                            index = self.edgelist_inOrder.index((self.dataset.varnames[j], self.dataset.varnames[i]))
                        if(not self.edgelist_inOrder[index] in self.forbidden_edge):
                            self.forbidden_edge.append(self.edgelist_inOrder[index])
                        #self.edgelist_inOrder.pop(index)
                        #self.edgeBold.pop(index)
                        #self.edgeColor.pop(index)


    def removeInvisibleEdges(self):
        self.invisibleTup = []

        self.edgeBoldDict=copy.deepcopy(self.edgeBoldfull)
        if (self.ColorMode == 'Compr'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorCompr)
        elif (self.ColorMode == 'Fit'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorFit)
        elif (self.ColorMode == 'Cmplx'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorCmplx)
        for i in range(len(self.pareto)):  # i is child
            for j in range(len(self.pareto[i])):  # j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    # if self.nbeq[i] == np.float64(0.0): continue
                    r = self.adj_simple[i, j] / self.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                    if (r <= self.adjThresholdVal):
                        tup = (self.dataset.varnames[j], self.dataset.varnames[i])
                        self.invisibleTup.append(tup)
                        #try:
                        #    del (self.edgeBoldDict[tup])
                        #except:
                        #    pass
                        #try:
                        #    del (self.edgeColorfull[tup])
                        #except:
                        #    pass

        self.edgeColor = self.colorDictToConstraintedcolorList(self.edgeColorfull,self.edgelist_inOrder)
        self.edgeBold = self.colorDictToConstraintedcolorList(self.edgeBoldDict,self.edgelist_inOrder)


    def computeNxGraph(self):
        self.G.clear()
        for v in self.dataset.varnames:
            self.G.add_node(v)

        self.nodesWithNoEquations=[]

        self.edgelist_inOrder = []

        for i in range(len(self.pareto)):#i is child
            for j in range(len(self.pareto[i])): #j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto

                    #if self.nbeq[i] == np.float64(0.0): continue
                    r = self.adj_simple[i, j] / self.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                    #if (r > self.adjThresholdVal):
                    self.G.add_edge(self.dataset.varnames[j], self.dataset.varnames[i],
                                           adjsimple=self.adj_simple[i, j], adjfit=
                                           self.adj_fit[i, j], adjcmplx=self.adj_cmplx[i, j],
                                           adjcontr=self.adj_contr[i, j])
                    self.edgelist_inOrder.append((self.dataset.varnames[j], self.dataset.varnames[i]))

        for v in self.dataset.varnames.tolist():
            if not v in self.varsIn:
                ix = np.ix_(self.equacolO[:, 2] == v)
                if(not True in self.equacolO[ix[0], 4] and not v in self.forbiddenNodes):
                    self.nodesWithNoEquations.append(v)

        self.computeEdgeBold()
        self.removeInvisibleEdges()
        self.removeForbiddenEdges()


    def colorDictToConstraintedcolorList(self,colorDict,edgesToShow):
        colorList=[]
        for edge in edgesToShow:
            try:
                colorList.append(colorDict[edge])
            except:
                pass
        return colorList

    def computeEdgeBold(self):

        self.edgeBoldfull = {}

        #for i in range(len(self.pareto)):  # i is child
        #    for j in range(len(self.pareto[i])):  # j is parent
        #        lIdxColPareto = self.pareto[i][j]
        #        if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    #if self.nbeq[i] == np.float64(0.0): continue
        for (x, y) in self.edgelist_inOrder:
            if (self.lastNodeClicked == x or self.lastNodeClicked == y):
                self.edgeBoldfull[(x,y)]=True
            else:
                self.edgeBoldfull[(x, y)]=False

    def computeComprEdgeColor(self):

        self.edgeColorCompr = {}

        for i in range(len(self.pareto)):  # i is child
            for j in range(len(self.pareto[i])):  # j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto

                    lIdxColPareto[:, 0] = (lIdxColPareto[:, 0] - self.cmplxMin) / (
                        self.cmplxMax - self.cmplxMin)  # Normalisation de la complexité
                    dist_lIdxColPareto = np.sqrt(
                        np.power(np.cos(self.comprFitCmplxVal * (np.pi / 2)) * lIdxColPareto[:, 0], 2) +
                        np.power(np.sin(self.comprFitCmplxVal * (np.pi / 2)) * lIdxColPareto[:, 1], 2))

                    dist_lIdxColPareto_idxMin = np.argmin(
                        dist_lIdxColPareto)  # Indice dans dist_lIdxColPareto correspondant au meilleur compromi
                    dist_lIdxColPareto_valMin = dist_lIdxColPareto[
                        dist_lIdxColPareto_idxMin]  # Distance meilleur compromi
                    #if self.nbeq[i] == np.float64(0.0): continue
                    r = self.adj_simple[i, j] / self.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i

                    #cdict1 = {'red': ((0.0, 0.0, 0.0),
                    #                  (0.5, 0.0, 0.0),
                    #                  (1.0, 0.0, 0.0)),
                    #          'green': ((0.0, 0.0, 0.0),
                    #                    (0.0, 0.5, 0.0),
                    #                    (0.0, 1.0, 0.0)),
                    #          'blue': ((0.0, 0.0, 0.5),
                    #                   (0.0, 0.0, 0.5),
                    #                   (0.0, 0.0, 0.5))
                    #          }
                    #cmap = mpl.colors.ListedColormap(["red", "grey", "green"], name='from_list')
                    #mycmap=mpl.colors.LinearSegmentedColormap('CustomMap', cdict1)
                    #m = mpl.cm.ScalarMappable(norm=[0,1], cmap=mycmap)

                    if(dist_lIdxColPareto_valMin<0.5):
                        cr = dist_lIdxColPareto_valMin
                        cg = 1-dist_lIdxColPareto_valMin
                        cb = dist_lIdxColPareto_valMin
                    else:
                        cr = dist_lIdxColPareto_valMin
                        cg = 1 - dist_lIdxColPareto_valMin
                        cb = 1 - dist_lIdxColPareto_valMin
                        #cr = np.minimum(dist_lIdxColPareto_valMin * 2, 1)
                        #cg = np.minimum((1 - dist_lIdxColPareto_valMin) * 2, 1)
                        #cb = 0

                    if (self.transparentEdges):
                        self.edgeColorCompr[(self.dataset.varnames[j], self.dataset.varnames[i])]=[cr + (1 - cr) * (1 - r), cg + (1 - cg) * (1 - r), cb + (1 - cb) * (1 - r)]
                    else:
                        self.edgeColorCompr[(self.dataset.varnames[j], self.dataset.varnames[i])]=[cr, cg, cb]

    def computeFitandCmplxEdgeColor(self):
        self.edgeColorFit = {}
        self.edgeColorCmplx = {}

        for i in range(len(self.pareto)):  # i is child
            for j in range(len(self.pareto[i])):  # j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    if (self.adj_fit[i, j] == 0):
                        raise Exception('Error on fit color')
                    if (self.adj_cmplx[i, j] == 0):
                        raise Exception('Error on cmplx color')

                    #if self.nbeq[i] == np.float64(0.0): continue

                    cr = np.minimum(self.adj_fit[i, j] * 2, 1)
                    cg = np.minimum((1 - self.adj_fit[i, j]) * 2, 1)
                    cb = 0
                    if (self.transparentEdges):
                        self.edgeColorFit[(self.dataset.varnames[j], self.dataset.varnames[i])]=[cr + (1 - cr) * (1 - r), cg + (1 - cg) * (1 - r), cb + (1 - cb) * (1 - r),1]
                    else:
                        cmap = self.colors.get("local",self.adj_fit[i, j])
                        #color = QColor.fromRgb(*cmap)
                        lcmap=list(np.array(cmap)/255)
                        lcmap.extend([1.0])
                        self.edgeColorFit[(self.dataset.varnames[j], self.dataset.varnames[i])]= lcmap  #(cr, cg, cb)
                    cr = np.minimum((self.adj_cmplx[i, j] / self.adj_cmplx_max) * 2, 1)
                    cg = np.minimum((1 - (self.adj_cmplx[i, j] / self.adj_cmplx_max)) * 2, 1)
                    cb = 0
                    if (self.transparentEdges):
                        self.edgeColorCmplx[(self.dataset.varnames[j], self.dataset.varnames[i])]=[cr + (1 - cr) * (1 - r), cg + (1 - cg) * (1 - r), cb + (1 - cb) * (1 - r),1]
                    else:
                        cmap = self.colors.get("complexity", self.adj_cmplx[i, j]/self.cmplxMax)
                        #color = QColor.fromRgb(*cmap)
                        lcmap = list(np.array(cmap) / 255)
                        lcmap.extend([1.0])
                        self.edgeColorCmplx[(self.dataset.varnames[j], self.dataset.varnames[i])]=lcmap

    def computeInitialPos(self):
        G=nx.DiGraph()
        G.clear()
        for v in self.dataset.varnames:
            G.add_node(v)

        for i in range(len(self.pareto)):
            for j in range(len(self.pareto[i])):
                #lIdxColPareto = self.pareto[i][j]
                #if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    #if self.nbeq[i] == np.float64(0.0): continue
                    if self.adj_contrGraph.has_edge(self.dataset.variablesClass[self.dataset.varnames[j]], self.dataset.variablesClass[self.dataset.varnames[i]]):
#                        print(self.dataset.varnames[j] + " --> " + self.dataset.varnames[i] + " : " + self.dataset.variablesClass[self.dataset.varnames[j]] + " --> " + self.dataset.variablesClass[self.dataset.varnames[i]])
                        G.add_edge(self.dataset.varnames[j], self.dataset.varnames[i],
                                        adjsimple=self.adj_simple[i, j], adjfit=
                                        self.adj_fit[i, j], adjcmplx=self.adj_cmplx[i, j],
                                        adjcontr=self.adj_contr[i, j])

        #with open('initpos.dat', 'rb') as f:
            #self.pos=pickle.load(f)
        self.pos = nx.nx_pydot.graphviz_layout(G, prog='sfdp')
        #self.pos = nx.spectral_layout(G)

        minx = np.inf
        maxx = -np.inf
        miny = np.inf
        maxy = -np.inf
        for k, p in list(self.pos.items()):
            if (minx > p[0]):
                minx = p[0]
            if (maxx < p[0]):
                maxx = p[0]
            if (miny > p[1]):
                miny = p[1]
            if (maxy < p[1]):
                maxy = p[1]
        for k in self.pos:
            self.pos[k] = ((self.pos[k][0] - minx) / (maxx - minx), (self.pos[k][1] - miny) / (maxy - miny))
#            print(k +" : (" + str(self.pos[k][0]) + ","+str(self.pos[k][1])+")")

        self.lpos = copy.deepcopy(self.pos)
        for p in self.lpos:  # raise text positions
            self.lpos[p] = (self.lpos[p][0], self.lpos[p][1] + 0.04)

        self.fpos = copy.deepcopy(self.pos)
        for p in self.fpos:
            self.fpos[p] = (self.fpos[p][0], self.fpos[p][1] - 0.04)



    def computeGlobalNxGraph(self):
        self.G.clear()
        for v in self.dataset.varnames:
            self.G.add_node(v)

        self.edgelist_inOrder = []

        for i in range(len(self.pareto)):  # i is child
            for j in range(len(self.pareto[i])):  # j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto

                    # if self.nbeq[i] == np.float64(0.0): continue
                    r = self.adj_simple[i, j] / self.nbeq[
                        i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                    if (r > self.adjThresholdVal):
                        self.G.add_edge(self.dataset.varnames[j], self.dataset.varnames[i],
                                        adjsimple=self.adj_simple[i, j], adjfit=
                                        self.adj_fit[i, j], adjcmplx=self.adj_cmplx[i, j],
                                        adjcontr=self.adj_contr[i, j])
                        self.edgelist_inOrder.append((self.dataset.varnames[j], self.dataset.varnames[i]))
        self.computeEdgeBold()
        self.removeInvisibleEdges()
        self.removeForbiddenEdges()

    def bestindvToSelectedEq(self):
        self.selectedEq = {}
        for v in self.dataset.varnames:
            try:
                self.selectedEq[v] = self.best_indv[v]
            except:
                pass
    def computeGlobalView(self):

        ft = Individual(self)
        res=ft.get_fitness(self.selectedEq)
        self.globErrDet=copy.deepcopy(res[2])
        self.GlobErr=res[0]#np.sum(list(self.globErr.values()))
        self.globErrLab = copy.deepcopy(res[2])
        for k in self.globErrLab.keys():
            self.globErrLab[k] = "{0:.2f}".format(self.globErrDet[k])

        equaLines=[]

        for v in self.selectedEq.keys():
            if(not v in self.varsIn):
                equaLines.append(self.equaPerNode[v][self.selectedEq[v]])
        self.edgelist_inOrder = []
        self.global_Edge_Color = []
        for l in range(len(equaLines)):
            for h in range(self.dataset.nbVar):  # Possible parents for the equations
                cont_h = len(re.findall(r'\b%s\b' % re.escape(self.dataset.varnames[h]), equaLines[l][3]))  # How many times the variable self.varname[h] is found in the equation self.
                if (cont_h > 0):
                    self.G.add_edge(self.dataset.varnames[h], equaLines[l][2])
                    self.edgelist_inOrder.append((self.dataset.varnames[h], equaLines[l][2]))
        err_max=-np.inf
        for (h, l) in self.edgelist_inOrder:
            err_max = np.maximum(res[2][l],err_max)

        for (h, l) in self.edgelist_inOrder:
            err_coef= res[2][l]/err_max
#            print(res[2][l])


            cr = np.maximum(np.minimum(err_coef * 2, 1),0)
            cg = np.maximum(np.minimum((1 - err_coef) * 2, 1),0)
            cb = 0
            self.global_Edge_Color.append([cr,cg,cb,1.0])
        pass

        maxcmplx=max(list(res[3].values()))
        for v in self.dataset.varnames:
            if(v in self.varsIn):
                self.fitCmplxPos[v] = (0,0)
            else:
                self.fitCmplxPos[v] = (res[2][v], res[3][v]/maxcmplx)


        self.fitCmplxlPos= dict(list(map(lambda x: (x[0], (x[1][0] + 0.04, x[1][1] + 0.04)), list(self.fitCmplxPos.items()))))
        self.fitCmplxfPos = dict(list(map(lambda x: (x[0], (x[1][0] - 0.04, x[1][1] - 0.04)), list(self.fitCmplxPos.items()))))
        #self.fitCmplxlPos = 0
        #self.pos=self.fitCmplxPos
        #self.fpos=self.fitCmplxfPos
        #self.lpos=self.fitCmplxlPos

