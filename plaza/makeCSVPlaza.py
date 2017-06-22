import os
from Bio import SeqIO

proteomesfolder = "../data/proteomes/"

annotationfile = open("annotation.csv","w")
annotationsourcefile = open("annot_sources.csv","w")

proteomIDs = {"Sce":"http://www.uniprot.org/proteomes/UP000002311","Ptr": "http://www.uniprot.org/proteomes/UP000000759","Ath" : "http://www.uniprot.org/proteomes/UP000006548","Ban":"http://www.uniprot.org/proteomes/UP000000594","Cel":"http://www.uniprot.org/proteomes/UP000001940","Cje":"http://www.uniprot.org/proteomes/UP000000799", "Dme":"http://www.uniprot.org/proteomes/UP000000803","Eco":"http://www.uniprot.org/proteomes/UP000000625","Hsa":"http://www.uniprot.org/proteomes/UP000005640","Mmu":"http://www.uniprot.org/proteomes/UP000000589","Rno":"http://www.uniprot.org/proteomes/UP000002494","Tpa":"http://www.uniprot.org/proteomes/UP000000811","Ype":"http://www.uniprot.org/proteomes/UP000000815"}
speciesIDs = {'Sce':4932,"Ptr": 2850, "Ath":3702,"Ban":1392,"Cel":6329,"Cje":192222,"Dme":7227,"Eco":481805,"Hsa":9606,"Mmu":10090,"Rno":10116,"Tpa": 243276, "Ype": 632}
for filename in os.listdir(proteomesfolder):
    print("reading {}...".format(filename))
    fastaSeq = SeqIO.parse(proteomesfolder+filename,'fasta')

    species = filename.split(".")[0]
    shortsp = species.split("_")[0][0] + species.split("_")[1][:2]
    outSource = "'','{}','NA','{}','{}','{}','NA','NA','0','{}','NA','NA','NA'\n".format(proteomIDs[shortsp],
                                                                                        shortsp,species,
                                                                                        shortsp,
                                                                                        speciesIDs[shortsp])
    annotationsourcefile.write(outSource)

    for fasta in fastaSeq:
        if shortsp == "Ptr":
            geneid = fasta.id.split("|")[1]
        else:
            split = fasta.id.split("|")
            geneid = split[2]
        seq = fasta.seq
        outAnnot= "'{}','{}','NA','NA','0','0','NA','{}','NA','NA','coding','eq','eq','0'\n".format(geneid, shortsp, seq)
        annotationfile.write(outAnnot)
