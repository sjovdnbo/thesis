l = []
with open("mapper.sh.o7015036") as fh:
    for i in fh:
        if i[:3].lower() == "dip":
            l.append(i.split(" ")[0])

print(len(l))