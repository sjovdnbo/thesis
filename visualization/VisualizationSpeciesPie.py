import matplotlib.pyplot as plt
import matplotlib
import operator
from getTaxIDString import getTaxID
#parameters
source = "species2.txt"

#init
db = {'Other':0}
legend = {"632":"Yersinia pestis","381518":"Influenza A virus","Other":"Other species","284812": "Schizosaccharomyces pombe 972h-","6239":"Caenorhabditis elegans","9606": "Homo sapiens", "10090":"Mus musculus","83333":"Escherichia coli K-12","7227":"Drosophila melanogaster","559292":"Saccharomyces cerevisiae S288C","3702":"Arabidopsis thaliana"}
with open(source) as fh:
    for line in fh:
        freq,rest = line.split(maxsplit=1)
        freq = int(freq)
        rest = rest.split("|")
        if rest != '-':
            ids = list(set([i.strip("taxid:").split('(')[0].strip() for i in rest]))
            #print(ids)
            for id in ids:
                if id in legend.keys():
                    if id not in db.keys():
                        db[id]= freq
                    else:
                        db[id]+=freq
                else:
                    db["Other"]+=freq

top10 = sorted(db.items(), key=operator.itemgetter(1))[::-1][:15]
print(top10)
labels = [legend[i[0]].capitalize() for i in top10]
sizes = [i[1] for i in top10]
colors = ['#ff6666','#ffb366','#ffff66','#b3ff66','#66ff66','#66ffb3','#66b3ff',"#6666ff",'#ahj','#ff4dd2','#ff668c']
fig1,ax1 = plt.subplots()

ax1.pie(sizes,pctdistance=0.9,labels=[""]*len(labels),colors=colors,autopct='%1.1f%%',startangle=90)
ax1.axis('equal')
plt.suptitle("Species frequency",fontsize = 20)
plt.legend(labels=labels)
matplotlib.rcParams["font.size"] = 12.0
matplotlib.rcParams["font.family"] = 'font.fantasy'

plt.show()