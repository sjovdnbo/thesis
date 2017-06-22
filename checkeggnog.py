with open("NOG.members.tsv") as fh:
    for i in fh:
        l = i.split("\t")[-1]
        sp = [i.split(".")[0] for i in l.split(",")]
        c = (sp.count("2850"))
        if c > 1:
            print(c)
