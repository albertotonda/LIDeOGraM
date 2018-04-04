import random
import sys
sys.path.append("fitness/")
import fitness
from deap import base
from deap import creator
from deap import tools
#from deap import algorithms
from myEAalgorithms import *
import numpy as np
from sklearn import linear_model
from scipy.special import binom
from math import log


class equaOptim:

    def __init__(self,X,Y,nbElmt):
        self.X=X
        self.Y=Y
        self.nbElmt=nbElmt
        nbVar=self.X.shape[1]
        self.nvars = nbVar

    def initIndividual(self,indv,nbElmt):
        nbVar=self.X.shape[1]
        vect=np.zeros(nbVar)
        elmtOne=random.sample(range(nbVar),nbElmt)
        vect[elmtOne]=1
        return indv(vect)

    def crossover(self,indv1,indv2):



        OneVectIndv1=np.argwhere(np.array(indv1)==1).flatten()
        OneVectIndv2=np.argwhere(np.array(indv2)==1).flatten()

        sameOne=[e for e in OneVectIndv1 if  e in OneVectIndv2]
        diffIndv1One=np.array([e for e in OneVectIndv1 if not e in OneVectIndv2])

        diffIndv2One=np.array([e for e in OneVectIndv2 if not e in OneVectIndv1])
        uniformCrossVect = np.random.randint(2, size=len(diffIndv1One))

        child1=np.zeros(len(indv1))
        child2=np.zeros(len(indv1))
        child1[sameOne] = 1
        child2[sameOne] = 1
        try:
            indchild1_1=diffIndv1One[np.argwhere(uniformCrossVect==1).flatten()]
        except:
            indchild1_1=[]
        try:
            indchild1_2=diffIndv2One[np.argwhere(uniformCrossVect==0).flatten()]
        except:
            indchild1_2=[]
        try:
            indchild2_1 = diffIndv2One[np.argwhere(uniformCrossVect == 1).flatten()]
        except:
            indchild2_1=[]
        try:
            indchild2_2 = diffIndv1One[np.argwhere(uniformCrossVect == 0).flatten()]
        except:
            indchild2_2=[]


        child1[list(indchild1_1)]=1
        child1[list(indchild1_2)] = 1
        child2[list(indchild2_1)] = 1
        child2[list(indchild2_2)] = 1

        if(self.nbElmt==5):
            a=10


        for i in range(len(child1)):
            indv1[i]= child1[i]
            indv2[i] = child2[i]

        return (indv1,indv2,)



    def mutation(self,indv):
        idx0 = np.argwhere(np.array(indv) == 0).flatten()
        idx1 = np.argwhere(np.array(indv) == 1).flatten()
        if len(list(idx0)) != 0:
            indv[random.sample(list(idx0), 1)[0]]=1.0
            indv[random.sample(list(idx1), 1)[0]]=0.0

        return (indv,)

    def evaluate(self,indv):
        arrIndv=np.array(indv)
        idx = np.argwhere(arrIndv == 1).flatten()

        reg=linear_model.LinearRegression()
        Xreg=self.X[:, idx]
        reg.fit(Xreg,self.Y)
        pred=reg.predict(Xreg)

        return (fitness(self.Y, pred),)



    def startOptim(self):

        random.seed(123)
        np.random.seed(123)
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("new_individual", self.initIndividual, creator.Individual,self.nbElmt)



        toolbox.register("mate", self.crossover)
        toolbox.register("mutate", self.mutation)
        toolbox.register("select", tools.selTournament, tournsize=2)
        #toolbox.register("select", tools.selRoulette)
        toolbox.register("new_population", tools.initRepeat, list, toolbox.new_individual)
        toolbox.register("evaluate", self.evaluate)

        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        logbook = tools.Logbook()


        NGEN = max(min(int(50*log(binom(self.nvars,self.nbElmt))), 200), 25)
        NGEN = int(NGEN)
        #print(NGEN)
        CXPB = 0.8
        MUTPB = 0.2
        mu =  max(int(log(binom(self.nvars,self.nbElmt))*log(binom(self.nvars,self.nbElmt))),10)
        mu = int(mu)
        lmbd = int(0.8* mu) #800
        #print(mu)
        halloffame = tools.HallOfFame(1)
        pop = toolbox.new_population(n=mu)
        fitnesses = toolbox.map(toolbox.evaluate, pop)
        for ind, fit in list(zip(pop, fitnesses)):
            #print(fit)
            ind.fitness.values = fit
        pop, logbook = eaMuPlusLambda(pop, toolbox, mu, lmbd, CXPB, MUTPB, NGEN, stats=stats,
                                                 halloffame=halloffame,stopping_criteria=0.001, verbose=True)

        return halloffame[0]