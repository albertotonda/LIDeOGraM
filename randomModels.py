#recupere la soltuion réel,
#recupere les soltuion lideo
# Tracé démo de l'algo d'apprentissage ?
# Tracé démo de l'optimisation global en fct bruit et taille model
#Auto générer les tests ?
#-*- coding: utf-8
import copy
import random
import re
import sys

import networkx as nx
import numpy as np

sys.path.append("fitness/")
sys.path.append('SALib/SaLib-master')
from SALib.analyze import sobol
from SALib.sample import saltelli
from scipy.stats.stats import pearsonr
from fitness import Individual
from equaOptim import equaOptim
import pandas as pd
from Dataset import Dataset
import ColorMaps
from collections import OrderedDict
from sklearn import linear_model
import fitness
from classes.ClassGraph import ClassGraph
from classes.ClassNode import ClassNode
from OptimModGlobal import OptimModGlobal
#from classes.WindowClasses import WindowClasses
import logging
import time


# TODO  Définie la position des noeuds et les initialise
class RandomModels():

    def __init__(self, mdl, output, cgraph):
        print(mdl,output,cgraph)
        self.outputfolder = output
        logging.basicConfig(filename=mdl+'.log', level=logging.DEBUG)
        logging.info("Program started -- {}".format(time.strftime("%d %m %y: %H %M %S")))
        self.name = mdl
        self.dataset = Dataset(mdl,cgraph)
        self.firstInit=True
        ctgraph = self.createConstraintsGraph()
        self.init2(ctgraph)
        logging.info("global search started -- {}".format(time.strftime("%d %m %y: %H %M %S")))
        optModGlob = OptimModGlobal(self)
        self.best_indv = optModGlob.startOptim()
        with open(self.outputfolder+"\\"+self.name.split("\\")[-1]+"_equasgflgob", 'w') as outp:
            #outp.write(str(self.best_indv))
            for k, v in self.best_indv.items():
                 outp.write(str(k) + ' >>> ' + str(v) + '\n')
        logging.info("global search finished -- {}".format(time.strftime("%d %m %y: %H %M %S")))
        logging.info("Program end -- {}".format(time.strftime("%d %m %y: %H %M %S")))

        logging.info("==============================================================")



    def init2(self,contrgraph):

        self.adj_contrGraph = contrgraph
        self.adj_contrGraph.edgesTrueName=[]
        for (e0,e1) in self.adj_contrGraph.edges():
            self.adj_contrGraph.edgesTrueName.append((e0.name,e1.name))
        self.correctDataset(self.dataset,self.adj_contrGraph)
        logging.info("local search started -- {}".format(time.strftime("%d %m %y: %H %M %S")))
        self.equacolO = self.findLassoEqs()
        logging.info("local search finished -- {}".format(time.strftime("%d %m %y: %H %M %S")))


        lst = self.equacolO.tolist()
        with open(self.outputfolder+"/"+self.name.split("\\")[-1]+"_equafgs",'w') as output:
            for _ in lst:
                output.write(",".join(map(lambda x: str(x),_)))
                output.write("\n")

        self.nbequa = len(self.equacolO)  # Number of Equation for all variables taken together
        self.adj_simple=np.zeros((self.dataset.nbVar,self.dataset.nbVar))
        self.adj_fit=np.ones((self.dataset.nbVar,self.dataset.nbVar))
        self.adj_cmplx=np.ones((self.dataset.nbVar,self.dataset.nbVar))
        self.nbeq=np.zeros(self.dataset.nbVar) # Number of equations for each variables

        self.equacolPO=[]
        for l in range(self.nbequa):
            for h in range(self.dataset.nbVar):
                #Possible parents for the equations
                cont_h = -1
                try:
                    cont_h=len(re.findall(r'\b%s\b' % re.escape(self.dataset.varnames[h]),self.equacolO[l,3]))  #How many times the variable self.varname[h] is found in the equation self.equacolO[l,3]
                    cont_h =cont_h+len(re.findall(r'\b%s\b' % re.escape(self.dataset.varnames[h]+"^2"), self.equacolO[l, 3]))
                except:
                    pass
                if(cont_h>0): #If present, add infos in adjacence matrix
                    ind_parent=h
                    ind_offspring=list(self.dataset.varnames).index(self.equacolO[l,2])
                    self.adj_simple[ind_offspring,ind_parent]+=1
                    self.adj_cmplx[ind_offspring,ind_parent]*=self.equacolO[l,0] #  GEOMETRIC mean
                    if(self.equacolO[l,1] != 0):
                        self.adj_fit[ind_offspring,ind_parent]*=self.equacolO[l,1] #  GEOMETRIC mean
                    self.equacolPO.append([self.equacolO[l,0],self.equacolO[l,1],self.equacolO[l,2],self.dataset.varnames[h],self.equacolO[l,3], self.equacolO[l,4]])
            self.nbeq[list(self.dataset.varnames).index(self.equacolO[l,2])]+=1 # Comptage du nombre d'équations pour chaque enfant

        self.equacolPO =np.array(self.equacolPO, dtype=object)





        self.adj_cmplx=np.power(self.adj_cmplx,1/self.adj_simple)
        self.adj_cmplx[self.adj_simple==0]=0
        self.adj_fit = np.power(self.adj_fit, 1 / self.adj_simple)
        self.adj_fit[self.adj_simple == 0] = 0


        self.adj_contr=self.createConstraints()

        self.pos = []
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
        #
        for i in range(len(self.equacolO)):
            self.data.append(self.equacolO[i, np.ix_([0, 1, 3, 4])][0])
        #
        #
        self.labels = {}
        self.edges = None

        self.varEquasize=OrderedDict(list(zip(self.dataset.varnames,self.nbeq)))
        self.varEquasizeOnlyTrue=self.varEquasize.copy()
        # self.computeEquaPerNode()

        ##########################

        self.datumIncMat=pd.DataFrame(self.equacolO)

        self.df_IncMat = pd.DataFrame(index=self.datumIncMat[2], columns=self.varsIn + self.datumIncMat[2].unique().tolist())
        for row in range(self.df_IncMat.shape[0]):
            v = self.df_IncMat.index.values[row]
            self.df_IncMat.ix[row] = self.getV(self.df_IncMat.columns.values, self.datumIncMat.iloc[row][3], v)

        self.dataIncMat = self.df_IncMat
        self.shapeIncMat = self.dataIncMat.shape

        ##########################



       # self.initGraph()

    def correctDataset(self,dataset,constrGraph):
        #TODO viere ceux qui servent a rien
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
            allidx.append(idx)

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






        dataset.classesIn=[]
        dataset.varsIn=[]
        for vc in constrGraph.nodes():
            if((len([e for e in constrGraph.edges() if e[1] == vc])==0)):
                dataset.classesIn.append(vc.name)
                dataset.varsIn.extend(vc.nodeList)

    def recomputeNode(self,node,neweqs):
        self.equacolO[self.equacolO[:, 2] == node, :]
        linesToRemove = np.ix_(self.equacolO[:, 2] == node)

    def eaForLinearRegression(self,X,Y,nb):
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

    def findLassoEqs(self):
        equacolOtmp=[]
        for i in range(len(self.dataset.varnames)):
            print('computing : ' + self.dataset.varnames[i])
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
                X=self.dataset.data_extd[:,idx]


                nbEqToFind=6

                for j in range(1,np.minimum(nbEqToFind,len(idx))+1):


                    clf = self.eaForLinearRegression(X,Y,j)#linear_model.LinearRegression()#linear_model.OrthogonalMatchingPursuit(n_nonzero_coefs=j)
                    #clf.fit(X, Y)
                    #pred = clf.predict(X)
                    pred=clf.pred

                    equacolOLine = self.regrToEquaColO(clf, par, self.dataset.varnames_extd[i], Y, pred)
                    #TODO restaurer sensitivity analysis
                    Si = random.random()#self.SA_Eq(X, par, clf)
                    equacolOLine.append(Si)
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

       # self.hide()
        equacolOtmp = np.array(equacolOtmp, dtype=object)
        equacolOtmp = equacolOtmp.reshape(len(equacolOtmp)/7,7)


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
        param_values = None
        try:
            param_values = saltelli.sample(pb, 100, calc_second_order=False)
        except:
            pass
        YSobol = clf.predict(param_values)


        #
        Si = sobol.analyze(pb, YSobol, calc_second_order=False, conf_level=0.95,
                           print_to_console=False, parallel=False)
        #Si = sobol.analyze(pb, YSobol, calc_second_order=False, conf_level=0.95,
        #                   print_to_console=False, parallel=False)
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

        fit= fitness(Y, pred)

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
            if (re.findall(r'\b%s\b' % re.escape(i), line)):
                table.append(1)
            elif v == i:
                table.append(-1)
            else:
                table.append(0)
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

        self.computeInitialPos()
        self.computeFitandCmplxEdgeColor()
        self.computeComprEdgeColor()
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
            cmap = self.colors.get("Pearson", 1 - v)
            lcmap = list(np.array(cmap) / 255)
            lcmap.extend([1.0])
            self.edgeColorPearson[e] = lcmap

    #TODO Vérif fonctionnement
    def createConstraintsGraph(self):
        ctgraph = ClassGraph()
        try:
            node_edge = None
            nodes = {}
            with open(self.dataset.ctmod) as f:
                for _ in f:
                    if _.startswith('nodes'):
                        node_edge = True
                        continue
                    if _.startswith('edges'):
                        node_edge = False
                        continue
                    if node_edge == True:
                        node, *names = _.strip().split(" ")
                        cn  = ClassNode(node,names)
                        ctgraph.add_node(cn)
                        nodes[node] = cn
                    if node_edge == False:
                        nNode = _.strip().split(" ")
                        ctgraph.add_edge(nodes[nNode[0]], nodes[nNode[1]])

        except FileNotFoundError as fnf :
            print("file error : {}".format(fnf))

        return ctgraph

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
        elif (self.ColorMode == 'SA'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorSA)
        elif (self.ColorMode == 'Pearson'):
            self.edgeColorfull = copy.deepcopy(self.edgeColorPearson)
        for i in range(len(self.pareto)):  # i is child
            for j in range(len(self.pareto[i])):  # j is parent
                lIdxColPareto = self.pareto[i][j]
                if (len(lIdxColPareto) > 0):  # il ne s'agit pas d'une variable d'entrée qui n'a pas de front de pareto
                    r = self.adj_simple[i, j] / self.nbeq[i]  # Rapport entre le nombre de fois que j intervient dans i par rapport au nombre d'équations dans i
                    tup = (self.dataset.varnames[j], self.dataset.varnames[i])
                    if (self.ColorMode!='Pearson' and r <= self.adjThresholdVal):
                        self.invisibleTup.append(tup)
                    elif(self.ColorMode=='Pearson' and  -1+self.adjThresholdVal < self.allPearson[tup] < 1-self.adjThresholdVal ):
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
            except:
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

        for e in self.edgeColorSA.keys():
            v=self.edgeColorSA[e]
            cmap = self.colors.get("SA", 1-v)
            lcmap = list(np.array(cmap) / 255)
            lcmap.extend([1.0])
            self.edgeColorSA[e]=lcmap
        print('it worked ?')

#TODO pos normalement inutile ?
    def computeInitialPos(self):
        G=nx.DiGraph()
        G.clear()
        for v in self.dataset.varnames:
            G.add_node(v)
        ed=[]
        for i in range(len(self.pareto)):
            for j in range(len(self.pareto[i])):
                for k in range(len(self.adj_contrGraph.nodes())):
                    if self.adj_contrGraph.nodes()[k].name == self.dataset.variablesClass[self.dataset.varnames[j]]:
                        jClass=self.adj_contrGraph.nodes()[k]
                    if self.adj_contrGraph.nodes()[k].name == self.dataset.variablesClass[self.dataset.varnames[i]]:
                        iClass=self.adj_contrGraph.nodes()[k]
                if self.adj_contrGraph.has_edge(jClass, iClass):
                    ed.append((self.dataset.varnames[j], self.dataset.varnames[i]))
                    G.add_edge(self.dataset.varnames[j], self.dataset.varnames[i],
                                    adjsimple=self.adj_simple[i, j], adjfit=
                                    self.adj_fit[i, j], adjcmplx=self.adj_cmplx[i, j],
                                    adjcontr=self.adj_contr[i, j])
        self.pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
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