import sys
from MI_UNIT_EX import MI_UNIT_EX
from MI_UNIT import MI_UNIT
from Bio import SeqIO
from readFasta import readFasta

locationIDmappingfile = "idmapping.dat"
locationDataset = "PPIdbsbatch1/wholeset.mitab"
sequenceLocation = "uniprot_trembl.fasta"
outlocation = "PPIdbsbatch1/wholesetExtended.mitab"



#locationIDmappingfile = "testidmapping.dat"
#locationDataset = "testdataset.mitab"
#sequenceLocation = "data/protseq.txt"
#outlocation = "wholesetExtended.mitab"

outfile = open(outlocation,"w")
datafile = open(locationDataset)


uniprotToGeneName = {}
entrezToUniprot = {}
tairToUniprot = {}
dIPtoUniprot =  {}
ensemblToUniprot = {}
chebiToUniprot = {}
ebiToUniprot = {}
refSeqToUniprot = {}

seqDB = {}
diperror = 0
def makeD():
    print("making dictionairies...")
    counterleftOut = 0
    counterAll = 0
    rest = []
    mapDB = open(locationIDmappingfile)

    for i in mapDB:
        uniprot= i.split()[0]
        name = i.split()[1]
        try: id = i.split()[2]
        except ValueError: print(i)
        if name == "Gene_Name" or name == "Gene_ORFName":  #uniprot parsing: gene ids
            if uniprot.upper() in uniprotToGeneName.keys():
                pass
            else:
                uniprotToGeneName[uniprot.upper()] = id.upper()
    mapDB.close()
    mapDB = open(locationIDmappingfile)
    for i in mapDB:
        uniprot = i.split()[0].upper()
        name = i.split()[1]
        try:
            id = i.split()[2].upper()
        except ValueError:
            print("maar 2 woorden in regel" + id)
        if name == "GeneID":
            try: entrezToUniprot[id] = uniprot
            except KeyError:
                print("entrez accession nr {} niet toegevoegd aan dict, geen uniprot beschikbaar".format(id))
        elif name == 'TAIR':
            try: tairToUniprot[id] = uniprot
            except KeyError:
                print("tair accession nr {} niet toegevoegd aan dict, geen uniprot beschikbaar".format(id))
        elif name == "DIP" or name == "dip":
            try: dIPtoUniprot[id.split("-")[1]] = uniprot
            except KeyError: print("dip accession nr {} niet toegevoegd aan dict, geen uniprot beschikbaar".format(id))
        elif name == "Ensembl":
            try: ensemblToUniprot[id] = uniprot
            except KeyError: print("ensembl accession nr {} niet toegevoegd aan dict, geen uniprot beschikbaar".format(id))
        elif name == "ChEMBL":
            try: chebiToUniprot[id] = uniprot
            except KeyError: print("chebi accession nr {} niet toegevoegd aan dict, geen uniprot beschikbaar".format(id))
        elif name == "EMBL":
            try:
                ebiToUniprot[id] = uniprot
            except KeyError:
                rest.append(i)
        elif name == "RefSeq":
            try: refSeqToUniprot[id.split(".")[0].split("_")[1]] = uniprot
            except KeyError: print("refseq accession nr {} niet toegevoegd aan dict, geen uniprot beschikbaar".format(id))

def makeFastalib():
    print("making sequence library...")
    return readFasta(sequenceLocation)



def convIdentifierToUniprot(entry,diperror=diperror):

    """
    @in: entry of id that needs to be translated to its corresponding UniprotID
    name is as they are depicted in the datafile, not in the mapping file
    """
    entry = entry.split("|")[0]
    try:
        name, id = entry.split(":")
        id = id.upper()
        name = name.lower()
        if name == "uniprotkb":
            return id.split("-")[0]
        elif name == "entrez gene/locuslink" or name == "entrezgene/locuslink":
            return entrezToUniprot[id]
        elif name == "tair":
            return tairToUniprot[id]
        elif name == "ensembl":
            return ensemblToUniprot[id]
        elif name == "refseq":
            return refSeqToUniprot[id]
    except KeyError:
        print("unable to map {} to {} with id {}".format(entry, name, id))
    except ValueError:
        if entry[:3] == "DIP":
            try:
                return dIPtoUniprot[entry.split("-")[1]]
            except KeyError:
                diperror+=1
                print("{} not found ".format(entry))
        else:
            print("problem parsing line entry: ", entry, ", should be name and id")

def getSeq(UniparcID):
    return seqDB[UniparcID]


#########################
dataset = set()

makeD()
#print(convIdentifierToUniprot("DIP-935N"),convIdentifierToUniprot("DIP-31142N"))
#print(uniprotToGeneName["Q16611"],uniprotToGeneName["O14908"])  # works
seqDB = makeFastalib()

print("starting conversion...")
print("----------------------------\noutput:\n----------------------------")

noSeqFoundErr= 0
redErr = 0
noGeneIDErr=0
for i in datafile:
    mi = MI_UNIT(i)
    sequenceA = "-"
    sequenceB = "-"
    if "innate" in mi.idInteractorA.split(":")[0].lower():
        uIDA = convIdentifierToUniprot(mi.altIDsInteractorA)
        uIDB = convIdentifierToUniprot(mi.altIDsInteractorB)
    else:
        uIDA = convIdentifierToUniprot(mi.idInteractorA)
        uIDB = convIdentifierToUniprot(mi.idInteractorB)
    #print(mi.idInteractorA+"\t Uniprot: \t{}".format(str(uIDA)))
    #print(mi.idInteractorB+"\t uniprot: \t {}".format(str(uIDB)))
    try:
        geneA = uniprotToGeneName[uIDA]
        try:
            geneB = uniprotToGeneName[uIDB]

            e = MI_UNIT_EX(mi, geneA, geneB,uIDA,uIDB)
            if e not in dataset:
                dataset.add(e)
                try:
                    sequenceA = getSeq(uIDA)
                    try:
                        sequenceB = getSeq(uIDB)
                        outfile.write(mi.whole + "\t{}\t{}\t{}\t{}\t{}\t{}\n".format(geneA, geneB,uIDA,uIDB, sequenceA, sequenceB))
                    except KeyError:
                        #print("no sequence found for entry {}".format(geneB))
                        noSeqFoundErr += 1
                except KeyError:
                    #print("no sequence found for entry {}".format(geneA))
                    noSeqFoundErr += 1
            else:
                redErr+=1

        except KeyError:
            geneB = None
            noGeneIDErr += 1
    except KeyError:
        geneB = None
        noGeneIDErr+=1

print("unmapped id's because of dip id absent: {}".format(diperror))
print("unmapped id's because of absent gene id: {}".format(noGeneIDErr-diperror))
print("unmapped id's because of absent gene seq: {}".format(noSeqFoundErr))
print("unmapped id's because of redundancy filtering: {}".format(redErr))


