import operator
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from DATABASE_MI import DATABASE_MI
from MI_UNIT import MI_UNIT
from matplotlib.backends.backend_pdf import PdfPages
import getTaxIDString as taxIDConverter
from DATABASE_MI import DATABASE_MI

SOURCEFOLDER = sys.argv[1]
CUTOFF = int(sys.argv[2])

DB_DICT = {"0469":"IntAct","0463":"biogrid","0471":"mint","2165":"bar","0465":"dip","1114":"virhostnet","0486":"uniprotkb","1335":"hpidb","1332":"bhf-ucl","2166":"ai","0917":"matrixdb","0903":"mpidb","1262":"i2d","0974":"innateDB","1222":"mbinfo","1263":"molecularConnections","1264":"ntnu", "0478":"hprd"}

# -------------------------

dataframe = DATABASE_MI()
with open(SOURCEFOLDER+"wholeset.mitab",'r') as fh:
#with open(SOURCEFOLDER+"mentha.mitab",'r') as fh:
    print("reading inputfile...")
    for i in fh:
        dataframe.__add__(MI_UNIT(i))

with open(SOURCEFOLDER+"databaseData.txt","w") as fh:
    print("making database list...")
    data = sorted(dataframe.getDBDict().items(),key = operator.itemgetter(1), reverse = True)
    for i in data:
        if i[0] != '-' and i[0] != "0914" and i[0] != "'-'":
            print("{}:\t{} accessions".format(DB_DICT[str(i[0])],i[1]))

print("making pdf...")
speciescounter = {}
for i in dataframe.dataframe:
    species,databases = i.getSpeciesA(),i.getDatabase()
    if species in speciescounter.keys():
        speciescounter[species] += 1
    else:
        speciescounter[species] = 1
sortedCounter = sorted(speciescounter.items(), key=operator.itemgetter(1), reverse=True)
sortedCounterKeys = [i[0] for i in sortedCounter if i[1] > CUTOFF]
sortedCounterValues = [i[1] for i in sortedCounter if i[1] > CUTOFF]

for i in range(len(sortedCounterKeys)):
    sortedCounterKeys[i]= taxIDConverter.getTaxID(sortedCounterKeys[i])[:25]
"""
############
############
figuur maken
############
############
"""
fig = plt.figure()
############
#figuur A###
###########
x = range(len(sortedCounterValues))
#figuur

plt.bar(x, sortedCounterValues, color="pink")
plot_margin = 0.25

x0, x1, y0, y1 = plt.axis()
plt.axis((x0 - plot_margin,x1 + plot_margin,y0 - plot_margin,y1 + plot_margin))
#axis
plt.xticks(np.arange(len(sortedCounterKeys)), sortedCounterKeys,rotation = 45)

plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 5
#legende
plt.xlabel("species")
plt.ylabel("number of interactions")
plt.tight_layout(h_pad=2)
plt.savefig("speciesGraphA.png", dpi=300)
plt.close()

##########
#figuur B#
##########



speciescounter = {}
for i in dataframe.dataframe:
    species,databases = i.getSpeciesB(),i.getDatabase()
    if species in speciescounter.keys():
        speciescounter[species] += 1
    else:
        speciescounter[species] = 1
sortedCounter = sorted(speciescounter.items(), key=operator.itemgetter(1), reverse=True)
sortedCounterKeys = [i[0] for i in sortedCounter if i[1] > CUTOFF]
sortedCounterValues = [i[1] for i in sortedCounter if i[1] > CUTOFF]
for i in range(len(sortedCounterKeys)):
    sortedCounterKeys[i]= taxIDConverter.getTaxID(sortedCounterKeys[i])[:25]

fig = plt.figure()
x = range(len(sortedCounterValues))

#figuur
plt.bar(x, sortedCounterValues, color="pink")
plot_margin = 0.25

x0, x1, y0, y1 = plt.axis()
plt.axis((x0 - plot_margin,x1 + plot_margin,y0 - plot_margin,y1 + plot_margin))
#axis
plt.xticks(np.arange(len(sortedCounterKeys)), sortedCounterKeys,rotation = 45)
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 5

#legende
plt.xlabel("species")
plt.ylabel("number of interactions")
plt.tight_layout(h_pad=2)
plt.savefig("speciesGraphB.png", dpi=300)
plt.close()