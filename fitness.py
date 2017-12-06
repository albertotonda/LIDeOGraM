"""Computed fitness of solutions."""
import math
import multiprocessing
from multiprocessing.pool import ThreadPool
import numpy as np
from scipy.stats.stats import pearsonr
from scipy import stats
from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sklearn.metrics import r2_score

class Equation:
    """Struct to hold node information."""
    def __init__(self, name, eq,cmplx, v,computedEq):
        self.equation = eq
        self.name = name
        self.variables = v
        self.complexity = cmplx
        self.computedEq = computedEq



#TODO: preparse all equations, and apply parameters on evalutation

class Individual:
    """Class to describe the whole system."""
    def __init__(self, modApp):  # gestion des noeud orphelins
        """Create and populate nodes dictionary."""
        self.inodes = {}
        self.equations = []
        self.variables = []
        self.exp = {}
        self.complexity = {}
        self.modApp = modApp


        for v in self.modApp.dataset.varnames:
            self.exp[v]=list(self.modApp.dataset.getAllExpsforVar(v))

        for varIn in self.modApp.varsIn:
            self.inodes[varIn] = self.exp[varIn]

        self.variables = list(self.modApp.dataset.varnames)




    def process(self, n: int,chosenEqs={}):
        """Take example i and compute solution.
        :type n: int
        """
        computed = {}
        # computed = {k : v[i] for (k,v) in self.inodes}
        for k in self.inodes.keys():
            computed[k] = float(self.inodes[k][n])

        equaLines=[]
        for v in chosenEqs.keys():
            if(not v in self.modApp.varsIn):
                idxs=np.logical_and(self.modApp.equacolO[:, 4] == True , self.modApp.equacolO[:, 2] == v)
                equaLines.append(self.modApp.equacolO[idxs][chosenEqs[v]])

        for t in equaLines:
            localvar = []
            for b in self.variables:
                if b in t[3]:
                    localvar.append(b)
            self.equations.append(Equation(t[2], t[3], t[0], localvar, t[4]))
            self.complexity[t[2]] = float(t[0])

        # computed = self.inodes  # "Age" : value ...
        neq = len(self.equations)
        nnode = len(self.variables)  # Eviter les boules infinies
        while neq and nnode:
            for eq in self.equations:
                if eq.name not in computed.keys() and set(eq.variables).issubset(set(computed.keys()))  :
                    # Attention ensemble vide inclus dans n'importe quel autre ensemble !
                    neq -= 1
                    eq.equation=eq.equation.replace("^","**")
                    result = (parse_expr(eq.equation, local_dict=computed))
                    computed[eq.name] = result
            nnode -= 1
        #if nnode == 0:
            #print("Error in process, variables not found") ATTENTION ERREUR LEVE LORS DE L'EXECUTION !!!
        return computed

    def get_fitness(self, chosenEqs, fun=(lambda x, y: math.fabs(x - y)/math.fabs(x)), penalty=0):
    #def get_fitness(self,chosenEqs,  fun=(lambda x, y: np.maximum(math.fabs(x / y),math.fabs(y / x))), penalty=0):
        """match solution against given data."""
        bkeys = self.variables
        ncases = len(self.exp[list(self.inodes.keys())[0]])
        results = []
        for case in range(ncases):
            results.append(self.process(case,chosenEqs))
        acc = 0
        cpx = 0
        errVarSum = {}
        errTot=0
        for i in range(len(bkeys)):  # For all variables in the data
            if(not(bkeys[i] in self.modApp.varsIn)):
                errVarSum[bkeys[i]]=0
                xr=[]
                yr=[]
                for j in range(len(results)):
                 if bkeys[i] in results[case] and bkeys[i] in self.exp:
                     try:
                        yr.append(float(results[j][bkeys[i]]))
                     except:
                        yr.append(np.nan)
                     try:
                        xr.append(float(self.exp[bkeys[i]][j]))
                     except:
                        xr.append(np.nan)
                acc+=1
                if( not np.nan in xr and not np.nan in yr):
                    errVarSum[bkeys[i]]=fitness(xr, yr)
                else:
                    errVarSum[bkeys[i]] = 1
                    #errVarSum[bkeys[i]] = p
                #if(bkeys[i] != 'C150' and bkeys[i] != 'C181trans'):
                errTot+=errVarSum[bkeys[i]]
        errTot=errTot/(len(bkeys)-len(self.modApp.varsIn))
        for i in bkeys:
         if i in self.complexity and not i in self.modApp.varsIn:
             cpx += self.complexity[i]
        return errTot, cpx ,errVarSum, self.complexity


