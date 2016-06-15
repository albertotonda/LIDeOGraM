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

        for eq in open(eqfile, 'r'):
            try:
                self.variables.append([u.strip() for u in eq.split(",")][2])
            except IndexError:
                pass
        self.variables.extend(self.inodes.keys())

        for eq in open(eqfile, 'r'):
            t = [k.strip() for k in eq.split(",")]
            localvar = []
            for b in self.variables:
                if b in t[3]:
                    localvar.append(b)
            self.equations.append(Equation(t[2] ,t[3] ,t[0], localvar))
            self.complexity[t[2]] = float(t[0])


    def process(self, n: int):
        """Take example i and compute solution.
        :type n: int
        """
        computed = {}
        # computed = {k : v[i] for (k,v) in self.inodes}
        for k in self.inodes.keys():
            computed[k] = self.inodes[k][n]
        # computed = self.inodes  # "Age" : value ...
        neq = len(self.equations)
        nnode = len(self.variables)  # Eviter les boules infinies
        while neq and nnode:
            for eq in self.equations:
                if eq.name not in computed.keys() and set(eq.variables).issubset(set(computed.keys()))  :
                    #Attention ensemble vide inclus dans n'importe quel autre ensemble !
                    neq -= 1
                    result = (parse_expr(eq.equation.replace("^","**"), local_dict=computed))
                    computed[eq.name] = result
            nnode -= 1
        if nnode == 0:
            print("Error in process, variables not found")
        return computed

    def get_fitness(self, fun=(lambda x, y: math.fabs(x - y)/x), penalty=0):
        """match solution against given data."""
        bkeys = self.variables
        ncases = len(self.exp[list(self.inodes.keys())[0]])
        results = []
        for case in range(ncases):
            results.append(self.process(case))
        var = 0.
        acc = 0
        cpx = 0
        for case in range(ncases):
            for i in bkeys:
                if i in results[case] and i in self.exp:
                    acc+=1
                    var += fun(float(results[case][i]), float(self.exp[i][case].replace(",",".")))
                else:
                    #Si un noeuds présent dans les données n'est pas calcul par le systeme on ajoute une penalité
                    var += penalty
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
