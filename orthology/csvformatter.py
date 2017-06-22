import os

def format(fh):
    out = ""
    fh.readline()
    for i in fh:
        id = i.split(",")[1].strip('"')
        out+="netw\t{}\n".format(id.strip())
    return out

for file in ["networkeggnog.csv","networkmerged.csv","networkplaza.csv","networkplazalib.csv"]:
    fh = open("wholenetworks/"+file)
    out = format(fh)
    fh.close()
    new = open("wholenetworks/"+file.split('.')[0]+'.txt','w')
    new.write(out)