class Individual_true:
    """Class to describe the whole system."""
    def __init__(self, modApp, truth):  # gestion des noeud orphelins
        """Create and populate nodes dictionary."""
        self.inodes = {}
        self.equations = []
        self.variables = []
        self.exp = {}
        self.complexity = {}
        self.varsIn = "Temperature,Diametre,MasseMolaire,Masse,Taille_part,Energie".split(",")
        self.modApp = modApp

        for v in truth.columns:
            self.exp[v]=list(truth[v])

        for varIn in self.varsIn:
            self.inodes[varIn] = self.exp[varIn]

        self.variables = list(self.modApp.dataset.varnames)

    def process(self, n: int,chosenEqs: dict):
        """Take example i and compute solution.
        :type n: int
        """
        computed = {}
        for k in self.inodes.keys():
            computed[k] = float(self.inodes[k][n])

        equaLines=[]
        for v in chosenEqs.keys():
            if(not v in self.varsIn):
                idxs=np.logical_and(self.modApp.equacolO[:, 4] == True , self.modApp.equacolO[:, 2] == v)
                equaLines.append(self.modApp.equacolO[idxs][chosenEqs[v]])

        for t in equaLines:
            localvar = []
            for b in self.variables:
                if b in t[3]:
                    localvar.append(b)
            self.equations.append(Equation(t[2], t[3], t[0], localvar, t[4]))
            self.complexity[t[2]] = float(t[0])

        # computed = self.inodes  # "Age" : value ...
        neq = len(self.equations)
        nnode = len(self.variables)  # Eviter les boules infinies
        while neq and nnode:
            for eq in self.equations:
                if eq.name not in computed.keys() and set(eq.variables).issubset(set(computed.keys()))  :
                    # Attention ensemble vide inclus dans n'importe quel autre ensemble !
                    neq -= 1
                    eq.equation=eq.equation.replace("^","**")
                    result = (parse_expr(eq.equation, local_dict=computed))
                    computed[eq.name] = result
            nnode -= 1
        #if nnode == 0:
            #print("Error in process, variables not found") ATTENTION ERREUR LEVE LORS DE L'EXECUTION !!!
        return computed

    def get_fitness(self, chosenEqs, fun=(lambda x, y: math.fabs(x - y)/math.fabs(x)), penalty=0):
    #def get_fitness(self,chosenEqs,  fun=(lambda x, y: np.maximum(math.fabs(x / y),math.fabs(y / x))), penalty=0):
        """match solution against given data."""
        bkeys = self.variables
        ncases = len(self.exp[list(self.inodes.keys())[0]])
        results = []
        for case in range(ncases):
            results.append(self.process(case,chosenEqs))
        acc = 0
        cpx = 0
        errVarSum = {}
        errTot=0
        for i in range(len(bkeys)):  # For all variables in the data
            if(not(bkeys[i] in self.modApp.varsIn)):
                errVarSum[bkeys[i]]=0
                xr=[]
                yr=[]
                for j in range(len(results)):
                 if bkeys[i] in results[case] and bkeys[i] in self.exp:
                     try:
                        yr.append(float(results[j][bkeys[i]]))
                     except:
                        yr.append(np.nan)
                     try:
                        xr.append(float(self.exp[bkeys[i]][j]))
                     except:
                        xr.append(np.nan)
                acc+=1
                if( not np.nan in xr and not np.nan in yr):
                    errVarSum[bkeys[i]]=fitness(xr, yr)
                else:
                    errVarSum[bkeys[i]] = 1
                    #errVarSum[bkeys[i]] = p
                #if(bkeys[i] != 'C150' and bkeys[i] != 'C181trans'):
                errTot+=errVarSum[bkeys[i]]
        errTot=errTot/(len(bkeys)-len(self.modApp.varsIn))
        for i in bkeys:
         if i in self.complexity and not i in self.modApp.varsIn:
             cpx += self.complexity[i]
        return errTot, cpx ,errVarSum, self.complexity


def fitness(xr,yr):
    allEqual = True
    for yri in range(len(yr) - 1):
        allEqual = allEqual and yr[yri] == yr[yri + 1]
    if (allEqual):
        fit = 1
    else:
        linslope, intercept, r_value, p_value, std_err = stats.linregress(list(map(float, xr)), list(map(float, yr)))
        if (linslope > 1):
            directionErr = 1 / linslope
        else:
            directionErr = linslope
        # errVarSum[bkeys[i]]=1-(pearsonr(xr,yr)[0]*directionErr)
        # errVarSum[bkeys[i]] = 1 - (np.maximum(pearsonr(xr, yr)[0],0) * directionErr)
        # errVarSum[bkeys[i]] = 1 - (np.maximum(pearsonr(xr, yr)[0], 0) )
        # errVarSum[bkeys[i]] = 1 - pearsonr(xr, yr)[0]
        p = pearsonr(list(map(float, xr)), list(map(float, yr)))[0]
        if (p > 0):
            fit = 1 - p * directionErr
        else:
            fit = 1 + p * directionErr
    return fit

def fitnessr2(xr,yr):
    return 1 - r2_score(list(map(float, xr)), list(map(float, yr)))



if __name__ == "__main__":
    i = Individual("params.csv", "ex_indiv.csv", "varnames.csv")
    print(i.get_fitness())
