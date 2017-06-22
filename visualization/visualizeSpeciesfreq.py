import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import operator
from getTaxIDString import getTaxID
sns.set_style(style="white")

#titanic = sns.load_dataset("titanic")
#print(titanic)
"""
run1data = {"H. sapiens":309901,"S. cerevisiae (strain ATCC 204508)": 2*119414, "D. melanogaster": 56231,
            "A. thaliana": 38062, "M. musculus": 29576, "E. coli (strain K12)": 20800, "C. elegans":12922, "S. pombe": 9257, "Dipodomys": 5474,
            "S. cerevisiae": 4264,"C. jejuni": 3811,"Influenza A virus": 3497,"P. falciparum":2720}

run2data = {"H. sapiens": 315997, "S. cerevisiae (strain ATCC 204508)": 2*121987, "D. melanogaster": 56247,
            "A. thaliana": 38046, "M. musculus": 30212, "E. coli (strain K12)": 20812, "C. elegans": 12978,
            "S. pombe": 9248, "Dipodomys": 5419,
            "S. cerevisiae": 4264, "C. jejuni": 3811, "Influenza A virus": 3494, "B. anthracis": 2826}
"""
run2data= {}
run1data = {}
for i in open("species1.txt"):
    freq,sp = i.split(maxsplit=1)
    run1data[sp.strip()]=int(freq)
for i in open("species2.txt"):
    freq, sp = i.split(maxsplit=1)
    run2data[sp.strip()] = int(freq)

def concat(id):
    string = getTaxID(id)
    gen,sp = string.split(maxsplit=1)
    return gen[0].upper()+" "+sp.split()[0][:9]

sortedRun1 = sorted(run1data.items(),key = operator.itemgetter(1))[::-1][:12]
print(sortedRun1)
run1vals = [i[1] for i in sortedRun1]
sortedRun2 = sorted(run2data.items(),key = operator.itemgetter(1))[::-1][:12]
run2keys = [concat(i[0]) for i in sortedRun2]
run2keys[-1] = "Influenza A"
run2vals = [i[1] for i in sortedRun2]
index = np.arange(len(run2keys))
bar_width = 0.35
opacity = 0.8

f,ax1= plt.subplots()

print(run1vals)
graph1 = plt.bar(index,run1vals,bar_width,alpha=0.5,color='#d24dff',label="Datarun 1")
graph2 = plt.bar(index+bar_width,run2vals,bar_width,alpha=0.5,color='#ffb366',label = "Datarun 2")

plt.title("Dataset species abundancy comparison")
plt.xticks(index,tuple(run2keys),rotation=60)

plt.xlabel("Species")
plt.ylabel("Number of entries")
plt.legend()
f.tight_layout()

f.savefig("C:/Users/beheerder/Google Drive/univ/bioinformatics 2/thesis/figures/speciesfreq.png", dpi=500)

plt.show()

