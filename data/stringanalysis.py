stringfh = open("stringnetwork.csv")
def readline_string(line):
    interaction = line.split(",")[2]
    intA,intB = interaction.split("(interacts with)")
    intA = int(intA.strip('"').strip().strip("ptri"))
    intB = int(intB.strip('"').strip().strip("ptri"))
    return intA,intB
print(stringfh.readline())

histonlist = [115670,155330,123960,100700,8160,159290,159130,155960,161230,98780,159250,234250,159110]

for i in stringfh:
    intA,intB = readline_string(i)
    if intA in histonlist and intB in histonlist:
        print("ptri{} and ptri{} connect".format(intA,intB))
