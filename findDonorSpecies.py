from getTaxIDString import getTaxID
import sys
import operator

with open(sys.argv[1]) as fh:
    map = {}
    for i in fh:
        idB = int(i.split('\t')[0].split(":")[1].split('(')[0])
        if idB not in map.keys():
            map[idB] = 1
        else:
            map[idB] +=1
mapcp = {}
for i in map.items():
    mapcp[getTaxID(i[0])] = i[1]

for i in sorted(mapcp.items(), key=operator.itemgetter(1)):
    print(i[0],"\t",i[1])