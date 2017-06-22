import sys
import glob

from MI_UNIT import MI_UNIT
SOURCEFOLDER = sys.argv[1]
"""
uniprotids = open(SOURCEFOLDER+"/uniprotIDs.txt","w")
intactids = open(SOURCEFOLDER+"data/intactIDs.txt","w")
ensemblids = open(SOURCEFOLDER+"data/ensemblIDs.txt","w")
entrezids = open(SOURCEFOLDER+"data/entrezIDs.txt","w")

"""

def addToDict(element,dict):
    if element in dict.keys():
        dict[element] = True
    else:
        pass

def getDatabase(element):
    return element.split(":")[0]
def getAccession(element):
    return element.split(":")[1]

def readfile(filename):
    wb = {}
    with open(filename,encoding='latin-1') as fh:
        count = 0
        fh.readline()
        for i in fh:
            accessionsdict = {"intact":False,"ensembl":False,"uniprotkb":False,"entrez gene/locuslink":False, "biogrid":False}
            i = MI_UNIT(i)
            accessionsdict["whole"] = i
            primID = i.idInteractorA
            addToDict(getDatabase(primID),accessionsdict)
            secID = i.altIDsInteractorA
            secID =secID.split("|")
            for i in secID:
                addToDict(getDatabase(i),accessionsdict)
            count+=1
            wb[count] = accessionsdict

    print(" \n---------------------\ndone reading {}... \n---------------------".format(filename))

    intactCount = 0
    ensemblCount = 0
    uniprotkbCount = 0
    entrezGeneCount = 0
    biogridCount = 0

    for i in wb.items():
        key = i[0]
        if i[1]["intact"] != False:
            if filename == "data\IntAct.mitab":

                intactCount+=1
        if i[1]["biogrid"] != False:
            biogridCount+=1
        if i[1]["ensembl"]!= False:
            ensemblCount+=1
        if i[1]["uniprotkb"] != False:
            uniprotkbCount+=1
        if i[1]["entrez gene/locuslink"] != False:
            entrezGeneCount+=1

    print("\t{}% of accessions contain {} identifiers, {} in total".format(uniprotkbCount/count*100,"uniprot",uniprotkbCount))
    print("\t{}% of accessions contain {} identifiers, {} in total".format(intactCount/count*100,"intact",intactCount))
    print("\t{}% of accessions contain {} identifiers, {} in total".format(ensemblCount/count*100,"ensembl",ensemblCount))
    print("\t{}% of accessions contain {} identifiers, {} in total".format(biogridCount/count*100,"biogrid",biogridCount))
    print("\t{}% of accessions contain {} identifiers, {} in total".format(entrezGeneCount/count*100,"entrezGene",entrezGeneCount))


for filename in glob.glob(SOURCEFOLDER+"/*.mitab"):
    readfile(filename)