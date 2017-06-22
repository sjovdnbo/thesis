import sys
from eggNOGID import eggNOGID
from MI_UNIT_string import MI_UNIT
import itertools
import numpy as np
eggnoggfile = sys.argv[1]
if eggnoggfile == "help":
    print(
        "help with arguments: \n------------\narg1: eggnog interactions\narg2: uniprot idmapping\narg3: PPIdata\narg4: taxid\n-----------")
    sys.exit()

mapping = sys.argv[2]
knowninteractions = sys.argv[3]
querysp = sys.argv[4]
outfolder = sys.argv[5].strip()
# arg 1 = file with eggnog interactions NOG.members.tsv
# arg 2 = og file <-> uniprot mappingIdEggnogg.tsv
# arg 3 = file wholesetExtended
# arg 4 = query species id, 2850 = ptr
species = ["Sce", "Tpa", "Rno", "Mmu", "Hsa", "Eco", "Dme", "Cje", "Cel", "Ath", "Ptr"]
taxIDs = ["4932", "243276", "10116", "10090", "9606", "481805", "7227", "192222", "6239", "1392", "3702", "2850"]
spDict = dict(zip(species, taxIDs))
outfileortho = open(outfolder+"/orthologyEggnogString{}.txt".format(querysp),'w')
outfileintero = open(outfolder+"/interologyEggnogString{}.txt".format(querysp),'w')
outfiledonorsp = open(outfolder+"/donorspeciesEggnogString{}.txt".format(querysp),'w')
oglist = {}
ptrgenes = set()
def parseSpnumber(string):
    if "taxid" in string:
        string = string.split(":")[1]
    if "(" in string:
        string = string.split("(")[0]
    return string
print("reading eggnog file...")
for i in open(eggnoggfile):
    parsed = i.split()
    og = parsed[1]
    genes = parsed[-1].split(",")
    taxids = [i.split(".")[0] for i in genes]
    if querysp in taxids:
        for j in genes:
            taxid, gene = j.split(".", maxsplit=1)
            if taxid in taxIDs:
                if og not in oglist.keys():
                    oglist[og] = {j}
                else:
                    oglist[og].add(j)
#print(oglist.items())
"""
for taxid in taxIDs:
    for og,genes in oglist.items():
        for gene in genes:
            tax,gene = gene.split(".",maxsplit=1)
            if taxid == tax:
                print(gene)
"""
uniprotDict = {}
print('reading mapping file...')
for line in open(mapping):
    uniprot,database,id = line.strip("\n").split("\t")
        #id = id.rstrip(".1").lower()
    #print(uniprot,database,id)
    if "ensemblgenome" in database.strip().lower():
        if "fbpp" not in id.lower():
            continue
    if "ensembl_pro" in database.strip().lower():
        #print(id.lower()[:5])
        if id.lower()[:6] not in ["ensmus","ensrno","ensp00"]:
            continue

    if '.' in id:
        id = id.split(".")[1]
    #if id.lower() == "fbpp0111676":print('fbpp0111676')
    if id not in uniprotDict.keys():
        uniprotDict[id.lower()]=uniprot
#print([i for i in uniprotDict.items()][:10])
#print([i for i in uniprotDict.items() if i[0][:6] == "ensrno"][:10])
#print([i for i in uniprotDict.items() if i[0][:2] == "cj"][:10])
#print([i for i in uniprotDict.items() if i[0][:5] == "ecolc"][:10])
#print([i for i in uniprotDict.items() if i[0][:5] == "ensnp"][:10])
#print([i for i in uniprotDict.items() if i[0][:4] == "fbpp"][:10])
#print([i for i in uniprotDict.items() if i[0][:6] == "ensmus"][:10])

#print(uniprotDict["ensrnop00000066448"])
#print(uniprotDict["fbpp0289365"])

