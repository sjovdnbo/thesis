import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

correlationlocation = sys.argv[1]
phat3location = sys.argv[2]
speciescontrlocation = sys.argv[3].strip()


correlationfh = open(correlationlocation)
speciesfh = open(speciescontrlocation)

correlationfh.readline()
correlationfh.readline()
correlationfh.readline()

colors = ['#ff6666','#ffb366','#ffff66','#b3ff66','#66ff66','#66ffb3','#66b3ff',"#6666ff",'#d24dff','#ff4dd2','#ff668c']

correlationDict = {}
print("making correlation dict...")

for i in correlationfh:
    intA,intB,corr = i.split()
    correlationDict[intA.lower()+"_"+intB.lower()]=float(corr)

print(sorted(correlationDict.items())[:5])
def makeDict(fileLocation):
    db = {}
    for i in open(fileLocation):
        try:
            ptr2 = i.split("\t")[0].lower()
            ptr3 = i.split("\t")[4].strip().lower()
            if ptr2 not in db.keys() and ptr2 !="" and ptr3 != "":
                db[ptr2] = ptr3
        except IndexError:
            pass
            #print(i)
    print(sorted(db.items())[:5])
    return db
def ptr2toPtr3(ptr2, db):
    try:
        return db[ptr2]
    except KeyError:
        #print("Could not find ptr2 id {}".format(ptr2))
        return ("ptr2",ptr2)
#phatrdict = makeDict(phat3location)

dictPCC = {1:[],2:[],3:[],4:[],5:[]}
print('making correlations')
for line in speciesfh:
    interaction,species = line.strip().replace("{","'").replace("}","'").strip("'").split("\t")
    intA,intB = interaction.split(",")
    try:
        intA = intA.strip('(').strip(')').strip(" ").strip("'").lower().strip("phatr").strip("draft")
        #intA = ptr2toPtr3(intA,phatrdict)
        intA = "ptri{}".format(intA.strip("i"))

        try:

            intB = intB.strip('(').strip(')').strip(" ").strip("'").lower().strip("phatr").strip("draft")
            intB = "ptri{}".format(intB.strip("i"))
            print(intA+"\t"+intB)
            #intB = ptr2toPtr3(intB, phatrdict)
            speciesnr = species.split(",")
            for i in range(len(speciesnr)):
                try:
                    dictPCC[len(speciesnr)].append(correlationDict["{}_{}".format(intA, intB)])
                except KeyError:
                    try:
                        dictPCC[len(speciesnr)].append(correlationDict["{}_{}".format(intB, intA)])
                    except KeyError:
                        pass
                        #print("key not found:", intA, intB)
        except KeyError:
            print(intB)
    except KeyError:
        print(intA)

a = [0.4,0.3,0.2,0.5,0.1]
b = [0.5,0.6,0.7,0.7,0.6,0.8,0.5,0.6,0.7,0.7,0.6,0.8]
d = {1:a,2:b}
x=np.arange(-1,1,0.1)
fig, ax = plt.subplots()
for i in range(1,6):
    print(len(dictPCC[i]))
    if sum(dictPCC[i])<0:
        sns.distplot(np.asarray([j for j in dictPCC[i]]),rug=False,hist=False,fit_kws="gau", color=colors[(i-1)*2], label = "{} species".format(i))


plt.title("Coexpression by number of species support")
#plt.xticks(index,tuple(run2keys),rotation=60)
plt.yticks()
plt.xlabel("PCC")
plt.ylabel("Kernel density estimate")
plt.legend(loc=2)
fig.tight_layout()
ax.grid(b=False)
ax.set_axis_bgcolor('white')

fig.savefig("{}.png".format("spContrPcc"), dpi=500)


