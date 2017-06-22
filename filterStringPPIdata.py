import sys

stringLocation = sys.argv[1]

if stringLocation == "help":
    print("help\n-----\nargument 1 = location of string file\nargument 2 = location and name of outfile\n-----")
    sys.exit("help terminated")
outLocation = sys.argv[2]
interactions = ['0205','0933','0190','0797','0934','1284','1271','0935','0795','0796','1280','1292','1278','1279','0794','1286','0932','1289','1288','1275','1276','1287','1295','1277','1272','1274','1273','1285','1290','1291','1293','1294','1282','1281','1283']
interactionIDMs = ['0026','0037','0660','0659','0363','0364','0362','0577','0035','0057','0085','0036','1177','0100','0087','0024','1100','2231','1178','1176','0101','0046,','0105','0058','0063','0686',"0064"]
taxIDInteractor = ["-2","-1","-"]
out = open(outLocation,'w')
with open(stringLocation) as fh:
    for i in fh:
        parsed = i.split()
        interaction = parsed[6].split(":")[2].split('"')[0]
        idm = parsed[11].split(":")[2].split('"')[0]
        sp1 = parsed[9].split(':')[1]
        sp2 = parsed[10].split(':')[1]
        if (interaction not in interactions) and (idm not in interactionIDMs) and sp1 not in taxIDInteractor and sp2 not in taxIDInteractor:
            out.write(i+"\n")
