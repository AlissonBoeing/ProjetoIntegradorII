class Treasure:
    #Exemplo do que chega em lcacas  ->  "1:1;2:3;5:2;6:6;4:3;2:1"
    def __init__(self, l):
        self.l1 = list(l.split(';'))
        self.lcacas = l
        # pega só a partir do setimo caracter e fica 1:1;2:3;5:2;6:6;4:3;2:1
        # ['1:1', '2:3', '5:2', '6:6', '4:3', '2:1']

    def getList(self):
        return self.l1

    def getString(self):
        return self.lcacas
