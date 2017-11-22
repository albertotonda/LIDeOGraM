import random
import sys
sys.path.append("fitness/")
import fitness
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy as np
import pickle


class OptimModGlobal:


    def __init__(self,modApp):
        self.modApp = modApp

    def initIndividual(self,indv, sizes):
        vect = []
        for size_i in sizes:
            if (size_i > 0):
                vect.append(random.randint(0, size_i - 1))
            else:
                vect.append(-1)
        return indv(vect)

    def evaluate(self,indv):
        ft = fitness.Individual(self.modApp)
        indvDict={}
        for i in range(len(self.modApp.dataset.varnames)):
            indvDict[self.modApp.dataset.varnames[i]]=indv[i]
        try:
            res = ft.get_fitness(indvDict)
        except:
            res = ft.get_fitness(indvDict)
        return (res[0],)

    def mutEqua(self,indv, probmut):
        for i in range(len(indv)):
            if (random.random() < probmut):
                if (self.sizes[i]  < 1):
                    indv[i] = -1
                else:
                    indv[i] = random.randint(0, self.sizes[i] - 1)

    def mutEqua2(self, indv, probmut,sizes):
        for i in range(len(indv)):
            if (random.random() < probmut):
                if (sizes[i] < 1):
                    indv[i] = -1
                else:
                    if sizes[i] > 1 :
                        if (indv[i]==0):
                            indv[i] = 1
                        elif (indv[i]==sizes[i]-1):
                            indv[i] = int(sizes[i]-2)
                        else:
                            indv[i] = indv[i] + random.randint(0,1)*2-1
        return (indv,)


    def startOptim(self):




        random.seed()

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.sizes=[]
        for v,s in self.modApp.varEquasizeOnlyTrue.items():
            self.sizes.append(s)

        toolbox = base.Toolbox()
        toolbox.register("new_individual",self.initIndividual,creator.Individual,self.sizes)
        toolbox.register("mate",tools.cxUniform,indpb=0.5)
        toolbox.register("mutate",self.mutEqua2,probmut=0.05,sizes=self.sizes)
        toolbox.register("select",tools.selTournament,tournsize=2)
        toolbox.register("new_population",tools.initRepeat,list,toolbox.new_individual)
        toolbox.register("evaluate",self.evaluate)

        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        logbook = tools.Logbook()

        #with open('bestIndv.dat', 'rb') as f:
        #with open('bestIndv_soussurexpr2.dat', 'rb') as f:
        #with open('bestIndv_soussurexpr_evoExp1_nomol.dat', 'rb') as f:
        #with open('bestIndv_soussurexpr_evoNoExp1.dat', 'rb') as f:
        #with open('testOptim/bestIndv_soussurexpr_evoExp1.dat', 'rb') as f:
        #    ret = pickle.load(f)
        #return ret

        #with open('fitEvo1.dat', 'rb') as f:
        #    r = pickle.load(f)

        #print('r:\n'+r)
        NGEN=10
        CXPB=0.8
        MUTPB=0.2
        mu=50
        lmbd=40
        halloffame=tools.HallOfFame(1)
        pop=toolbox.new_population(n=mu)
        fitnesses=toolbox.map(toolbox.evaluate, pop)
        for ind, fit in list(zip(pop, fitnesses)):
            print(fit)
            ind.fitness.values = fit
        pop,logbook=algorithms.eaMuPlusLambda(pop,toolbox,mu,lmbd,CXPB,MUTPB,NGEN,stats=stats,halloffame=halloffame,verbose=True)
        pass
        # record = stats.compile(pop)
        # popfit = [ind.fitness.values for ind in pop]
        # logbook.record(gen=0, evals=mu, popfitnesses=popfit,pop=pop,**record)
        # for g in range(NGEN):
        #     # Select the next generation individuals
        #     offspring = toolbox.select(pop, lmbd)
        #     # Clone the selected individuals
        #     #print(offspring)
        #     offspring = list(map(toolbox.clone, offspring))
        #
        #     # Apply crossover on the offspring
        #     #print(list(offspring))
        #     #print(offspring[::2])
        #     #print(offspring[1::2])
        #     #print(zip(offspring[::2], offspring[1::2]))
        #     for child1, child2 in list(zip(offspring[::2], offspring[1::2])):
        #         if random.random() < CXPB:
        #             toolbox.mate(child1, child2)
        #             del child1.fitness.values
        #             del child2.fitness.values
        #
        #     # Apply mutation on the offspring
        #     for mutant in offspring:
        #         if random.random() < MUTPB:
        #             toolbox.mutate(mutant)
        #             del mutant.fitness.values
        #
        #     # Evaluate the individuals with an invalid fitness
        #     invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        #     fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        #     for ind, fit in list(zip(invalid_ind, fitnesses)):
        #         ind.fitness.values = fit
        #
        #     # The population is entirely replaced by the offspring
        #     pop[:] = offspring
        #     record = stats.compile(pop)
        #     popfit=[ind.fitness.values for ind in pop]
        #     logbook.record(gen=g+1, evals=mu+(g+14)*lmbd,popfitnesses=popfit,pop=pop, **record)
        #     with open('logbook.dat','wb') as f:
        #         pickle.dump(logbook,f)
        #     print(g)
        #     logbook.header = "gen", "evals", "avg", "std", "min", "max"
        #     print(logbook)
        # print(self.sizes)
        # print(pop)
        # logbook.header = "gen", "evals", "avg", "std", "min", "max"
        # print(logbook)

        gen = logbook.select("gen")
        fit_avgs = logbook.select("avg")
        fit_stds = logbook.select("std")
        fit_mins = logbook.select("min")
        fit_maxs = logbook.select("max")


        # import matplotlib.pyplot as plt
        #
        # fig, ax1 = plt.subplots()
        # ax1.plot(gen, fit_mins, "g-", label="Minimum Fitness")
        # ax1.plot(gen, fit_avgs, "y-", label="Average Fitness")
        # ax1.plot(gen, fit_stds, "k-", label="Std Fitness")
        # ax1.plot(gen, fit_maxs, "r-", label="Maximum Fitness")
        # ax1.set_xlabel("Generation")
        # ax1.set_ylabel("Fitness")
        # for tl in ax1.get_yticklabels():
        #     tl.set_color("b")
        # fig.show()


        with open('fitEvolNoExpNoMol10.dat','wb') as f:
            pickle.dump([fit_mins,fit_avgs,fit_stds,fit_maxs],f)

        #popfitnesses = logbook.select("popfitnesses")
        #flatPopFit = []
        #for popGenI in popfitnesses:
        #    p = []
        #    for indFit in popGenI:
        #        p.append(indFit[0])
        #    flatPopFit.append(p)



        bestindvDict = {}
        for i in range(len(self.modApp.dataset.varnames)):
            bestindvDict[self.modApp.dataset.varnames[i]] = halloffame[0][i]
            #bestindvDict[self.modApp.dataset.varnames[i]] = pop[np.argmin(flatPopFit[-1])][i]
        #with open('retOptim.dat', 'wb') as f:
        #    pickle.dump(pop[np.argmin(flatPopFit[-1])], f)

        #bestindvDict=[]

        with open('bestIndv_soussurexpr_evoNoExpNoMol10.dat', 'wb') as f:
            pickle.dump(bestindvDict, f)

        return bestindvDict

