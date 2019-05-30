class Treasure:

    def __init__(self, l):           # l      ->  "1:1;2:3;5:2;6:6;4:3;2:1"
        self.l1 = list(l.split(';')) # l1     -> ['1:1', '2:3', '5:2', '6:6', '4:3', '2:1']
        self.lcacas = l              # String -> 1:1;2:3;5:2;6:6;4:3;2:1

    def getList(self):
        return self.l1

    def getString(self):
        return self.lcacas

    