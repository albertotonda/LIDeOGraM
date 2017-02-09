import matplotlib.pyplot as plt
import pickle
import numpy as np

fit_mins=[]
fit_avgs=[]
fit_stds=[]
fit_maxs=[]


#
with open('fitEvol1Exp.dat', 'rb') as f:
     ret = pickle.load(f)
fit_mins.append(ret[0])
fit_avgs.append(ret[1])
fit_stds.append(ret[2])
fit_maxs.append(ret[3])
for i in [2,3,4,5,6,7,8,9,10]:
    with open('fitEvolExp'+str(i)+'.dat', 'rb') as f:
        ret = pickle.load(f)
    gen=range(len(ret[0]))
    fit_mins.append(ret[0])
    fit_avgs.append(ret[1])
    fit_stds.append(ret[2])
    fit_maxs.append(ret[3])

# for i in [1,2,3,4,5,6,7,8,9,10]:
#     with open('fitEvolNoExp'+str(i)+'.dat', 'rb') as f:
#         ret = pickle.load(f)
#     gen=range(len(ret[0]))
#     fit_mins.append(ret[0])
#     fit_avgs.append(ret[1])
#     fit_stds.append(ret[2])
#     fit_maxs.append(ret[3])

fit_mins_med=np.median(fit_mins,axis=0)
fit_avgs_med=np.median(fit_avgs,axis=0)
fit_maxs_med=np.median(fit_maxs,axis=0)
fit_mins_q1=np.percentile(fit_mins,25,axis=0)
fit_avgs_q1=np.percentile(fit_avgs,25,axis=0)
fit_maxs_q1=np.percentile(fit_maxs,25,axis=0)
fit_mins_q3=np.percentile(fit_mins,75,axis=0)
fit_avgs_q3=np.percentile(fit_avgs,75,axis=0)
fit_maxs_q3=np.percentile(fit_maxs,75,axis=0)
minExp=fit_mins_med

fit_mins=[]
fit_avgs=[]
fit_stds=[]
fit_maxs=[]

for i in [1,2,3,4,5,6,7,8,9,10]:
    with open('fitEvolNoExp'+str(i)+'.dat', 'rb') as f:
        ret = pickle.load(f)
    gen=range(len(ret[0]))
    fit_mins.append(ret[0])
    fit_avgs.append(ret[1])
    fit_stds.append(ret[2])
    fit_maxs.append(ret[3])

fit_mins_med=np.median(fit_mins,axis=0)
fit_avgs_med=np.median(fit_avgs,axis=0)
fit_maxs_med=np.median(fit_maxs,axis=0)
fit_mins_q1=np.percentile(fit_mins,25,axis=0)
fit_avgs_q1=np.percentile(fit_avgs,25,axis=0)
fit_maxs_q1=np.percentile(fit_maxs,25,axis=0)
fit_mins_q3=np.percentile(fit_mins,75,axis=0)
fit_avgs_q3=np.percentile(fit_avgs,75,axis=0)
fit_maxs_q3=np.percentile(fit_maxs,75,axis=0)
minNoExp=fit_mins_med
fig, ax1 = plt.subplots()
ax1.set_title("Fitness across generations")
ax1.plot(gen, minNoExp, "g-", label="Median Fitness without Expertise",linewidth=2)
ax1.plot(gen, minExp, "b-", label="Median Fitness with Expertise",linewidth=2)
#ax1.plot(gen, fit_stds_med, "k-", label="Std Fitness")
#ax1.plot(gen, fit_maxs_med, "r-", label="Maximum Fitness",linewidth=3)
#ax1.plot(gen, fit_mins_q1, "g-",)
#ax1.plot(gen, fit_avgs_q1, "y-")
#ax1.plot(gen, fit_stds_med, "k-", label="Std Fitness")
#ax1.plot(gen, fit_maxs_q1, "r-")
#ax1.plot(gen, fit_mins_q3, "g-")
#ax1.plot(gen, fit_avgs_q3, "y-")
#ax1.plot(gen, fit_stds_med, "k-", label="Std Fitness")
#ax1.plot(gen, fit_maxs_q3, "r-")
ax1.set_xlabel("Generation")
ax1.set_ylabel("Fitness")
#for tl in ax1.get_yticklabels():
#    tl.set_color("b")
plt.legend()
plt.show()

fit_mins= np.array(fit_mins)
bestfits=fit_mins[:,100]
print("bestfits:"+np.mean(bestfits)+ " s:"+np.std(bestfits))