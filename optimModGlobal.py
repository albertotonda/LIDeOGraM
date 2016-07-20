import random
import sys
sys.path.append("fitness/")
import fitness
from deap import base
from deap import creator
from deap import tools



class OptimModGlobal:


    def __init__(self,modApp):
        self.modApp = modApp

    def initIndividual(self,indv, sizes):
        vect = []
        for size_i in sizes:
            if (size_i - 1 > 0):
                vect.append(random.randint(0, size_i - 1))
            else:
                vect.append(-1)
        return indv(vect)

    def evaluate(self,indv):
        ft = fitness.Individual(self.modApp, "fitness/ex_indiv.csv")
        indvDict={}
        for i in range(len(self.modApp.varnames)):
            indvDict[self.modApp.varnames[i]]=indv[i]
        res = ft.get_fitness(indvDict)
        return (res[0],)

    def mutEqua(self,indv, probmut):
        for i in range(len(indv)):
            if (random.random() < probmut):
                if (self.sizes[i] - 1 < 1):
                    indv[i] = -1
                else:
                    indv[i] = random.randint(0, self.sizes[i] - 1)

    def startOptim(self):
        random.seed()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.sizes=[]
        for v,s in self.modApp.varEquasize:
            self.sizes.append(s)

        toolbox = base.Toolbox()
        toolbox.register("new_individual",self.initIndividual,creator.Individual,self.sizes)
        toolbox.register("mate",tools.cxUniform,indpb=0.5)
        toolbox.register("mutate",self.mutEqua,probmut=0.25)
        toolbox.register("select",tools.selTournament,tournsize=3)
        toolbox.register("new_population",tools.initRepeat,list,toolbox.new_individual)
        toolbox.register("evaluate",self.evaluate)


        NGEN=100
        CXPB=0.8
        MUTPB=0.1
        pop=toolbox.new_population(n=100)
        fitnesses=toolbox.map(toolbox.evaluate, pop)
        for ind, fit in list(zip(pop, fitnesses)):
            ind.fitness.values = fit
        for g in range(NGEN):
            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            #print(offspring)
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover on the offspring
            #print(list(offspring))
            #print(offspring[::2])
            #print(offspring[1::2])
            #print(zip(offspring[::2], offspring[1::2]))
            for child1, child2 in list(zip(offspring[::2], offspring[1::2])):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # Apply mutation on the offspring
            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in list(zip(invalid_ind, fitnesses)):
                ind.fitness.values = fit

            # The population is entirely replaced by the offspring
            pop[:] = offspring
            print(g)
        print(self.sizes)
        print(pop)