convertlist = ['192222',"7227","481805","3702",'10116','10090','9606']
converted = 0
failed = 0
total = 0
ptrlist={}
for og,genes in oglist.items():
    conv = set()
    for gene in genes:
        total +=1
        ENgene = eggNOGID(gene)
        taxid = ENgene.taxid
        if taxid in convertlist:
            if taxid == "192222":
                query = "cj"+ENgene.gene[2:]
            elif taxid == "3702":
                query = ENgene.gene
            elif taxid in ["7227","481805",'10116','10090','9606']:
                query = ENgene.gene
            query = query.lower()
            try:
                conv.add(uniprotDict[query].split("-")[0].split(".")[0])
                converted+=1
            except KeyError:
                #print("gene not found: {},query = {}".format(gene,query))
                failed +=1
        else:
            conv.add(ENgene.gene)
    oglist[og]=conv
#print(oglist.items())
print("total: {}\tconverted: {}\tfailed: {}".format(total,converted,failed))
# print(len(oglist))
# print(ptrgenes)
# print("fetched orthologous groups, {} groups for species {}".format(len(oglist), querysp))
orthologyMap = {}
print("writing orthology...")
total_other = 0
total_ptrs = 0
max = []
for og,genes in oglist.items():
    ptrs = [i for i in genes if "phatr" in i.lower()]
    if len(ptrs)> len(max):
        max = ptrs
    other = [i for i in genes if "phatr" not in i.lower()]
    total_other+=len(other)
    total_ptrs+=len(ptrs)
    for gene in other:
        if gene not in orthologyMap.keys():
            orthologyMap[gene] = ptrs
        else:
            newlist =  orthologyMap[gene]+ ptrs
            newlist = list(set(newlist))
            orthologyMap[gene]=newlist
        for ptr in ptrs:
            outfileortho.write(ptr+"\t"+gene+"\n")
print("number of orthologous groups: {}".format(len(oglist)))
print("number of ptrs: {}\tavg ptrs: {}".format(total_ptrs,total_ptrs/len(oglist)))
print("avg ptr map size: {}".format(sum([len(i) for i in orthologyMap.values()])/len(orthologyMap.keys())))
print("median ptr map size:{}".format(np.median([len(i) for i in orthologyMap.values()])))
#print(max)
#print(orthologyMap.items())
# ok because no ptr data in interaction data


print('writing interology ptr to file')
interologsMapped = 0
interologs = set()
donorspmap = {}

for int in open(knowninteractions):
    interaction = MI_UNIT(int)
    uIDA = interaction.idInteractorA
    uIDB = interaction.idInteractorB
    try:
        ptrA = orthologyMap[uIDA]
        ptrB = orthologyMap[uIDB]
        #print([i for i in itertools.product(ptrA,ptrB)])

        for comb in itertools.product(ptrA,ptrB):
            ptr1 = comb[0].strip()
            ptr2 = comb[1].strip()

            if ptr1 != ptr2:
                if (ptr1, ptr2) not in interologs and (ptr2, ptr1) not in interologs:
                    interologs.add((ptr1, ptr2))
                    donorspmap[(ptr1, ptr2)] = {parseSpnumber(interaction.taxidInteractorA),
                                                parseSpnumber(interaction.taxidInteractorB)}
                    # outfiledonorsp.write("{}\t{}\n".format(interaction.taxidInteractorA, interaction.taxidInteractorB))
                    # print("interology detected! uniprot interaction between {} and {}".format(uIDA,uIDB))
                    outfileintero.write("{}\t{}\n".format(ptr1, ptr2))
                    interologsMapped += 1
                else:
                    donorspmap[(ptr1, ptr2)].add(parseSpnumber(interaction.taxidInteractorA))
                    donorspmap[(ptr1, ptr2)].add(parseSpnumber(interaction.taxidInteractorB))
    except KeyError:
        continue
outfiledonorsp.write("".join([str(key)+'\t'+str(value)+"\n" for key,value in donorspmap.items()]))


print("mapped interologs: {}".format(interologsMapped))

