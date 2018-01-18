import random
import sys

sys.path.append("fitness/")
import fitness
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import numpy as np
import logging
from time import strftime
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal, QCoreApplication


class OptimModGlobal(QWidget):
    update_bar_signal = pyqtSignal(int)
    def __init__(self, modApp):
        QWidget.__init__(self)
        self.modApp = modApp


    def initIndividual(self, indv, sizes):
        vect = []
        for size_i in sizes:
            if (size_i > 0):
                vect.append(random.randint(0, size_i - 1))
                # random.randint(a, b)
                # Return a random integer N such that a <= N <= b. Alias for randrange(a, b+1).
            else:
                vect.append(-1)
        return indv(vect)

    def evaluate(self, indv):
        ft = fitness.Individual(self.modApp)
        indvDict = {}
        for i in range(len(self.modApp.dataset.varnames)):
            indvDict[self.modApp.dataset.varnames[i]] = indv[i]
        try:
            res = ft.get_fitness(indvDict)
        except:
            res = ft.get_fitness(indvDict)
        return (res[0],)

    def mutEqua(self, indv, probmut):
        for i in range(len(indv)):
            if (random.random() < probmut):
                if (self.sizes[i] < 1):
                    indv[i] = -1
                else:
                    indv[i] = random.randint(0, self.sizes[i] - 1)

    def mutEqua2(self, indv, probmut, sizes):
        for i in range(len(indv)):
            if (random.random() < probmut):
                if (sizes[i] < 1):
                    indv[i] = -1
                else:
                    if sizes[i] > 1:
                        if (indv[i] == 0):
                            indv[i] = 1
                        elif (indv[i] == sizes[i] - 1):
                            indv[i] = int(sizes[i] - 2)
                        else:
                            indv[i] = indv[i] + random.randint(0, 1) * 2 - 1
        return (indv,)

    def startOptim(self):

        random.seed()

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.sizes = []
        for v, s in self.modApp.varEquasizeOnlyTrue.items():
            self.sizes.append(s)

        toolbox = base.Toolbox()
        toolbox.register("new_individual", self.initIndividual, creator.Individual, self.sizes)
        toolbox.register("mate", tools.cxUniform, indpb=0.5)
        toolbox.register("mutate", self.mutEqua2, probmut=0.05, sizes=self.sizes)
        toolbox.register("select", tools.selTournament, tournsize=2)
        toolbox.register("new_population", tools.initRepeat, list, toolbox.new_individual)
        toolbox.register("evaluate", self.evaluate)

        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        stats.register("all", lambda x: list(x))

        NGEN = 2
        CXPB = 0.8
        MUTPB = 0.2
        mu = 2
        lmbd = 2
        halloffame = tools.HallOfFame(1)
        pop = toolbox.new_population(n=mu)
        fitnesses = toolbox.map(toolbox.evaluate, pop)
        for ind, fit in list(zip(pop, fitnesses)):
            print(fit)
            ind.fitness.values = fit

        evolutionlog = tools.Logbook()

        for gen in range(NGEN):
            pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, mu, lmbd, CXPB, MUTPB, 1, stats=stats,
                                                     halloffame=halloffame, verbose=1)
            evolutionlog.record(gen=gen, book=logbook)
            self.update_bar_signal.emit(int(100*float(gen)/(NGEN-1)))
            QCoreApplication.processEvents()

        fit_alls = logbook.select("all")

        logging.info("Global search finished {} -- {}".format(strftime("%d%m%y%H%M%S"), strftime("%d %m %y: %H %M %S")))
        with open(strftime("%d%m%y%H%M%S"), 'w') as output:
            for _ in fit_alls:
                output.write(str(_))
                output.write("\n")

        bestindvDict = {}
        for i in range(len(self.modApp.dataset.varnames)):
            bestindvDict[self.modApp.dataset.varnames[i]] = halloffame[0][i]

        return bestindvDict
