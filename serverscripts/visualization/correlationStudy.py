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
from scipy.stats import ks_2samp


correlationlocation = sys.argv[1]
interologylocation= sys.argv[2]
newlocation = sys.argv[3]
cutoff = float(sys.argv[4])

figurename = newlocation.split("/")[-1].split(".")[0]

correlationfh = open(correlationlocation)
interologyfh = open(interologylocation)
filteredfh = open(newlocation,'w')

correlationfh.readline()
correlationfh.readline()
correlationfh.readline()
def normalization(list):
    return [(i - np.mean(list)) / np.std(list) for i in list]

def getNumber(id):
    if "_" in id:
        id = id.split("_")[1]
    id = id[4:]
    return id

correlationDict = {}
print("making correlation dict...")
for i in correlationfh:
    intA,intB,corr = i.split()
    correlationDict[intA.lower()+"_"+intB.lower()]=float(corr)

inter_corr = []
count = 0
invalid = 0

print("filtering correlation...")
for i in interologyfh:
    intA,intB = i.split()
    count += 1
    try:
        corr = correlationDict[intB.lower() + "_" + intA.lower()]
        inter_corr.append(corr)
        filteredfh.write("{}\t{}\n".format(intA.lower(),intB.lower()))
    except KeyError:
        try:
            corr = correlationDict[intA.lower() + "_" + intB.lower()]
            inter_corr.append(corr)
        except KeyError:
            print(intA.lower(),intB.lower())
            invalid += 1

print("making sample list...")

filtered = [i for i in inter_corr if i > cutoff]

random_corr = random.sample(list(correlationDict.values()),len(inter_corr))
print(ks_2samp(inter_corr, random_corr))
#random_corr_new = random_corr #normalization
#inter_corr_new = inter_corr


print("\tpassed interactions: {} \t\tfiltered interactions:{}".format(len(filtered),len(inter_corr)-len(filtered)))
print("\tnumber of invalid keys: {} out of {} = {}".format(invalid,count,invalid/count))


print("visualization...")

nbins = 20
index = np.arange(nbins)
bar_width = 0.35
opacity = 0.8

f,ax1= plt.subplots()
data = [random_corr,inter_corr]#668cff
ax1.hist(data,nbins,histtype='bar',color=['#668cff','#ffb366'],label = ["random coexpression","PPI coexpression"])
#graph1 = plt.hist(random_corr,index,bar_width,histtype="bar",alpha=0.5,color='#d24dff',label="random coexpression")
#graph2 = plt.hist(inter_corr,index,bar_width,histtype="bar",alpha=0.5,color='#ffb366',label = "real coexpression")

plt.title("Coexpression comparison")
#plt.xticks(index,tuple(run2keys),rotation=60)
plt.yticks()
plt.xlabel("PCC")
plt.ylabel("Number of interactions in interval")
plt.legend(loc=2)
f.tight_layout()
ax1.grid(b=False)
ax1.set_axis_bgcolor('white')

f.savefig("{}.png".format(figurename), dpi=500)

#plt.show()
