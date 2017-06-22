from MI_UNIT import MI_UNIT
class DATABASE_MI:
    def __init__(self):
        self.dataframe = []
        self.size = 0

    def __add__(self, other):
        self.dataframe.append(other)
        self.size +=1

    """
    niet goed!
    other moet gecast worden!

                MI_UNIT(other) == other
    """
    def __contains__(self, item):
        for i in self.dataframe:
            if i.__eq__(item):
                return True
        return False

    def __sizeof__(self):
        return self.size
    def __str__(self):
        return "database of mitab units, with size "+str(self.size)

    def getDBDict(self):
        map = {}
        for i in self.dataframe:
            db = i.getDatabase()
            if db in  map.keys():
                map[db]+=1
            else:
                map[db] =0
        return map
