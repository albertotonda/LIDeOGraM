#-*- coding: utf-8
import copy
import random
import re
import sys

import networkx as nx
import numpy as np

#sys.path.append("fitness/")
sys.path.append('SALib/SaLib-master')
from SALib.analyze import sobol
from SALib.sample import saltelli
from scipy.stats.stats import pearsonr
from equaOptim import equaOptim
from fitness import Individual
import pandas as pd
from Dataset import Dataset
from sympy.parsing.sympy_parser import parse_expr
import ColorMaps
from collections import OrderedDict
from sklearn import linear_model
from fitness import fitness
from classes.ClassGraph import ClassGraph
from classes.ClassNode import ClassNode
from classes.WindowClasses import WindowClasses
from RFGraph_View import RFGraph_View
from RFGraph_Controller import RFGraph_Controller
from QtConnector import QtConnector
from PyQt4 import QtGui
import logging
from time import strftime
import pandas


# TODO  Définie la position des noeuds et les initialise
class RFGraph_Model(QtGui.QMainWindow):

    def __init__(self):
        logging.basicConfig(filename=strftime("lastlog")+'.log', level=logging.DEBUG)
        logging.info("Program started -- {}".format(strftime("%d %m %y: %H %M %S")))

        QtGui.QMainWindow.__init__(self) #Only for the progress bar

        datafile =  QtGui.QFileDialog.getOpenFileName(self, caption="Load a datafile",directory="data", filter="Datafile (*.csv)")
        #datafile = "data/dataset_mol_cell_pop_nocalc_sursousexpr_expertcorrected_incert_ifset_bolotin_2_nooutlier.csv"

        #datafile = "data/Classeur1.csv"

        self.dataset = Dataset(datafile)
       # self.trueture = Dataset("data/ballon_clean_no_noise.csv")
        #self.dataset = Dataset("data/use_case.mld")
        self.regressionType = 'OMP'  # 'OMP' or 'EA'
        logging.info("Data file {} -- {}".format(datafile, strftime("%d %m %y: %H %M %S")))
        self.createConstraintsGraph()
        self.firstInit = True



    def init2(self, contrgraph):

        self.adj_contrGraph = contrgraph
        self.adj_contrGraph.edgesTrueName = []
        for (e0, e1) in self.adj_contrGraph.edges():
            self.adj_contrGraph.edgesTrueName.append((e0.name, e1.name))
        self.correctDataset(self.dataset, self.adj_contrGraph)

        self.equacolO = self.findLassoEqs()

        #self.equacolO = self.readEureqaResults('data/eq_erqa4.txt')
        self.nbequa = len(self.equacolO)  # Number of Equation for all variables taken together

        self.adj_simple = np.zeros((self.dataset.nbVar,self.dataset.nbVar))
        self.adj_fit = np.ones((self.dataset.nbVar,self.dataset.nbVar))
        self.adj_cmplx = np.ones((self.dataset.nbVar,self.dataset.nbVar))
        self.nbeq = np.zeros(self.dataset.nbVar) # Number of equations for each variables

        self.equacolPO = []
        for l in range(self.nbequa):
            for h in range(self.dataset.nbVar):
                #Possible parents for the equations
                try:
                    cont_h = len(re.findall(r'\b%s\b' % re.escape(self.dataset.varnames[h]),self.equacolO[l,3]))  #How many times the variable self.varname[h] is found in the equation self.equacolO[l,3]
                    cont_h = cont_h+len(re.findall(r'\b%s\b' % re.escape(self.dataset.varnames[h]+"^2"), self.equacolO[l, 3]))


                except:
                    pass
                if cont_h>0: #If present, add infos in adjacence matrix
                    ind_parent=h
                    ind_offspring=list(self.dataset.varnames).index(self.equacolO[l,2])
                    self.adj_simple[ind_offspring,ind_parent]+=1
                    self.adj_cmplx[ind_offspring,ind_parent]*=self.equacolO[l,0] #  GEOMETRIC mean
                    if self.equacolO[l,1] != 0:
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
        #self.adj_simple = genfromtxt('data/adj_simple_withMol.csv', delimiter=',')
        #self.adj_cmplx = genfromtxt('data/adj_cmplx_withMol.csv', delimiter=',')
        #self.adj_fit = genfromtxt('data/adj_fit_withMol.csv', delimiter=',')
        #self.adj_contr = genfromtxt('data/adj_contraintes_withMol.csv', delimiter=',')
        #self.dataset.varnames = genfromtxt('data/varnames_withMol.csv', dtype='str', delimiter=',')
        #self.nbeq = genfromtxt('data/nbeq_withMol.csv', delimiter=',')
        #self.equacolPOf = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv', 'float', delimiter=',')
        #self.equacolPOs = genfromtxt('data/equa_with_col_ParentOffspring_withMol.csv', 'str', delimiter=',')
        #self.equacolOf = genfromtxt('data/equa_with_col_Parent_withMol.csv', 'float', delimiter=',')
        #self.equacolOs = genfromtxt('data/equa_with_col_Parent_withMol.csv', 'str', delimiter=',')
        #self.datasetset_cell_popS = genfromtxt('data/dataset_cell_pop.csv', 'str', delimiter=',')
        #self.datasetset_mol_cellS = genfromtxt('data/dataset_mol_cell.csv', 'str', delimiter=',')
        #self.datasetset_cell_popF = genfromtxt('data/dataset_cell_pop.csv', 'float', delimiter=',')
        #self.datasetset_mol_cellF = genfromtxt('data/dataset_mol_cell.csv', 'float', delimiter=',')
        #self.varsIn = ['Temperature','Age','AMACBIOSYNTHsousexpr','BIOSYNTH_CARRIERSsousexpr','CELLENVELOPEsousexpr','CELLPROCESSESsousexpr','CENTRINTMETABOsousexpr','ENMETABOsousexpr','FATTYACIDMETABOsousexpr','Hypoprotsousexpr','OTHERCATsousexpr','PURINESsousexpr','REGULFUNsousexpr','REPLICATIONsousexpr','TRANSCRIPTIONsousexpr','TRANSLATIONsousexpr','TRANSPORTPROTEINSsousexpr','AMACBIOSYNTHsurexpr','BIOSYNTH_CARRIERSsurexpr','CELLENVELOPEsurexpr','CELLPROCESSESsurexpr','CENTRINTMETABOsurexpr','ENMETABOsurexpr','FATTYACIDMETABOsurexpr','Hypoprotsurexpr','OTHERCATsurexpr','PURINESsurexpr','REGULFUNsurexpr','REPLICATIONsurexpr','TRANSCRIPTIONsurexpr','TRANSLATIONsurexpr','TRANSPORTPROTEINSsurexpr']
        self.varsIn = self.dataset.varsIn
        self.NodeConstraints = []
        self.lastNodeClicked = None
        self.last_clicked = None
        self.mode_cntrt = False
        self.cntrt_FirstClick = ''
        self.cntrt_SecondClick = ''
        self.forbidden_edge = []
        self.curr_tabl=[]
        self.adjThresholdVal=0.0
        self.comprFitCmplxVal=0.0
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
        self.edgeColorCompr=[]
        self.edgeColorFit=[]
        self.edgeColorCmplx=[]
        self.ColorMode='Fit'
        self.transparentEdges=False
        self.edgeBoldfull=[]
        self.adj_cmplx_max = np.amax(self.adj_cmplx)
        self.best_indv={}
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
        self.eqButton=-1


        #Necessaire de faire une deepcopy ?
        #self.lpos= copy.deepcopy(self.pos)
        #for p in self.lpos:  # raise text positions
        # self.modApp.lpos[p] = (self.modApp.lpos[p][0],self.modApp.lpos[p][1]+0.04)
        #    self.lpos[p][1] +=0.04

        # Charge la base de données d'équations à afficher après chargement
        # TODO: Base de données d'équations à changer


        self.data = []

        #self.dataMaxComplexity = self.cmplxMax
        for i in range(len(self.equacolO)):
            self.data.append(self.equacolO[i, np.ix_([0, 1, 3, 4, 7])][0])
            #self.dataMaxComplexity = max(self.dataMaxComplexity, self.equacolPO[i,np.ix_([0])][0][0])
            #self.dataMaxFitness = max(self.dataMaxFitness, self.equacolPO[i,np.ix_([1])][0][0])



        self.labels = {}
        self.edges = None

        self.varEquasize=OrderedDict(list(zip(self.dataset.varnames,self.nbeq)))
        self.varEquasizeOnlyTrue=self.varEquasize.copy()
        self.computeEquaPerNode()

        ##########################
        #self.datumIncMat = pd.read_csv("data/equa_with_col_Parent_withMol.csv", header=None)
        #self.datumIncMat = self.datumIncMat.sort(2)
        self.datumIncMat=pd.DataFrame(self.equacolO)
        variables = self.varsIn + sorted(self.datumIncMat[2].unique().tolist())

        self.df_IncMat = pd.DataFrame(index=self.datumIncMat[2], columns=self.varsIn + self.datumIncMat[2].unique().tolist())
        for row in range(self.df_IncMat.shape[0]):
            v = self.df_IncMat.index.values[row]
            self.df_IncMat.ix[row] = self.getV(self.df_IncMat.columns.values, self.datumIncMat.iloc[row][3], v)

        self.dataIncMat = self.df_IncMat
        self.shapeIncMat = self.dataIncMat.shape

        #self.dataIncMat.to_csv('debugMat.csv',header = True, index = True)

        ##########################



        self.initGraph()
        if self.firstInit:
            vwApp = RFGraph_View(self)
            cntrApp = RFGraph_Controller(self, vwApp)
            vwApp.cntrApp = cntrApp
            vwApp.eqTableGUI.cntrApp = cntrApp
            vwApp.updateMenuBar(cntrApp)
            vwApp.eqTableGUI.horizontalHeader().sortIndicatorChanged.connect(cntrApp.eqTableHeaderClicked)

            #self.progress_bar_global = vwApp.global_compute_progress
            qtconnector = QtConnector(vwApp, cntrApp)
        self.firstInit=False

    def correctDataset(self,dataset,constrGraph):
        dataset.varnames=dataset.true_varnames
        dataset.nbVar = dataset.true_nbVar
        dataset.variablesClass = dataset.true_variablesClass
        dataset.data = dataset.true_data

        for vc in constrGraph.nodes():
            for v in vc.nodeList:
                dataset.variablesClass[v]=vc.name

        allidx=[]
        for unv in constrGraph.unboundNode:
            idx = np.where(dataset.varnames == unv)
            dataset.variablesClass.pop(unv)
            allidx.append(idx[0][0])

        dataset.varnames = np.delete(dataset.varnames,allidx)
        dataset.nbVar = len(dataset.varnames)
        dataset.data = np.delete(dataset.data,allidx,axis=1)

        dataset.varnames_extd=copy.deepcopy(dataset.varnames)
        dataset.data_extd=copy.deepcopy(dataset.data)

        for v in dataset.varnames:
            idx=np.where(dataset.varnames == v)
            idx=idx[0][0]

            constrNodeV=[n for n in constrGraph.nodes() if n.name == dataset.variablesClass[v]][0]

            if('Square' in constrNodeV.operators):
                newVar=v+"^2"
                dataset.varnames_extd=np.append(dataset.varnames_extd,newVar)
                dataset.data_extd=np.append(dataset.data_extd,np.transpose(np.array([dataset.data_extd[:,idx]**2])),axis=1)
                dataset.variablesClass[newVar]=dataset.variablesClass[v]

            if ('Exponentiel' in constrNodeV.operators):
                newVar = "exp("+v+")"
                expV=np.transpose(np.exp(np.array([dataset.data_extd[:, idx]])))
                if(not True in np.isinf(expV)):
                    dataset.varnames_extd = np.append(dataset.varnames_extd, newVar)
                    dataset.data_extd = np.append(dataset.data_extd, expV,axis=1)
                dataset.variablesClass[newVar] = dataset.variablesClass[v]

            if ('Logarithm' in constrNodeV.operators):
                newVar = "log("+v+")"
                logV=np.transpose(np.log(np.array([dataset.data_extd[:, idx]])))
                if (not True in np.isinf(logV) and not True in np.isnan(logV)):
                    dataset.varnames_extd = np.append(dataset.varnames_extd, newVar)
                    dataset.data_extd = np.append(dataset.data_extd, logV,axis=1)
                    dataset.variablesClass[newVar] = dataset.variablesClass[v]

            if ('Inverse' in constrNodeV.operators):
                newVar = "1/"+v
                divV=np.transpose(np.divide(1,np.array([dataset.data_extd[:, idx]])))
                if (not True in np.isinf(divV)):
                    dataset.varnames_extd = np.append(dataset.varnames_extd, newVar)
                    dataset.data_extd = np.append(dataset.data_extd, divV, axis=1)
                    dataset.variablesClass[newVar] = dataset.variablesClass[v]

            if ('Multiplication (x1*x2)' in constrNodeV.operators):

                for v2 in [v2 for v2 in constrNodeV.nodeList if v2!=v]:
                    idx2 = np.where(dataset.varnames == v2)
                    idx2 = idx2[0][0]
                    newVar = v+"*"+v2
                    multV=np.transpose(np.array([dataset.data_extd[:, idx2]])*np.array([dataset.data_extd[:, idx]]))
                    dataset.varnames_extd = np.append(dataset.varnames_extd, newVar)
                    dataset.data_extd = np.append(dataset.data_extd, multV, axis=1)
                    dataset.variablesClass[newVar] = dataset.variablesClass[v]






        dataset.classesIn=[]
        dataset.varsIn=[]
        for vc in constrGraph.nodes():
            if((len([e for e in constrGraph.edges() if e[1] == vc])==0)):
                dataset.classesIn.append(vc.name)
                dataset.varsIn.extend(vc.nodeList)

    def recomputeNode(self,node,neweqs):
        self.equacolO[self.equacolO[:, 2] == node, :]
        linesToRemove = np.ix_(self.equacolO[:, 2] == node)

    def createProgressBar(self):
        self.setWindowTitle("Searching for models")
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(0, 0, 250, 20)
        self.setGeometry(50, 50, 295, 25)
        self.progress.setValue(0)
        self.show()

    def evalfit(self,nbAP, nbPP, dataSize, nbRepet=10):
        if (nbAP > nbPP):
            nbAPr = nbPP
        else:
            nbAPr = nbAP
        meanf = 0
        for i in range(nbRepet):
            X = np.random.rand(dataSize)
            P = np.random.rand(dataSize, nbPP)
            clf = linear_model.OrthogonalMatchingPursuit(n_nonzero_coefs=nbAPr)
            clf.fit(P, X)
            Y = clf.predict(P)
            meanf += fitness(X, Y) / nbRepet
        return meanf

    def eaForLinearRegression(self,X,Y,nb):
        random.seed(123)
        if(nb==1):
            bestFit=np.Inf
            bestX=-1
            bestReg=None
            for i in range(X.shape[1]):
                reg=linear_model.LinearRegression()
                X1D=[]
                for e in X[:,i]:
                    X1D.append([e])
                reg.fit(X1D,Y)
                pred=reg.predict(X1D)
                fit = fitness(Y, pred)
                if(fit < bestFit):
                    bestFit=fit
                    bestX=i
                    bestReg=reg

            class MyReg():
                def __init__(self,coef,intercept,pred):
                    self.coef_=coef
                    self.intercept_=intercept
                    self.pred=pred

            coef=np.zeros(X.shape[1])
            coef[bestX]=bestReg.coef_[0]
            X1D = []
            for e in X[:, bestX]:
                X1D.append([e])
            falseReg=MyReg(coef,bestReg.intercept_,bestReg.predict(X1D))
            return falseReg
        else:
            print("OPTIMISATION WITH " + str(nb) )
            eqOpt=equaOptim(X,Y,nb)
            ret=eqOpt.startOptim()

            reg = linear_model.LinearRegression()
            xind=np.argwhere(np.array(ret) == 1).flatten()
            reg.fit(X[:,xind], Y)
            pred = reg.predict(X[:,xind])

            class MyReg():
                def __init__(self, coef, intercept, pred):
                    self.coef_ = coef
                    self.intercept_ = intercept
                    self.pred = pred

            coef = np.zeros(X.shape[1])

            for i in range(len(xind)):
                coef[xind[i]]=reg.coef_[i]

            falseReg=MyReg(coef,reg.intercept_,pred)

            return falseReg

    def addnoise(self,m): #to make it possible to use OrthogonalMatchingPursuit for some datasets
        newM=np.array(m)
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                newM[i,j] = m[i,j] * (1+(random.random()*2-1)*0.0000001)

        return newM

    def findLassoEqs(self):
        equacolOtmp=[]
        self.createProgressBar()
        for i in range(len(self.dataset.varnames)):
            print('computing : ' + self.dataset.varnames[i])
            self.progress.setValue(i*100/len(self.dataset.varnames))
            iClass = self.dataset.variablesClass[self.dataset.varnames[i]]
            print(self.dataset.classesIn)
            if(not iClass in self.dataset.classesIn):
                parIClass=[]
                for (e1,e2) in self.adj_contrGraph.edges():
                    if(e2.name==iClass and not e1.name in parIClass):
                        parIClass.append(e1.name)
                #parIClass=list(self.adj_contrGraph.edge[iClass].keys())
                par=[]
                for v in self.dataset.varnames_extd:
                    if(self.dataset.variablesClass[v] in parIClass):
                        par.append(v)
                Y = list(self.dataset.data[:, i])


                idx=[list(self.dataset.varnames_extd).index(v) for v in par]
                try:
                    X=self.dataset.data_extd[:,idx]
                except Exception as e:
                    print(e)


                nbEqToFind=10

                for j in range(1,np.minimum(nbEqToFind,len(idx))+1):
                    if self.regressionType=='OMP':
                        clf = linear_model.OrthogonalMatchingPursuit(n_nonzero_coefs=j)
                        #clf = self.eaForLinearRegression(X, Y, j)
                        factnormY=(1 / np.mean(np.array(Y)))
                        Yn=list(np.array(Y)*factnormY)
                        Xn=self.addnoise(X)
                        clf.fit(Xn, Yn)
                        clf.coef_ = clf.coef_ / factnormY
                        clf.intercept_ = clf.intercept_ / factnormY
                        pred = clf.predict(X)
                    elif self.regressionType == 'EA':
                        clf = self.eaForLinearRegression(X, Y, j)
                        pred = clf.pred

                    equacolOLine = self.regrToEquaColO(clf, par, self.dataset.varnames_extd[i], Y, pred)
                    # TODO restaurer sensitivity analysis
                    Si = random.random()  # self.SA_Eq(X, par, clf)
                    equacolOLine.append(Si)
                    evFit = self.evalfit(j, len(par), len(Y))
                    equacolOLine.append(evFit)
                    equacolOtmp.extend(equacolOLine)
                # curEqFound=0
                # alpha=1
                # cmplxOneFound=False
                # lastFoundCmplx=1
                # maxIter=10
                # currIter=0
                # maxIter2=20
                # currIter2=0
                # while(curEqFound != nbEqToFind and currIter2!=maxIter2):
                #     currIter2+=1
                #     while(not cmplxOneFound): #Find equation of complexity one
                #         clf = linear_model.Lasso(alpha=alpha)
                #         clf.fit(X, Y)
                #
                #         pred = clf.predict(X)
                #         equacolOLine = self.regrToEquaColO(clf, par, self.dataset.varnames[i], Y, pred)
                #         #print("Find first : equacolOLine[0]" + str(equacolOLine[0]) + " alpha= "+str(alpha) + " curEqFound: " + str(curEqFound))
                #         if(equacolOLine[0]==1):
                #             cmplxOneFound = True
                #             curEqFound+=1
                #             #print("Add : " + str(equacolOLine[3]))
                #             Si = self.SA_Eq(X, par, clf)
                #             equacolOLine.append(Si)
                #             if(len(equacolOLine)==8):
                #                 print("stop:" + str(len(equacolOLine)))
                #             print("was:" + str(len(equacolOLine)) + " cpmlx:" + str(lastFoundCmplx))
                #             equacolOtmp.extend(equacolOLine)
                #         else:
                #             alpha *= 2
                #
                #     alpha/=2
                #     clf = linear_model.Lasso(alpha=alpha)
                #     clf.fit(X, Y)
                #     pred=clf.predict(X)
                #     equacolOLine=self.regrToEquaColO(clf,par,self.dataset.varnames[i],Y,pred)
                #     #print("cmplx : " + str(equacolOLine[0]) + " alpha= " + str(alpha)  + " curEqFound: " + str(curEqFound)+ " lastFoundCmplx : " + str(lastFoundCmplx))
                #     if (equacolOLine[0] > lastFoundCmplx + 4):
                #         minAlpha=alpha
                #         maxAlpha=alpha*2
                #         currIter=0
                #         while(equacolOLine[0]!=lastFoundCmplx + 4 and currIter!=maxIter):
                #             currIter+=1
                #             alpha=(minAlpha+maxAlpha)/2
                #             clf = linear_model.Lasso(alpha=alpha)
                #             clf.fit(X, Y)
                #             pred = clf.predict(X)
                #             equacolOLine = self.regrToEquaColO(clf, par, self.dataset.varnames[i], Y, pred)
                #             #print("cmplx : " + str(equacolOLine[0]) + " alpha= " + str(alpha) + " curEqFound: " + str(curEqFound) + " lastFoundCmplx : " + str(lastFoundCmplx))
                #             #print("     minAlpha = " + str(minAlpha) + " maxAlpha = " + str(maxAlpha) + " lastFoundCmplx:"+str(lastFoundCmplx))
                #             if(equacolOLine[0] > lastFoundCmplx + 4):
                #                 minAlpha=alpha
                #             elif(equacolOLine[0] < lastFoundCmplx + 4):
                #                 maxAlpha=alpha
                #             else:
                #                 lastFoundCmplx = equacolOLine[0]
                #                 #print("Add : " + str(equacolOLine[3]))
                #                 Si = self.SA_Eq(X,par,clf)
                #                 equacolOLine.append(Si)
                #                 if (len(equacolOLine) == 8):
                #                     print("stop:" + str(len(equacolOLine)))
                #                 print("was:" + str(len(equacolOLine)) + " cpmlx:" + str(lastFoundCmplx))
                #                 equacolOtmp.extend(equacolOLine)
                #                 currIter2=0
                #                 curEqFound += 1
                #                 break
                #         if(currIter==maxIter and not len(equacolOLine) == 7): #and we don't already have the SA results
                #             lastFoundCmplx=equacolOLine[0]
                #             #print("Add : " + str(equacolOLine[3]))
                #             Si = self.SA_Eq(X, par, clf)
                #             equacolOLine.append(Si)
                #             if (len(equacolOLine) == 8):
                #                 print("stop:" + str(len(equacolOLine)))
                #             print("was:" + str(len(equacolOLine)) + " cpmlx:"+str(lastFoundCmplx))
                #             equacolOtmp.extend(equacolOLine)
                #             currIter2=0
                #             curEqFound += 1
                #     elif(equacolOLine[0] < lastFoundCmplx + 4):
                #         alpha /= 2
                #     else:
                #         lastFoundCmplx = equacolOLine[0]
                #         #print("Add : " + str(equacolOLine[3]))
                #         Si = self.SA_Eq(X, par, clf)
                #         equacolOLine.append(Si)
                #         if (len(equacolOLine) == 8):
                #             print("stop:" + str(len(equacolOLine)))
                #         print("was:" + str(len(equacolOLine)) + " cpmlx:" + str(lastFoundCmplx))
                #         equacolOtmp.extend(equacolOLine)
                #         currIter2=0
                #         curEqFound += 1

        self.hide()
        equacolOtmp = np.array(equacolOtmp, dtype=object)
        print(len(equacolOtmp)/8)
        equacolOtmp = equacolOtmp.reshape(int(len(equacolOtmp)/8),8)


        return equacolOtmp

    def SA_Eq(self,X,par,clf):
        xmin = np.amin(X, axis=0)
        xmax = np.amax(X, axis=0)

        xbounds = []
        for i in range(len(xmin)):
            xbounds.append([xmin[i], xmax[i]])

        pb = {}
        pb['bounds'] = xbounds
        pb['dists'] = None
        pb['groups'] = None
        pb['names'] = par
        pb['num_vars'] = len(par)

        param_values = saltelli.sample(pb, 10, calc_second_order=False)

        YSobol = clf.predict(param_values)


        #
        Si = sobol.analyze(pb, YSobol, calc_second_order=False, conf_level=0.95,
                           print_to_console=False, parallel=False)
        #Si = sobol.analyze(pb, YSobol, calc_second_order=False, conf_level=0.95,
        #                   print_to_console=False, parallel=False)
        print("par =" + str(np.array(par)) + "\n"+ str(Si['ST_conf']))
        Si['par']=par
        return Si

    def regrToEquaColO(self,clf,parNode,childNode,Y,pred):
        line=[]
        s=''
        cmplx = 0;
        hasCoef=False
        varUsedInEq=[]


        for i in range(len(parNode)):
            if(clf.coef_[i] > 0  ):
                hasCoef=True
                s += ' + ' + str(clf.coef_[i]) + ' * ' + parNode[i] + ' '
                varUsedInEq.append(parNode[i])
                cmplx += 4
            elif(clf.coef_[i] < 0 ):
                hasCoef=True
                s +=  str(clf.coef_[i]) + ' * ' + parNode[i] + ' '
                varUsedInEq.append(parNode[i])
                cmplx += 4

        if (clf.intercept_ != 0 and hasCoef):
            s = str(clf.intercept_) + ' ' + s
            cmplx += 1;

        if (clf.intercept_ != 0 and not hasCoef):
            s += str(clf.intercept_)
            cmplx += 1;

        if(clf.intercept_ == 0):
            cmplx -= 1;

        fit=fitness(Y,pred)

        line.append(cmplx)
        line.append(fit)
        line.append(childNode)
        line.append(s)
        line.append(True)
        line.append(varUsedInEq)



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
        lastval = None
        counter = 1
        for s in stringTab:
            convertArr.append(np.float32(s[0]))
            xr=self.dataset.getAllExpsforVar(s[2])
            yr=[]
            for numExp in range(self.dataset.nbExp):
                yr.append(parse_expr(s[3].replace("^","**"), local_dict=self.dataset.getAllVarsforExp(numExp)))
            mfx = list(map(float, xr.tolist()))
            #print(yr)
            mfy = list(map(float, yr))
            recomputedFitness=fitness(mfx, mfy)
            #convertArr.append(np.float32(s[1]))
            convertArr.append(recomputedFitness)
            convertArr.append(s[2])
            convertArr.append(s[3])
            convertArr.append(True)
            convertArr.append(list(filter(lambda x: x in s[3], self.dataset.varnames)))
            convertArr.append(random.random()) #SA Thomas .
            parIClass = []
            iClass = self.dataset.variablesClass[s[2]]
            for (e1, e2) in self.adj_contrGraph.edges():
                if (e2.name == iClass and not e1.name in parIClass):
                    parIClass.append(e1.name)
            # parIClass=list(self.adj_contrGraph.edge[iClass].keys())
            par = []
            for v in self.dataset.varnames_extd:
                if (self.dataset.variablesClass[v] in parIClass):
                    par.append(v)
            if lastval == s[2]:
                counter += 1
            else:
                counter = 1
                lastval = s[2]
            convertArr.append(self.evalfit(counter, len(par), self.dataset.true_nbExp))
            #convertArr.append(sympify(s[3]))


        finalTab = np.array(convertArr, dtype=object)
        shp = np.shape(stringTab)
        finalTab = finalTab.reshape((shp[0], shp[1] + 4))
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
            v=self.dataset.varnames[i]
            for vclasse in self.adj_contrGraph.nodes():
                if(v in vclasse.nodeList):
                    vcolor=tuple(vclasse.color)
                    break
            self.nodeColor.append(vcolor)

            #self.nodeColor.append((0.5, 0.5 + 0.5 * self.nodeWeight[i] / np.amax(self.nodeWeight), 0.5))
            #if(self.dataset.varnames[i])
            #self.
            # if(self.dataset.variablesClass[self.dataset.varnames[i]]== 'Molss' or self.dataset.variablesClass[self.dataset.varnames[i]]== 'Molsur'):
            #     self.nodeColor.append((0.5, 0.5, 0.9))
            # if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'condition'):
            #     self.nodeColor.append((0.9, 0.55, 0.55))
            # if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'Cell'):#CellAniso
            #     self.nodeColor.append((0.3, 0.9, 0.9))
            # if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'CellAniso'):
            #     self.nodeColor.append((0.7, 0.7, 0.5))
            # if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'PopCentri'):
            #     self.nodeColor.append((0.8, 0.8, 0.2))
            # if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'PopLyo'):
            #     self.nodeColor.append((0.8, 0.8, 0.2))
            # if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'PopCong'):
            #     self.nodeColor.append((0.8, 0.8, 0.2))
            # if (self.dataset.variablesClass[self.dataset.varnames[i]] == 'PopSto3'):
            #     self.nodeColor.append((0.8, 0.8, 0.2))
        self.computeInitialPos()
        self.computeFitandCmplxEdgeColor()
        self.computeFitRandColor()
        self.computeComprEdgeColor()
        #self.computeSAEdgeColor()
        self.computePearsonColor()

        self.computeNxGraph()

    def computePearsonColor(self):
        self.allPearson={}
        for v1 in self.dataset.varnames:
            for v2 in self.dataset.varnames:
                xd=self.dataset.getAllExpsforVar(v1)
                yd=self.dataset.getAllExpsforVar(v2)
                try:
                    self.allPearson[(v1,v2)] = pearsonr(xd, yd)[0]
                except:
                    pass
        self.edgeColorPearson = {}
        for ek, ev in self.allPearson.items():
            ek0_parClass=self.dataset.variablesClass[ek[0]]
            ek1_parClass = self.dataset.variablesClass[ek[1]]
            if((ek0_parClass,ek1_parClass) in self.adj_contrGraph.edgesTrueName):
                self.edgeColorPearson[(ek[0],ek[1])] =self.allPearson[(ek[0],ek[1])]

        for e, v in self.edgeColorPearson.items():
            cmap = self.colors.get("Pearson", (v/2)+0.5)
            # color = QColor.fromRgb(*cmap)
            lcmap = list(np.array(cmap) / 255)
            lcmap.extend([1.0])
            self.edgeColorPearson[e] = lcmap



    def createConstraintsGraph(self):
        #graph = nx.DiGraph()
        graph = ClassGraph()
        for i in np.unique(list(self.dataset.variablesClass.values())):
            #print(i)
            i_var = [v for (v, e) in self.dataset.variablesClass.items() if e ==i ]
            graph.add_node(ClassNode(i, i_var))
        #testMutex = threading.Lock()
        #print("creating classes window")
        classApp=WindowClasses(graph,self.init2)
        #classApp=Window(ClassGraph.readJson("classes/screen.clgraph"),self.init2)
        #print("after classes window")
        #graph=classApp.exec()
        #testMutex.acquire(True)



        #graph=classApp.graph
        # graph.add_edge('condition','Molss')
        # graph.add_edge('condition', 'Molsur')
        # graph.add_edge('condition','Cell')
        # graph.add_edge('Molss','Cell')
        # graph.add_edge('Molsur', 'Cell')
        # #graph.add_edge('Molsur','Molss')
        # graph.add_edge('Cell', 'CellAniso')
        # graph.add_edge('Cell','PopCentri')
        # graph.add_edge('Cell','PopCong')
        # graph.add_edge('Cell','PopLyo')
        # graph.add_edge('Cell','PopSto3')
        # graph.add_edge('CellAniso', 'PopCentri')
        # graph.add_edge('CellAniso', 'PopCong')
        # graph.add_edge('CellAniso', 'PopLyo')
        # graph.add_edge('CellAniso', 'PopSto3')
        # graph.add_edge('condition','PopCentri')
        # graph.add_edge('condition','PopCong')
        # graph.add_edge('condition','PopLyo')
        # graph.add_edge('condition','PopSto3')
        # graph.add_edge('PopCentri','PopCong')
        # graph.add_edge('PopCentri','PopLyo')
        # graph.add_edge('PopCentri','PopSto3')
        # graph.add_edge('PopCong','PopLyo')
        # graph.add_edge('PopCong', 'PopSto3')
        # graph.add_edge('PopLyo','PopSto3')

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

    def removeInvisibleEdges(self):
        self.invisibleTup = []

        self.edgeBoldDict=copy.deepcopy(self.edgeBoldfull)
        if (self.ColorMode == 'Compr'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorCompr)
        elif (self.ColorMode == 'Fit'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorFit)
        elif (self.ColorMode == 'Cmplx'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorCmplx)
        elif (self.ColorMode == 'SA'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorSA)
        elif (self.ColorMode == 'Pearson'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorPearson)
        elif (self.ColorMode == 'FitRd'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorFR)
        for i in range(len(self.pareto)):  # i is child
            for j in range(len(self.pareto[i])):  # j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    # if self.nbeq[i] == np.float64(0.0): continue
                    r = self.adj_simple[i, j] / self.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                    tup = (self.dataset.varnames[j], self.dataset.varnames[i])
                    if (self.ColorMode!='Pearson' and self.ColorMode!='SA' and r <= self.adjThresholdVal):
                        self.invisibleTup.append(tup)
                    elif((self.ColorMode=='Pearson' or self.ColorMode=='SA') and not -1+self.adjThresholdVal < self.allPearson[tup] < 1-self.adjThresholdVal ):
                        self.invisibleTup.append(tup)

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
                    r = self.adj_simple[i, j] / self.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
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
            except Exception as e:
                print(e)
                pass
        return colorList

    def computeEdgeBold(self):

        self.edgeBoldfull = {}
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
                    r = self.adj_simple[i, j] / self.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i

                    if(dist_lIdxColPareto_valMin<0.5):
                        cr = dist_lIdxColPareto_valMin
                        cg = 1-dist_lIdxColPareto_valMin
                        cb = dist_lIdxColPareto_valMin
                    else:
                        cr = dist_lIdxColPareto_valMin
                        cg = 1 - dist_lIdxColPareto_valMin
                        cb = 1 - dist_lIdxColPareto_valMin

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

                    cr = np.minimum(self.adj_fit[i, j] * 2, 1)
                    cg = np.minimum((1 - self.adj_fit[i, j]) * 2, 1)
                    cb = 0
                    if (self.transparentEdges):
                        self.edgeColorFit[(self.dataset.varnames[j], self.dataset.varnames[i])]=[cr + (1 - cr) * (1 - r), cg + (1 - cg) * (1 - r), cb + (1 - cb) * (1 - r),1]
                    else:
                        cmap = self.colors.get("local",self.adj_fit[i, j])
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
                        lcmap = list(np.array(cmap) / 255)
                        lcmap.extend([1.0])
                        self.edgeColorCmplx[(self.dataset.varnames[j], self.dataset.varnames[i])]=lcmap

    def computeFitRandColor(self):
        self.edgeColorFR = {}
        for e in self.edgeColorFit.keys():
            idxE = np.where(self.equacolPO[:, 2] == e[1])[0]
            idxPe = np.where(self.equacolPO[idxE, 3] == e[0])[0]
            idxP = idxE[idxPe]
            eqs=self.equacolPO[idxP, 4]
            eqsC = [self.equacolO[self.equacolO[:, 3] == e, :][0] for e in eqs]
            edgeColVal = [np.minimum(e[1] / e[7], 1) for e in eqsC][0]
            #edgeColVal=np.mean([np.minimum(e[1] / e[7], 1) for e in eqsC])
            edgeColVal = np.min([np.minimum(e[1] / e[7], 1) for e in eqsC])

            cmap = self.colors.get("local",edgeColVal)
            lcmap = list(np.array(cmap) / 255)
            lcmap.extend([1.0])
            self.edgeColorFR[e] = lcmap



    def computeSAEdgeColor(self):
        self.edgeColorSA={}
        for e in self.edgeColorFit.keys():
            samin=1
            samax=0

            for eq in self.equacolO[self.equacolO[:,2]==e[1]]:
                sa=eq[6]
                if(samin > sa['ST'][sa['par'].index(e[0])] and e[0] in eq[5]):
                    samin= sa['ST'][sa['par'].index(e[0])]
                if(samax <sa['ST'][sa['par'].index(e[0])] and e[0] in eq[5]):
                    samax = sa['ST'][sa['par'].index(e[0])]
            if(samin > 0.5 and samax > 0.5):
                self.edgeColorSA[e]=samin*0.5+samax*0.5
            elif(samin<0.25 and samax < 0.25):
                self.edgeColorSA[e] = samin * 0.5 + samax * 0.5
            elif(samin<0.25 and samax > 0.5):
                self.edgeColorSA[e]=0.5
            elif(0.25<=samin<=0.5 or 0.25<=samax<=0.5):
                self.edgeColorSA[e] = 0.5
            else:
                print("SA ERROR !")
                    #self.edgeColorSA[e]=sa['ST'][sa['par'].index(e[0])]

        for e in self.edgeColorSA.keys():
            v=self.edgeColorSA[e]
            cmap = self.colors.get("SA", 1-v)
            # color = QColor.fromRgb(*cmap)
            lcmap = list(np.array(cmap) / 255)
            lcmap.extend([1.0])
            self.edgeColorSA[e]=lcmap
        #self.edgeColorFit=self.edgeColorSA
        #print('it worked ?')


    def computeInitialPos(self):
        G=nx.DiGraph()
        G.clear()
        for v in self.dataset.varnames:
            G.add_node(v)
        ed=[]
        for i in range(len(self.pareto)):
            for j in range(len(self.pareto[i])):
                for k in range(len(self.adj_contrGraph.nodes())):
                    if list(self.adj_contrGraph.nodes())[k].name == self.dataset.variablesClass[self.dataset.varnames[j]]:
                        jClass=list(self.adj_contrGraph.nodes())[k]
                    if list(self.adj_contrGraph.nodes())[k].name == self.dataset.variablesClass[self.dataset.varnames[i]]:
                        iClass=list(self.adj_contrGraph.nodes())[k]
                if self.adj_contrGraph.has_edge(jClass, iClass):
