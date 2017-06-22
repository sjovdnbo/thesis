import matplotlib.pyplot as plt
import matplotlib
import operator
#parameters
cutoff = 7000
source = "databases.txt"

#init
db = {"Other":0}
legend = {"Other":"Other databases","MI:0463": "biogrid", "MI:0469":"IntAct","MI:0471":"MINT","MI:2165":"BAR","MI:0465":"DIP","MI:1114":"virhostnet"}
with open(source) as fh:
    for line in fh:
        freq,rest = line.split(maxsplit=1)
        freq = int(freq)
        rest = rest.split("|")
        if rest != '-':
            ids = list(set([i.strip("psi-mi:").split('(')[0].strip('"').upper() for i in rest]))
            for id in ids:
                if id in legend.keys():
                    if id not in db.keys():
                        db[id] = freq
                    else:
                        db[id] += freq
                else:
                    db["Other"] += freq





top10 = sorted(db.items(), key=operator.itemgetter(1))[::-1][:10]
print(top10)
labels = [legend[i[0]] for i in top10]
sizes = [i[1] for i in top10]
#labels.append(legend["Other"])      #restscore toevoegen aan labels en grafiek data
#sizes.append(db["Other"])
colors = ['#ff6666','#ffb366','#b3ff66','#66ff66','#66b3ff',"#6666ff",'#d24dff','#ff4dd2','#ff668c']
fig1,ax1 = plt.subplots()

ax1.pie(sizes,pctdistance=0.9,labels=[""]*len(labels),colors=colors,autopct='%1.1f%%',startangle=90)
ax1.axis('equal')
plt.suptitle("Source database contribution",fontsize = 20)
plt.legend(labels=labels,bbox_to_anchor=(0.9,0.9))
matplotlib.rcParams["font.size"] = 12.0
matplotlib.rcParams["font.family"] = 'font.fantasy'

plt.show()