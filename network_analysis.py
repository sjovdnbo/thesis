import os,operator,decimal
PATH = "data/network analysis/"
CRITERION = "BetweennessCentrality"
TOP = 15

MAX = 0.99
MIN = 0
overallDict = {"eggnog_nf":{},"eggnog_f":{},"plaza_lib_nf":{},"plaza_lib_f":{},"plaza_reg_nf":{},"plaza_reg_f":{},"string_nf":{},"string_f":{}}

def gethubs(fh,criterion = CRITERION,top=TOP,minimum=MIN,maximum=MAX):
    header = fh.readline().strip().split(",")
    indexCriterion = [i.strip('"') for i in header].index(criterion)
    indexName = [i.strip('"') for i in header].index("name")
    dict = {}
    for line in fh:
        node = line.strip().split(",")[indexName].strip('"')
        degree = line.strip().split(",")[indexCriterion].strip('"')
        if 'E' in degree:
            degree = decimal.Decimal(degree)
        else:
            degree = float(degree)

        if minimum <= degree and degree <= maximum:
            #print(minimum, degree, maximum)
            dict[node]=degree
    avg = sum([float(i) for i in dict.values()])/len(dict.values())
    print("average {}: {}".format(CRITERION,avg))
    top = len(dict.items())/100*top
    return sorted(dict.items(),key=operator.itemgetter(1))[::-1][:int(top)]

def getCommonIDs(tuple1,tuple2):
    ids2 = [i[0] for i in tuple2]
    retained = [i for i in tuple1 if i[0] in ids2]
    return retained

def comparison(string,data1,data2):
    comp = getCommonIDs(overallDict[data1], overallDict[data2])
    print("{} : {} retained out of {} -> {}% \n\t {}".format(string,len(comp), len(overallDict[data1]),len(comp)/len(overallDict[data1])*100, comp))
    return comp

overallDict["eggnog_nf"] = gethubs(open(PATH + "int_eggnog_merged.csv"))
overallDict["eggnog_f"] = gethubs(open(PATH + "int_eggnog_merged_cof.csv"))
overallDict["plaza_lib_nf"] = gethubs(open(PATH + "int_plaza_lib_merged.csv"))
overallDict["plaza_lib_f"] = gethubs(open(PATH + "int_plaza_lib_merged_cof.csv"))
overallDict["plaza_reg_nf"] = gethubs(open(PATH + "int_plaza_reg_merged.csv"))
overallDict["plaza_reg_f"] = gethubs(open(PATH + "int_plaza_reg_merged_cof.csv"))
overallDict["string_nf"] = gethubs(open(PATH + "int_string.csv"))
overallDict["string_f"] = gethubs(open(PATH + "int_string_cof.csv"))




print("------------\nfiltered vs not filtered:\n------------")
comparison("plaza regular","plaza_reg_nf","plaza_reg_f")
comparison("plaza liberal","plaza_lib_nf","plaza_lib_f")
comparison("eggnog","eggnog_nf","eggnog_f")
comparison("string","string_nf","string_f")

print("\n------------\nfiltered: overall\n------------")
plaza = comparison("plaza regular vs liberal","plaza_reg_f","plaza_lib_f")
eggnog = comparison("string vs eggnog","string_f","eggnog_f")
retained = getCommonIDs(plaza,plaza)
print("retained hubs over all networks: {}\n {}".format(len(retained),retained))
outfile = open("data/network analysis/networkanalysisout.txt",'w')
for i in retained:
    outfile.write(i[0]+"\n")
#print(overallDict["string_nf"])