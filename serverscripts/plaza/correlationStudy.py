import sys
import os
from scipy.stats import ttest_ind
import random

correlationlocation = sys.argv[1]
interologylocation = sys.argv[2]

correlationfh = open(correlationlocation)
interologyfh = open(interologylocation)
#C:\Users\beheerder\PycharmProjects\thesis\orthology\interologyPlaza.txt
print(correlationfh.readline())
print(correlationfh.readline())
print(correlationfh.readline())

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
            invalid+=1
print(len(correlationDict.items()))
random_corr = random.sample(list(correlationDict.values()),1000)
print("total correlation from interologs= {}\ntotalcorrelation from random pairs= {}".format(sum(inter_corr)/count,sum(random_corr)/len(random_corr)))
print("p value between two correlations: {}".format(ttest_ind(inter_corr,random_corr)))
print("number of invalid keys: {} out of {} = {}".format(invalid,count,invalid/count))