def readFasta(filename):
    seqs = {}
    with open(filename) as fh:
        name = None
        s = ''
        for line in fh:
            line = line.rstrip()
            if line[0] == '>':  # or line.startswith('>')
                if name:
                    seqs[name] = s
                #name = line[1:].split(" ")[0]  # uniparct gene parsing
                name = line[1:].split("|")[1] #uniprot fasta parsing
                seqs[name] = ''
                s = ''
            else:
                s = s + line
        if name:  # just checking against an empty file
            seqs[name] = s
    return seqs

