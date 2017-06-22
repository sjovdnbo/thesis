import matplotlib.pyplot as plt
import matplotlib
import operator
#parameters
cutoff = 7000
source = "interactions.txt"

#init
db = {"Other":0}
legend = {"Other":"Other interactions","MI:0915": "physical association", "MI:0407":"direct interaction","MI:0914":"association","MI:0403":"colocalization","MI:0218":"physical interactions"}
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
labels = [legend[i[0]].capitalize() for i in top10]
sizes = [i[1] for i in top10]
#labels.append(legend["Other"])      #restscore toevoegen aan labels en grafiek data
#sizes.append(db["Other"])
colors = ['#ff6666','#ffb366','#ffff66','#66ff66','#66b3ff','#d24dff','#ff668c']
fig1,ax1 = plt.subplots()

ax1.pie(sizes,pctdistance=0.9,labels=[""]*len(labels),colors=colors,autopct='%1.1f%%',startangle=90)
ax1.axis('equal')
plt.suptitle("Protein interactions",fontsize = 20)
plt.legend(labels=labels,bbox_to_anchor=(0.9,0.9))
matplotlib.rcParams["font.size"] = 12.0
matplotlib.rcParams["font.family"] = 'font.fantasy'

plt.show()