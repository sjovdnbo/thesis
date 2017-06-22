import sys

file2 = open("orthology/interologyPlazaSimple.txt")
file1= open("orthology/interologyPlaza.txt")
genes1 = {}

def readfile(file):
    genes = set()
    interactions = set()
    for line in file:
        try:
            gene1,gene2 = line.strip().split()
            gene1 = gene1.strip()
            gene2 = gene2.strip()
            if gene1 not in genes:
                genes.add(gene1)
            if gene2 not in genes:
                genes.add(gene2)
            if (gene1,gene2) not in interactions:
                if (gene2,gene1) not in interactions:
                    interactions.add((gene1,gene2))
        except ValueError:
            #print(line)
            continue
    return genes,interactions

genes1,interactions1 = readfile(file=file1)
genes2,interactions2 = readfile(file=file2)
print(len(interactions1.intersection(interactions2)))


