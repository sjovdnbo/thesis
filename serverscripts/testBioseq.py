from Bio import SeqIO

sequenceLocation = "uniparc_active.fasta"
#sequenceLocation = "data/protseq.fasta"

record_dict = SeqIO.index(sequenceLocation, "fasta")

print(record_dict["UPI0000126777"])  # use any record ID