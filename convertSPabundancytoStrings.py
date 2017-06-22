from getTaxIDString import getTaxID
with open("speciesabundancy1","r+") as fh:
    s = ""
    for i in fh:
        number, id = i.strip().split(" ")
        sp = str(getTaxID(str(id)))
        print(sp)
        s+=str(number)+"\t"+sp+"\n"
    fh.write(s)



