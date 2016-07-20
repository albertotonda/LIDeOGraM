"""Computed fitness of solutions."""
import math
import multiprocessing
from multiprocessing.pool import ThreadPool
import numpy as np

from sympy.parsing.sympy_parser import parse_expr


class Equation:
    """Struct to hold node information."""
    def __init__(self, name, eq,cmplx, v):
        self.equation = eq
        self.name = name
        self.variables = v
        self.complexity = cmplx


#TODO: preparse all equations, and apply parameters on evalutation

class Individual:
    """Class to describe the whole system."""
    def __init__(self, modApp, eqfile):  # gestion des noeud orphelins
        """Create and populate nodes dictionary."""
        self.inodes = {}
        self.equations = []
        self.variables = []
        self.exp = {}
        self.complexity = {}
        self.modApp = modApp


        for i in range(len(self.modApp.dataset[0])):
            self.exp[self.modApp.dataset[0,i]]=list(self.modApp.dataset[2:, i])

        for varIn in self.modApp.varsIn:
            self.inodes[varIn] = self.exp[varIn]

        self.variables = list(self.modApp.varnames)
        self.variables.extend(self.inodes.keys())


        pass

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
                equaLines.append(self.modApp.equaPerNode[v][chosenEqs[v]])

        for t in equaLines:
            localvar = []
            for b in self.variables:
                if b in t[3]:
                    localvar.append(b)
            self.equations.append(Equation(t[2], t[3], t[0], localvar))
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
                    result = (parse_expr(eq.equation, local_dict=computed))
                    computed[eq.name] = result
            nnode -= 1
        #if nnode == 0:
            #print("Error in process, variables not found") ATTENTION ERREUR LEVE LORS DE L'EXECUTION !!!
        return computed

    def get_fitness(self,chosenEqs,  fun=(lambda x, y: math.fabs(x - y)/x), penalty=0):
        """match solution against given data."""
        bkeys = self.variables
        ncases = len(self.exp[list(self.inodes.keys())[0]])
        results = []
        for case in range(ncases):
            results.append(self.process(case,chosenEqs))
        var = 0.
        acc = 0
        cpx = 0
        for case in range(ncases):
            for i in bkeys:
                if i in results[case] and i in self.exp:
                    acc+=1
                    if(float(results[case][i])!= float(self.exp[i][case].replace(",","."))):
                        if(float(results[case][i])==0.0):
                            var += fun(float(self.exp[i][case].replace(",", ".")),float(results[case][i]))
                        else:
                            var += fun(float(results[case][i]), float(self.exp[i][case].replace(",", ".")))
                else:
                    #Si un noeuds présent dans les données n'est pas calcul par le systeme on ajoute une penalité
                    #Option non utilisé (normalement)
                    var += penalty
                    raise NotImplementedError
        for i in bkeys:
            if i in self.complexity:
                cpx += self.complexity[i]
        return var/acc, cpx

def get_multithread_fitness(var,exps,initv):
    tasks = [Individual(initv,var,exp) for exp in exps]
    p = ThreadPool.Pool(multiprocessing.cpu_count())
    xs = p.map(lambda x : x.get_fitness(), tasks)
    return xs


if __name__ == "__main__":
    i = Individual("params.csv", "ex_indiv.csv", "varnames.csv")
    print(i.get_fitness())
