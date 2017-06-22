import sys,os
import decimal
clusterfile = sys.argv[1]
out = ""
fh = open(clusterfile,encoding='utf-8-sig')
fh.readline()
for i in fh:
    line = i.split('NaN')[1].split('"')
    line = [i for i in line if i != ","]

    pval = line[0].strip("'")
    pval = float(str(pval).replace(",","."))

    genelist = line[1]
    clusternumber = i.split(",")[0]
    if pval<0.05:
        for id in genelist.split(" "):
            id = "cluster{}\t{}".format(clusternumber,id)
            out+=id+"\n"
os.remove(clusterfile)
open(clusterfile,'w').write(out)

