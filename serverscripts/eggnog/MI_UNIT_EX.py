from MI_UNIT import MI_UNIT
class MI_UNIT_EX():
    def __init__(self, mi, geneA=None, geneB=None, uniprotA=None,uniprotB=None,new=True):
        if new==True:
            self.mi = mi
            self.geneA = geneA
            self.geneB = geneB
            self.uniprotA = uniprotA
            self.uniprotB = uniprotB
            self.seqA = "-"
            self.seqB = "-"
        else:
            l=mi.split("\t")
            self.idInteractorA = l[0].split("|")[0]
            self.idInteractorB = l[1].split("|")[0]
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
            self.geneA = l[15]
            self.geneB = l[16]
            self.uniprotA = l[17]
            self.uniprotB = l[18]
            self.seqA = l[19]
            self.seqB = l[20]


    def setGeneA(self, gene):
        self.geneA = gene
    def setGeneB(self, gene):
        self.geneB = gene
    def getGeneA(self):
        return self.geneA
    def getGeneB(self):
        return self.geneB
    def getUniprotIdA(self):
        return self.uniprotA
    def getUniprotIdB(self):
        return self.uniprotB
    def setSequenceA(self,string):
        self.seqA = string
    def getSequenceA(self):
        return self.seqA
    def getSequenceB(self):
        return self.seqB

    def __hash__(self):
        return hash(self.geneA) + hash(self.geneB)

    def __eq__(self, other):
        #try:
        if self.__hash__() == other.__hash__():
            return True
        else:
            return False
        """except:"""
    def __str__(self):
        return self.geneA + ", " + self.geneB