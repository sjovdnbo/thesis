oGtoPTR = {}
for i in open("NOG.members.tsv"):
	l = i.split()
	OG = l[1]
	ids = l[5].split(',')
	if OG == "ENOG410ZQ99":
		print("OG = 410ZQ99")