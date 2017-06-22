import sys

stringLocation = sys.argv[1]
ppi = {}
if stringLocation == "help":
    print("help\n-----\nargument 1 = location of string file\nargument 2 = location and name of outfile\n-----")
    sys.exit("help terminated")
outLocation = sys.argv[2]
maplocation = sys.argv[3]
interactions = ["1100","0064",'0205','0933','0190','0797','0934','1284','1271','0935','0795','0796','1280','1292','1278','1279','0794','1286','0932','1289','1288','1275','1276','1287','1295','1277','1272','1274','1273','1285','1290','1291','1293','1294','1282','1281','1283']
interactionIDMs = list(set(["0001","0063","0046","2231","0064","0037","0110","0024","0087","0058","0036","0057","0085","0100","1177","0101","0105","0686","0026","0036","0037","1178","1176","1177","0105","0035",'0026','0037','0660','0659','0363','0364','0362','0577','0035','0057','0085','0036','1177','0100','0087','0024','1100','2231','1178','1176','0101','0046,','0105','0058','0063','0686',"0064"]))
interactionIDMs.extend(interactions)
joint = interactionIDMs
taxIDInteractor = ["-2","-1","-"]
out = open(outLocation,'w')
ids = set()
mapdb = {}
def changeID(id,db):
    uniprot = 0
    entrez = 0
    ids = id.split("|")
    #print(ids)
    for i in ids:
        if "uniprot" in i:
            #print("uniprot")
            return i.split(":")[1]
        if "entrez" in i:
            try:
                #print("entrez")
                return db[i.split(":")[1]]
            except KeyError:
                return None
    return None
with open(maplocation) as fh:
    for line in fh:
        parsed = line.split("\t")
        uni,db,id = parsed
        if db == "GeneID":
            mapdb[id.strip('\n')] = uni
#print(len(mapdb.items()))
with open(stringLocation) as fh:
    ommitted = 0
    for i in fh:
        parsed = i.split("\t")
        id1 = changeID(parsed[0],mapdb)
        id2 = changeID(parsed[1],mapdb)
        if id1 == None or id2 == None:
            ommitted+=1
            continue
        pair = (id1,id2)
        if parsed[6] != '-':
            interaction = parsed[6].split(":",maxsplit=1)[1].split('(')[0].strip('"').strip("MI:")
        else:
            continue
        if parsed[11]!='-':
            idm = parsed[11].split(":",maxsplit=1)[1].split('(')[0].strip('"')
        else:
            continue
        if parsed[9] != '-' and parsed[10] != '-':
            if ":" not in parsed[9]:
                sp1 = parsed[9]
                sp2 = parsed[10]
            else:
                sp1 = parsed[9].split(':')[1]
                sp2 = parsed[10].split(':')[1]
        else:
            continue
        if interaction not in joint and idm not in joint and sp1 not in taxIDInteractor and sp2 not in taxIDInteractor and pair not in ids:
            ids.add(pair)
            parsed[0] = id1
            parsed[1] = id2
            out.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(*parsed))
print("ommitted entries: {}".format(ommitted))