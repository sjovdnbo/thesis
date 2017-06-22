class MI_UNIT:
    def __init__(self, string):
        l = string.strip("\n").split("\t")
        self.idInteractorA = l[0].split("|")[1].split(":")[1].split["_"][0]
        self.idInteractorB = l[1].split("|")[1].split(":")[1].split["_"][0]
        self.altIDsInteractorA = l[2]
        self.altIDsInteractorB = l[3]
        self.aliasesInteractorA = l[4]
        self.aliasesInteractorB = l[5]
        self.interactionDetectionMethod = l[6]
        self.publication1stAuthor = l[7]
        self.publicationIdentifiers = l[8]
        self.taxidInteractorA = l[9]
        self.taxidInteractorB = l[10]
        self.interactionTypes = l[11]
        self.sourceDatabase = l[12]
        self.interactionIdentifiers = l[13]
        self.confidence = l[14]

        self.whole = self.idInteractorA+"\t"+self.idInteractorB+"\t"+self.altIDsInteractorA+"\t"+self.altIDsInteractorB+"\t"+self.aliasesInteractorA+"\t"+self.aliasesInteractorB+"\t"+self.interactionDetectionMethod+"\t"+self.publication1stAuthor+"\t"+self.publicationIdentifiers+"\t"+self.taxidInteractorA+"\t"+self.taxidInteractorB+"\t"+self.interactionTypes+"\t"+self.sourceDatabase+"\t"+self.interactionIdentifiers+"\t"+self.confidence.strip()

    def __str__(self):
        return "interaction " + self.idInteractorA + " with " + self.idInteractorB

    def decode(self, string):
        h = 0
        for i in string:
            if i.isdigit() == True:
                h += int(i) ** 2
            else:
                h += ord(i) ** 2
        return h

    def getSpeciesA(self):
        if self.taxidInteractorA != "-":
            if ":" not in self.taxidInteractorA:
                return self.taxidInteractorA
            else:
                if "(" in self.taxidInteractorA:
                    s = self.taxidInteractorA.split(":")[1].split("(")[0].strip('"')
                else:
                    s = self.taxidInteractorA.split(":")[1].strip('"')
                return s
        else:
            return self.taxidInteractorA

    def getSpeciesB(self):
        if self.taxidInteractorB != "-":
            if ":" not in self.taxidInteractorB:
                return self.taxidInteractorB
            else:
                if "(" in self.taxidInteractorB:
                    s = self.taxidInteractorB.split(":")[1].split("(")[0].strip('"')
                else:
                    s = self.taxidInteractorB.split(":")[1].strip('"')
                return s
        else:
            return self.taxidInteractorB

    def __eq__(self, other):
        if (self.idInteractorA == other.idInteractorA and self.idInteractorB == other.idInteractorB) or (self.idInteractorA == other.idInteractorB and self.idInteractorB == other.idInteractorA):
            l1 = self.getPubmedList()
            l2 = other.getPubmedList()
            l3 = [val for val in l1 if val in l2]
            if len(l3) >=1:
                return True
            else:
                return False
        else:
            return False


    def getPubmedList(self):
        if self.publicationIdentifiers == "-":
            return []
        else:
            s = self.publicationIdentifiers.split("|")
            return s
    def getTaxIDInteractorA(self):
        return self.taxidInteractorA
    def getDatabase(self):
        if self.sourceDatabase == "-":
            return "-"
        else:
            db =  self.sourceDatabase.split("MI:")[1]
            if "(" in db:
                db = db.split("(")[0]
            db = db.strip('"')
            return db

    def getInteractionType(self):
        try:
            if self.interactionTypes.strip() == '-':
                return '-'
            else:
                if "IA:" in self.interactionTypes:
                    it = self.interactionTypes.split("IA:")[1]
                else:
                    it = self.interactionTypes.split("MI:")[1]
                if "(" in it:
                    it = it.split("(")[0]
                it = it.strip('"')
                return it

        except IndexError:
            print(IndexError,"InteractionType:",self.interactionTypes)

    def getInteractionDetectionMethod(self):
        method = self.interactionDetectionMethod
        try:
            if method.strip() == "-":
                return method
            else:
                r = self.interactionDetectionMethod.split(":")[2].split('(')[0].strip('"')
                return r
        except IndexError:
            print(IndexError,"interactionDetectionMethod:",method)


