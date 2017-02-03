"""Computed fitness of solutions."""
import math
import multiprocessing
from multiprocessing.pool import ThreadPool
import numpy as np
from scipy.stats.stats import pearsonr
from scipy import stats
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

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
    def __init__(self, modApp, eq):  # gestion des noeud orphelins
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
                try:
                    equaLines.append(self.modApp.equaPerNode[v][chosenEqs[v]])
                except:
                    pass
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
                    #Attention ensemble vide inclus dans n'importe quel autre ensemble !
                    neq -= 1
                    eq.equation=eq.equation.replace("^","**")
                    #eq.equation=eq.equation.replace(".",",")
                    #result = eq.computedEq.evalf(subs=computed)
                    #result = lambdify(computed,eq.computedEq)
                    #symbols = tuple(eq.computedEq.free_symbols)
                    #lbd = lambdify(symbols, eq.computedEq)
                    result = (parse_expr(eq.equation, local_dict=computed))
                    computed[eq.name] = result
            nnode -= 1
        #if nnode == 0:
            #print("Error in process, variables not found") ATTENTION ERREUR LEVE LORS DE L'EXECUTION !!!
        return computed

    def get_fitness(self,chosenEqs,  fun=(lambda x, y: math.fabs(x - y)/math.fabs(x)), penalty=0):
    #def get_fitness(self,chosenEqs,  fun=(lambda x, y: np.maximum(math.fabs(x / y),math.fabs(y / x))), penalty=0):
        """match solution against given data."""
        bkeys = self.variables
        ncases = len(self.exp[list(self.inodes.keys())[0]])
        results = []
        for case in range(ncases):
            results.append(self.process(case,chosenEqs))
        var = 0.
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
                     yr.append(float(results[j][bkeys[i]]))
                     xr.append(float(self.exp[bkeys[i]][j]))
                acc+=1
                errVarSum[bkeys[i]]= fitness(xr,yr) #np.sum(fun(np.array(xr), np.array(yr)))
                errTot+=errVarSum[bkeys[i]]

        for i in bkeys:
         if i in self.complexity and not i in self.modApp.varsIn:
             cpx += self.complexity[i]
        return errTot, cpx ,errVarSum

def get_multithread_fitness(var,exps,initv):
    tasks = [Individual(initv,var,exp) for exp in exps]
    p = ThreadPool.Pool(multiprocessing.cpu_count())
    xs = p.map(lambda x : x.get_fitness(), tasks)
    return xs

def fitness(xr,yr):
    allEqual = True
    for yri in range(len(yr) - 1):
        allEqual = allEqual and yr[yri] == yr[yri + 1]
    if (allEqual):
        fit = 1
    else:
        linslope, intercept, r_value, p_value, std_err = stats.linregress(xr, yr)
        if (linslope > 1):
            directionErr = 1 / linslope
        else:
            directionErr = linslope
        # errVarSum[bkeys[i]]=1-(pearsonr(xr,yr)[0]*directionErr)
        # errVarSum[bkeys[i]] = 1 - (np.maximum(pearsonr(xr, yr)[0],0) * directionErr)
        # errVarSum[bkeys[i]] = 1 - (np.maximum(pearsonr(xr, yr)[0], 0) )
        # errVarSum[bkeys[i]] = 1 - pearsonr(xr, yr)[0]
        p = pearsonr(xr, yr)[0]
        if (p > 0):
            fit = 1 - p * directionErr
        else:
            fit = 1 + p * directionErr
    return fit

def get_multithread_fitness(var,exps,initv):
    tasks = [Individual(initv,var,exp) for exp in exps]
    p = ThreadPool.Pool(multiprocessing.cpu_count())
    xs = p.map(lambda x : x.get_fitness(), tasks)
    return xs


if __name__ == "__main__":
    i = Individual("params.csv", "ex_indiv.csv", "varnames.csv")
    print(i.get_fitness())
