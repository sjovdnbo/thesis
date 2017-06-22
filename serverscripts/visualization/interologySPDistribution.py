import sys, operator
import numpy as np
import matplotlib.pyplot as plt

def readfile(file):
    multiplePredDict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    speciesContrDict = {'7227':0,'192222':0,'6239':0,'3702':0,'9606':0,'10090':0,'243276':0,'10116':0,'197':0}
    for line in file:
        try:
            int, sp = line.strip("\n").split("\t")
            sp = sp.strip("}")
            for ids in sp.split(","):
                ids = ids.strip("{").strip(" '")
                if ids not in speciesContrDict.keys():
                    speciesContrDict[ids] = 1
                else:
                    speciesContrDict[ids]+=1
            multiplePredDict[len(sp.split(","))] += 1
        except ValueError:
            print(line)

    return multiplePredDict,speciesContrDict
def makeDictPercent(dict):
    new = {}
    for key,value in dict.items():
        new[key]= value/sum(dict.values())
    return new
def sortDict(dict):
    return sorted(dict.items(),key=operator.itemgetter(1))[::-1]
def getpair(dict,key):
    return (key,dict[key])
def dictToList(dict):
    list = []
    for i in ['7227','192222','3702','6239','9606','10090','10116','243276','197']:
        list.append(getpair(dict,i))
    return list


def get2nditem(listoftuples):
    return [i[1] for i in listoftuples]

multiplePredictedData_PR, speciesContribution_PR = readfile(open(sys.argv[1]))
multiplePredictedData_PL, speciesContribution_PL = readfile(open(sys.argv[2]))
multiplePredictedData_EG, speciesContribution_EG = readfile(open(sys.argv[3]))
#print("multiple Predicted data: {}\n".format([str(key)+": "+str(value) for key,value in multiplePredictedData.items()]))
##################################################################
##################################################################
normalizedMultiplePredictedData_PR = sortDict(makeDictPercent(multiplePredictedData_PR))
normalizedMultiplePredictedData_PL = sortDict(makeDictPercent(multiplePredictedData_PL))
normalizedMultiplePredictedData_EG = sortDict(makeDictPercent(multiplePredictedData_EG))
print("first figure data: ")
print("\nPR:",sortDict(multiplePredictedData_PR))
print("\t",normalizedMultiplePredictedData_PR)
print("\nPl:",sortDict(multiplePredictedData_PL))
print("\t",normalizedMultiplePredictedData_PL)
print("\neggnog:",sortDict(multiplePredictedData_EG))
print("\t",normalizedMultiplePredictedData_EG)

index = np.arange(1,len(normalizedMultiplePredictedData_EG)+1)

bar_width = 0.2
opacity = 0.8
f,ax1= plt.subplots()

graph1 = plt.bar(index-(1.5*bar_width),get2nditem(normalizedMultiplePredictedData_PR),bar_width,alpha=0.5,color='#d24dff',label="Regular Plaza")
graph2 = plt.bar(index-(0.5*bar_width),get2nditem(normalizedMultiplePredictedData_PL),bar_width,alpha=0.5,color='#ffb366',label = "Liberal Plaza")
graph3 = plt.bar(index+(0.5*bar_width),get2nditem(normalizedMultiplePredictedData_EG),bar_width,alpha=0.5,color='#7fd6ff',label = "EggNOG")

plt.title("Number of species predicting the same interaction")
plt.xlim(0.5,7.5)
plt.xticks(index)
plt.xlabel("Multiplicity")
plt.ylabel("Percentage of entries")
plt.legend()
f.tight_layout()

f.savefig("multiplePredictions.png", dpi=500)

##################################################################
##################################################################
normalizedSpeciesContribution_PR = dictToList(makeDictPercent(speciesContribution_PR))
normalizedSpeciesContribution_PL = dictToList(makeDictPercent(speciesContribution_PL))
normalizedSpeciesContribution_EG = dictToList(makeDictPercent(speciesContribution_EG))
print("\n-----------\n\nsecond figure data:")
print("\nPR:",sortDict(speciesContribution_PR))
print("\t",normalizedSpeciesContribution_PR)
print("\npl:",sortDict(speciesContribution_PL))
print("\t",normalizedSpeciesContribution_PL)
print("\neg:",sortDict(speciesContribution_EG))
print("\t",normalizedSpeciesContribution_EG)

index = np.arange(len(speciesContribution_EG.keys()))

bar_width = 0.2
opacity = 0.8
f,ax1= plt.subplots()

graph1 = plt.bar(index-(1.5*bar_width),get2nditem(normalizedSpeciesContribution_PR),bar_width,alpha=0.5,color='#d24dff',label="Regular Plaza")
graph2 = plt.bar(index-(0.5*bar_width),get2nditem(normalizedSpeciesContribution_PL),bar_width,alpha=0.5,color='#ffb366',label = "Liberal Plaza")
graph3 = plt.bar(index+(0.5*bar_width),get2nditem(normalizedSpeciesContribution_EG),bar_width,alpha=0.5,color='#7fd6ff',label = "EggNOG")

plt.title("Species Contribution to prediction")
plt.xticks(index,["Drome","Sacce","Arath","Caeel","Homsa","Musmu","Ratno","Trepa","Camje"],rotation=60)

plt.xlabel("Species")
plt.ylabel("Percentage of predictions")
plt.legend()
f.tight_layout()

f.savefig("speciesContribution.png", dpi=500)


#print("species contribution: {}\n".format([str(key)+": "+str(value) for key,value in sorted(speciesContribution.items(),key = operator.itemgetter(1))]))
#normalizedSpContribution = makeDictPercent(multiplePredictedData_PR).items()
