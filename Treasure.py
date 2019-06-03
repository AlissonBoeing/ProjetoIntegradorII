class Treasure:

    def __init__(self, l):           # "1:1;2:3;5:2;6:6;4:3;2:1"
        self.l1 = list(l.split(';')) # ['1:1', '2:3', '5:2', '6:6', '4:3', '2:1']
        self.lcacas = l              # "1:1;2:3;5:2;6:6;4:3;2:1"

    def getList(self):
        return self.l1

    def getString(self):
        return self.lcacas

    #usei tal funcao em SistemaRobo linha 115
    def removeCaca(self, alvo):
        self.l1.remove(alvo)             #remove a caca alvo
        self.lcacas = ';'.join(self.l1)  # traduz ed lista para string separando por ';'

    #Remove de self.l1 a caca mais proxima e a retorna
    def getCloserTarget(self, posRobo):
        #Exemplo posRobo -> '6:4' ou '2:0' ou '1:3' ou '5:5'...
        rbx = int(posRobo[0])
        rby = int(posRobo[2])

        #pega primeiro elemento da lista para poder comparar com outros elementos
        closer = self.l1[0]
        clx = int(closer[0])
        cly = int(closer[2])

        # compara e acha a caca mais proxima
        for i in self.l1:
            tex = int(i[0])
            tey = int(i[2])

            if abs(rbx-tex) + abs(rby-tey) < abs(rbx-clx) + abs(rby-cly):
                closer = str(tex) + ':' + str(tey) #'3:4'
                clx = int(closer[0])
                cly = int(closer[2])

        if closer in self.l1:
            self.l1.remove(closer)
        return closer

    # Ordena as cacas da melhor maneira para se busca-las
    # Atualiza self.l1 e tambem ja arruma a string self.lcacas
    def ordenaListaCaca(self, posRobo):
        ordenada = []
        loop = range(len(self.l1))
        for i in loop:
            if i == 0:
                ordenada.append(self.getCloserTarget(posRobo))
            else:
                ordenada.append(self.getCloserTarget(ordenada[i-1]))

        self.l1 = ordenada
        self.lcacas = ';'.join(self.l1) # traduz lista em string. Elementos separados por ponto-e-virgula

##########  testes  ###############
# treasure = Treasure('1:1;1:3;2:1;2:3')

# treasure.ordenaListaCaca('0:0')

# lista = treasure.getList()

# for i in lista:
#     print('Elemento: ' + i)
