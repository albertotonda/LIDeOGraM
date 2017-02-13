import pickle
from deap import base
from deap import creator
from deap import tools
import matplotlib.pyplot as plt



with open('logbook.dat','rb') as f:
    logbook=pickle.load(f)

popfitnesses=logbook.select("popfitnesses")
print(logbook)

flatPopFit=[]
for popGenI in popfitnesses:
    p=[]
    for indFit in popGenI:
        p.append(indFit[0])
    flatPopFit.append(p)

gen = logbook.select("gen")
fit_avgs = logbook.select("avg")
fit_stds = logbook.select("std")
fit_mins = logbook.select("min")
fit_maxs = logbook.select("max")

fig, ax1 = plt.subplots()
ax1.plot(gen, fit_mins, "g-", label="Minimum Fitness")
ax1.plot(gen, fit_avgs, "y-", label="Average Fitness")
#ax1.plot(gen, fit_stds, "k-", label="Std Fitness")
ax1.plot(gen, fit_maxs, "r-", label="Maximum Fitness")
for i in range(len(flatPopFit)):
    ax1.plot([i]*len(flatPopFit[i]),flatPopFit[i],"*")
ax1.set_xlabel("Generation")
ax1.set_ylabel("Fitness")
for tl in ax1.get_yticklabels():
    tl.set_color("b")
plt.show()