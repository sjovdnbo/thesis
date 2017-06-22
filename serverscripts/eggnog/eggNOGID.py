class eggNOGID:
    def __init__(self,string):
        parsed = string.split(".")
        self.taxid = parsed[0]
        self.gene = parsed[1]
        self.whole = self.taxid+"."+self.gene