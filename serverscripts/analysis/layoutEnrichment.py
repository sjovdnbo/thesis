import sys

enrichmentfile = open(sys.argv[1])
head = [next(enrichmentfile) for x in range(7)]

hrfile = open("/group/transreg/emcae/GOtermsPTR.csv")

outfile = open("readablefile_{}".format(sys.argv[1]),'w')

d = {}
for i in hrfile:
    go,_,annot,string = i.strip().split("\t")
    if go in d.keys():
        pass
    else:
        d[go] = (annot,string)


for i in enrichmentfile:
    cluster, go,pval, _, enrfold, setsize, _, hits = i.split("\t")
    outfile.write("{}\t{},{},{},{},{},{}\n".format(cluster,d[go][0],go,enrfold,pval,round(int(hits)/int(setsize),3),d[go][1]))