#                        print(self.dataset.varnames[j] + " --> " + self.dataset.varnames[i] + " : " + self.dataset.variablesClass[self.dataset.varnames[j]] + " --> " + self.dataset.variablesClass[self.dataset.varnames[i]])
                    ed.append((self.dataset.varnames[j], self.dataset.varnames[i]))
                    G.add_edge(self.dataset.varnames[j], self.dataset.varnames[i],
                                    adjsimple=self.adj_simple[i, j], adjfit=
                                    self.adj_fit[i, j], adjcmplx=self.adj_cmplx[i, j],
                                    adjcontr=self.adj_contr[i, j])

        #with open('initpos.dat', 'rb') as f:
        #    self.pos=pickle.load(f)
        self.pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
        #self.pos = nx.circular_layout(G)
        #self.pos = nx.nx_pydot.pydot_layout(G)
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
        if(miny==maxy):
            for k in list(self.pos.keys()):
                self.pos[k]=(self.pos[k][0],random.random()*300)
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

            # print(k +" : (" + str(self.pos[k][0]) + ","+str(self.pos[k][1])+")")

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
                idxV = np.where(self.equacolO[:, 2] == v)[0]
                eqs = self.equacolO[idxV[np.where(self.equacolO[idxV, 4] == True)[0]], :]
                equaLines.append(eqs[self.selectedEq[v]])
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
            cb = 0.0
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

