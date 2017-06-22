import sys

mappingfile = sys.argv[1]


if mappingfile == "help":
    print("help with arguments\n"
            "-------------------\n"
          "Argument 1 = location of file with mapping table\n"
        "Argument 2 = location of file to be mapped\n"
        "Argument 3 = destination location and filename\n-------------------"
          )
    sys.exit("script stopped after help")

mapableFile = sys.argv[2]
outfile = open(sys.argv[3],'w')

def parseID(id):
    if "draft" in id:
        id = id.split("draft")[1]
    else:
        id = id.split("r")[1]
    return id

def makeDict(fileLocation):
    db = {}
    for i in open(fileLocation):
        try:
            ptr2 = i.split("\t")[0]
            ptr3 = i.split("\t")[4].strip()
            if ptr2 == "13400":
                print("nu")
            if ptr2 not in db.keys() and ptr2 !="" and ptr3 != "":
                db[ptr2] = ptr3
        except IndexError:
            print(i)
    return db

def ptr2toPtr3(ptr2, db):
    try:
        return db[ptr2]
    except KeyError:
        print("Could not find ptr2 id {}".format(ptr2))
        return None

db = makeDict(mappingfile)
count = 0

for i in open(mapableFile):
    s= i.split()
    intA = s[0]
    intB = s[1]
    intA = ptr2toPtr3(parseID(intA),db)
    intB = ptr2toPtr3(parseID(intB),db)
    if intA != None and intB != None:
        outfile.write(intA+"\t"+intB+"\n")
    else:
        count +=1
print("mappings ommitted: {} entries were not retrieved from mapping.".format(count))
