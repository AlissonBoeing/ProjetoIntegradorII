class Treasure:
    #Exemplo do que chega em lcacas  ->  "cacas,1:1;2:3;5:2;6:6;4:3;2:1"
    def _init_(self, lcacas):
        self.l1 = list(self.lcacas[6:].split(';'))
        self.lcacas = lcacas[6:]
        # pega só a partir do setimo caracter e fica 1:1;2:3;5:2;6:6;4:3;2:1
        # ['1:1', '2:3', '5:2', '6:6', '4:3', '2:1']

    def getList(self):
        return self.l1

    def getString(self):
        return self.lcacas
