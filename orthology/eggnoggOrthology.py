import sys
from MI_UNIT import MI_UNIT_string

eggnoggfile = sys.argv[1]
eggnoggmapping = sys.argv[2]
knowninteractions = sys.argv[3]
querysp = sys.argv[4]
#arg 1 = file with eggnog interactions NOG.members.tsv
#arg 2 = file for idmapping og <-> uniprot mappingIdEggnogg.tsv
#arg 3 = file wholesetExtended
#arg 4 = query species id, 2850 = ptr
"""
workflow:
1. alle orthologe groepen uit eggnog halen
2. kijken of ergens ptrs in zitten
3. alle orthologen van ptr uitschrijven
4. interologen bepalen
"""

outfileortho = open("orthologyEggnog{}.txt".format(querysp),'w')
outfileintero = open("interologyEggnog{}.txt".format(querysp),'w')
outfiledonorsp = open("donorspeciesEggnog{}.txt".format(querysp),'w')
uniToOG = {}
oGToUni = {}
print("reading mapping file...")
for i in open(eggnoggmapping):
    uniprot = i.split()[0]
    egg = i.split()
    for i in egg:
        if i != '-':
            uniToOG[uniprot] = i
            if i not in oGToUni.keys():
                oGToUni[i] = [uniprot]
            else:
                oGToUni[i].append(uniprot)

print("size of uniprot id map: " + str(len(uniToOG.keys())))

oGtoPTR = {}
for i in open(eggnoggfile):
    l =  i.split()
    OG = l[1]
    ids = l[5].split(',')
    for id in ids:
        sp = id.split('.')[0]
        if str(querysp) == sp:
            if OG not in oGtoPTR.keys():
                oGtoPTR[OG] = [id.split(".")[1]]
            else:
                oGtoPTR[OG].append(id.split(".")[1])
print("size of ptr protein dict: {}".format(sum([int(len(i)) for i in oGtoPTR.values()])))


absentcounter = 0
print('writing orthology ptr to file')
orthologyMap = {}
for i in oGtoPTR.keys():
    try:
        ptrs = oGtoPTR[i]
        for j in oGToUni[i]:
            for k in ptrs:
                orthologyMap[j] = k
                outfileortho.write("{}\t{}\n".format(k,j))
    except KeyError:
        print("absent OG: {}".format(i))
        absentcounter+=1
print("absent OG's: {}".format(absentcounter))
print("total orthology links: {}".format(len(orthologyMap.keys())))
print("")

print('writing interology ptr to file')
interologsMapped = 0
interologs = set()
for int in open(knowninteractions):
    interaction = MI_UNIT(int)
    uIDA = interaction.getUniprotIdA()
    uIDB = interaction.getUniprotIdB()
    try:
        ptrA = orthologyMap[uIDA]
        ptrB = orthologyMap[uIDB]
        if (ptrA,ptrB) not in interologs:
            interologs.add((ptrA,ptrB))
            outfiledonorsp.write("{}\t{}\n".format(interaction.taxidInteractorA,interaction.taxidInteractorB))
            #print("interology detected! uniprot interaction between {} and {}".format(uIDA,uIDB))
            outfileintero.write("{}\t{}\n".format(ptrA,ptrB))
            interologsMapped+=1
    except KeyError:
        pass

print("mapped interologs: {}".format(interologsMapped))