import matplotlib.pyplot as plt
import matplotlib
import operator
#parameters
cutoff = 7000
source = "technologies.txt"

#init
db = {'Other':0}
legend = {"Other":"Other technologies","MI:0004": "affinity chromatography technologies", "MI:0018":"two-hybrid","MI:0096":"pull-down","MI:0696":"tandem affinity purification","MI:0007":"anti-tag coimmunoprecipitation","MI:0401":"biochemical","MI:1112":"two-hybrid prey pooling approach","MI:0397":"two-hybrid array","MI:0006": "anti-bait coimmunoprecipitation","MI:0090":"protein complementation assay"}
with open(source) as fh:
    for line in fh:
        freq,rest = line.split(maxsplit=1)
        freq = int(freq)
        rest = rest.split("|")
        if rest != '-':
            for id in rest:
                id = id.strip("psi-mi:")
                id = id.split('(')[0].strip('"').upper()
                if id in legend.keys():
                    if id not in db.keys():
                        db[id]= freq
                    else:
                        db[id]+=freq
                else:
                    db["Other"]+=freq

top10 = sorted(db.items(), key=operator.itemgetter(1))[::-1][:10]
print(top10)
labels = [legend[i[0]].capitalize() for i in top10]
sizes = [i[1] for i in top10]
colors = ['#ff6666','#ffb366','#ffff66','#b3ff66','#66ff66','#66ffb3','#66b3ff',"#6666ff",'#d24dff','#ff4dd2','#ff668c']
fig1,ax1 = plt.subplots()

ax1.pie(sizes,pctdistance=0.9,labels=[""]*len(labels),colors=colors,autopct='%1.1f%%',startangle=90)
ax1.axis('equal')
plt.suptitle("Experimental PPI techologies",fontsize = 20)
plt.legend(labels=labels)
matplotlib.rcParams["font.size"] = 12.0
matplotlib.rcParams["font.family"] = 'font.fantasy'

plt.show()