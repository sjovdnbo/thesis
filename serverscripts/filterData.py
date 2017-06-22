import sys
import glob
import os
from MI_UNIT import MI_UNIT

from DATABASE_MI import DATABASE_MI

SOURCEFOLDER = sys.argv[1]


data = DATABASE_MI()
speciescounter = {}
"""
u1 = MI_UNIT('uniprotkb:P07867	uniprotkb:P04114	intact:EBI-3926040|uniprotkb:Q9UMN0|uniprotkb:P78479|uniprotkb:P78480|uniprotkb:Q7Z600|uniprotkb:Q13786|uniprotkb:O00502|uniprotkb:P78481|uniprotkb:Q4ZG63|uniprotkb:Q13779|uniprotkb:Q13788|uniprotkb:Q13785|uniprotkb:Q13787|uniprotkb:Q53QC8	intact:EBI-9206530	psi-mi:apob_human(display_long)|uniprotkb:APOB(gene name)|psi-mi:APOB(display_short)	psi-mi:lipc_rat(display_long)|uniprotkb:Lipc(gene name)|psi-mi:Lipc(display_short)|uniprotkb:Lipase member C(gene name synonym)	psi-mi:"MI:0047"(far western blotting)	Choi et al. (1998)	imex:IM-22978|pubmed:9685401	taxid:9606(human)|taxid:9606(Homo sapiens)	taxid:10116(rat)|taxid:10116("Rattus norvegicus (Rat)")	psi-mi:"MI:0914"(association)	psi-mi:"MI:1332"(bhf-ucl)	intact:EBI-9206517|imex:IM-22978-1	intact-miscore:0.35')
u2= MI_UNIT('uniprotkb:P04114	uniprotkb:P07867	intact:EBI-3926040|uniprotkb:Q9UMN0|uniprotkb:P78479|uniprotkb:P78480|uniprotkb:Q7Z600|uniprotkb:Q13786|uniprotkb:O00502|uniprotkb:P78481|uniprotkb:Q4ZG63|uniprotkb:Q13779|uniprotkb:Q13788|uniprotkb:Q13785|uniprotkb:Q13787|uniprotkb:Q53QC8	intact:EBI-9206530	psi-mi:apob_human(display_long)|uniprotkb:APOB(gene name)|psi-mi:APOB(display_short)	psi-mi:lipc_rat(display_long)|uniprotkb:Lipc(gene name)|psi-mi:Lipc(display_short)|uniprotkb:Lipase member C(gene name synonym)	psi-mi:"MI:0047"(far western blotting)	Choi et al. (1998)	pubmed:9685402|pubmed:9685401	taxid:9606(human)|taxid:9606(Homo sapiens)	taxid:10116(rat)|taxid:10116("Rattus norvegicus (Rat)")	psi-mi:"MI:0914"(association)	psi-mi:"MI:1332"(bhf-ucl)	intact:EBI-9206517|imex:IM-22978-1	intact-miscore:0.35')
print(u1.__eq__(u2))
#equals functie werkt!
met pubmed overlap, en reciprociteit
"""

if os.path.isfile(SOURCEFOLDER+"wholeset.mitab"):
    os.remove(SOURCEFOLDER+"wholeset.mitab")

def readFile(pathname, header=True):
    try:
        with open(pathname, "r", encoding='latin-1') as fh:
            print("\treading file: "+ pathname+"\n")
            if header == True: fh.readline()
            for i in fh:
                i = MI_UNIT(i)
                data.__add__(i)
    except FileNotFoundError:
        print("\tError reading file: "+ pathname+ "\tnot found!\n")
print("initiating reading\n")

for filename in glob.glob(sys.argv[1]+"*.mitab"):
    readFile(filename)

interactions = []
def filter(taxIDInteractor = ["-2","-1"],interactionType = ['0208','1110','0799','0205','0933','0190','0797','0934','1284','1271','0935','0795','0796','1280','1292','1278','1279','0794','1286','0932','1289','1288','1275','1276','1287','1295','1277','1272','1274','1273','1285','1290','1291','1293','1294','1282','1281','1283'],interactionIDMs = ['0026','0037','0577','0660','0659','0363','0364','0362','0577','0035','0577','0035','0057','0085','0036','1177','0100','0087','0024','1100','2231','1178','1176','0101','0046,','0105','0058','0063','0686','0064']):
    print("initiating filtering...\n")
    for i in data.dataframe:
        idm = i.getInteractionDetectionMethod()
        it = i.getInteractionType()
        idA = i.getSpeciesA()
        idB = i.getSpeciesB()
        if idm not in interactionIDMs and it not in interactionType and idA not in taxIDInteractor and idB not in taxIDInteractor:
                interactions.append(i)
filter()


with open(SOURCEFOLDER+"wholeset.mitab","w") as fh:
    for i in interactions:
        fh.write(i.whole+"\n")
    print("\nfile written with {} PPI".format(len(interactions)))

