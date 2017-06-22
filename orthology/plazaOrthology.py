import os
import sys
from MI_UNIT_EX import MI_UNIT_EX

orthologsfolder = sys.argv[1] #ortholog folder

knowninteractions = sys.argv[2] #mytab file

outfiledonorsp = open("donorspeciesPlaza.txt","w")
outOrthologyPlaza = open("orthologyPlaza.txt","w")
outInterologyPlaza = open("interologyPlaza.txt",'w')

commonOrthologsDict = {}
def iterkeys(values):
    out = []
    for val in values:
        out.append(val)
    return out

def permute(listA,listB):
    out = set()
    for a in listA:
        for b in listB:
            out.add((a,b))
    return out

def readOrthofile(file):
    print("reading {}...".format(file))
    fh = open(file,"r")
    orthoDict = {}
    for line in fh:
        split = line.strip("\n").split("\t")
        geneId = split[0]
        targetgenes = split[3].replace(";",',').split(",")
        targetgenes = [i.split(":")[1] for i in targetgenes if ":" in i]
        orthoDict[geneId] = targetgenes
    print("constructed dict with {} keys, {} values on average\n".format(len(orthoDict.keys()), sum([len(i) for i in orthoDict.values()])/len(orthoDict.keys())))
    return orthoDict

#iterate over files and make common dict
for filename in os.listdir(orthologsfolder):
    d = readOrthofile(orthologsfolder+filename)
    for key,value in d.items():
        if key not in commonOrthologsDict.keys():
            commonOrthologsDict[key] = value
        else:
            commonOrthologsDict[key].extend(value)
#filter common dict to only double occurences and remove empty vals afterwards
for key,value in commonOrthologsDict.items():
    value = set([i for i in value if value.count(i) >=2])
    commonOrthologsDict[key]= value
print("filtering orthologsdict, {} keys with on average {} values".format(len(commonOrthologsDict.keys()),sum([len(i)for i in commonOrthologsDict.values()])/len(commonOrthologsDict.keys())))

oGtoPTR = {}
#write orthologs and make ortholog->ptr dict
for key,values in commonOrthologsDict.items():
    if "ptr" in key:
        for value in values:
            if value != key:
                value = value.split("_")[0]
                outOrthologyPlaza.write("{}\t{}\n".format(key,value))
                if value not in oGtoPTR.keys():
                    oGtoPTR[value] = {key}
                else:
                    oGtoPTR[value].add(key)
#print(sum([len(i) for i in oGtoPTR.values()])/len(oGtoPTR.keys()))

for k,v in oGtoPTR.items():
    #if len(v) > 1:
     #   print(v)
     oGtoPTR[k] = list(v)
#write interologs
interologsMapped = 0
interologs = set()
print('mapping interologs...')
for int in open(knowninteractions):
    interaction = MI_UNIT_EX(int,new = False)
    uIDA = interaction.getUniprotIdA()
    uIDB = interaction.getUniprotIdB()
    try:
        ptrA = iterkeys(oGtoPTR[uIDA]) # list with all values
        ptrB = iterkeys(oGtoPTR[uIDB])
        for i in permute(ptrA,ptrB):    #make list of all possible combinations between these lists
            #hier testen of wel zelfde species
            #uIDA.split("_")[1] == uIDB.split("_")[1]
            if i not in interologs and i[0] != i[1]:
                interologs.add(i)
                outfiledonorsp.write("{}\t{}\n".format(interaction.taxidInteractorA,interaction.taxidInteractorB))
                #print("interology detected! uniprot interaction between {} and {}".format(uIDA,uIDB))
                outInterologyPlaza.write("{}\t{}\n".format(i[0],i[1]))
                interologsMapped+=1
    except KeyError:
        pass

