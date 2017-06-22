import sys
from scipy.stats import ttest_ind
import matplotlib
matplotlib.use('Agg')
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import math


correlationlocation = sys.argv[1]
interologylocation= sys.argv[2]
newlocation = sys.argv[3]

correlationfh = open(correlationlocation)
interologyfh = open(interologylocation)
filteredfh = open(newlocation)

correlationfh.readline()
correlationfh.readline()
correlationfh.readline()

def getNumber(id):
    if "_" in id:
        id = id.split("_")[1]
    id = id[4:]
    return id

correlationDict = {}
for i in correlationfh:
    intA,intB,corr = i.split()
    correlationDict[intA.lower()+"_"+intB.lower()]=float(corr)

inter_corr = []
count = 0
invalid = 0
for i in interologyfh:
    intA,intB = i.split()
    count += 1
    try:
        corr = correlationDict[intB.lower() + "_" + intA.lower()]
        inter_corr.append(corr)
    except KeyError:
        try:
            corr = correlationDict[intA.lower() + "_" + intB.lower()]
            inter_corr.append(corr)
        except KeyError:
            print(intA.lower(),intB.lower())
            invalid += 1

random_corr = random.sample(list(correlationDict.values()),len(inter_corr))
random_corr_new = [(i-np.mean(random_corr))/np.std(random_corr) for i in random_corr] #normalization
inter_corr_new = [(i-np.mean(inter_corr))/np.std(inter_corr) for i in inter_corr]
print("before normalization:\nstd random_corr:{} \t std inter_Corr: {}".format(np.std(random_corr),np.std(inter_corr)))
print("mean random_corr:{} \t mean inter_corr: {}".format(np.mean(random_corr),np.mean(inter_corr)))
print('min/max inter_corr:[{},{}]'.format(min(inter_corr),max(inter_corr)))
print('min/max random_corr:[{},{}]'.format(min(random_corr),max(random_corr)))
print("\nafter normalization:\nstd random_corr:{} \t std inter_Corr: {}".format(np.std(random_corr_new),np.std(inter_corr_new)))
print("mean random_corr_new:{} \t mean inter_corr_new: {}".format(np.mean(random_corr_new),np.mean(inter_corr_new)))
print('min/max inter_corr_new:[{},{}]'.format(min(inter_corr_new),max(inter_corr_new)))
print('min/max random_corr_new:[{},{}]'.format(min(random_corr_new),max(random_corr_new)))
print("\ntotal correlation from interologs= {}"
      "\ntotal correlation from random pairs= {}".format(sum(inter_corr_new)/len(inter_corr_new),sum(random_corr_new)/len(random_corr_new)))
print("p value between two correlations: {}".format(ttest_ind(inter_corr_new,random_corr_new)))
print("number of invalid keys: {} out of {} = {}".format(invalid,count,invalid/count))




fig, ax = plt.subplots()
"""
for a in [random_corr_new, inter_corr_new]:
    sns.distplot(a,bins=20, ax=ax, kde=True)
ax.set_xlim([-4, 3])
"""
print(random_corr)
print(inter_corr)
log_random_corr = [math.log(1+i-min(random_corr)) for i in random_corr]
log_inter_corr = [math.log(1+i-min(inter_corr)) for i in inter_corr]
for a in [log_inter_corr, log_random_corr]:
    legend = ""
    if a==log_inter_corr:
        legend = "Interologs Correlation"
    if a==log_random_corr:
        legend = "Random Correlation"
    sns.distplot(a,bins=20, label=legend, ax=ax, kde=True)

ax.legend()




plt.xlabel('Z-score')
plt.ylabel('frequency')
plt.title("Z-score distribution of correlations")
plt.savefig("visualizationCorrelationStudy.png", dpi=1200)
plt.close()