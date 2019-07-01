from ev3dev.ev3 import *
import time
from Treasure import *
import threading

class Robo(threading.Thread):

    def __init__(self, vel, modo,  sentido, posin, li):
        threading.Thread.__init__(self)
        self.setDaemon(False)
        self.velocidade  = vel
        self.l           = LargeMotor('outA')# esquerda
        self.r           = LargeMotor('outD')# direita
        self.cl          = ColorSensor()
        self.colors      = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
        self.id          = 'a0:f3:c1:0b:3c:48'
        #self.cor         = cor
        self.sentido     = sentido
        self.modo        = modo
        self.posX        = int(posin[0])
        self.posY        = int(posin[2])
        self.treasure    = Treasure(li)
        self.parado      = True
        self.estounacaca = False
        self.goal        = 0
        self.matar       = False
        self.setPausar()
        self.ladversario = []

    def getladversario(self):
        #return self.ladversario
        return self.ladversario

    def setladversario(self, ladversario):
        self.ladversario = ladversario

    def setMatar(self,val):
        self.matar = val

    def getGoal(self):
        return str(self.goal)

    def getTreasure(self):
        return self.treasure

    def isNacaca(self):
        return self.estounacaca

    def run(self):
        j = 0
        self.moverAutomatico()
                #self.treasure.ordenaListaCaca(self.getPos())
                #time.sleep(4)

    def getPos(self):
        return (str(self.posX) + ":" + str(self.posY))

    def isParado(self):
        return self.parado

    def setLista(self,lista): #verificar se o goal esta na lista, se nao seta matar
        #comparar com a que ja esta no robo, e se a caca que ele esta ido atras ainda existe
        listaatt = Treasure(lista)
        #listaatt = listaatt.ordenaListaCaca(self.getPos)
        if(not self.getGoal in listaatt.getString()):
            self.treasure = listaatt
            self.setMatar(True)
        else:
            self.treasure = listaatt

    def command(self, comando):
        if comando in 'Ww':
            self.moverFrente()

        elif comando in 'Aa':
            self.moverEsquerda()

        elif comando in 'Ss':
            self.moverRetornar()

        elif comando in 'Dd':
            self.moverDireita()

        elif comando in 'Vv':
            self.obterCaca()

    #Isso aqui eh aqui mesmo?
    def obterCaca(self):
        self.estounacaca = True

    #isso aqui eh aqui mesmo?
    def atualizarMapa(self):
        pass

    def getId(self):
        return self.id

    def getColor(self):
        return self.cor

    def setVel(self, vel):
        if vel < 1000 and vel > 0:
            self.velocidade = vel
        else:
            print('Somente valores de 0 a 999')

    def setPausar(self):
        self.r.stop(stop_action="hold")
        self.l.stop(stop_action="hold")

    def setSentido(self, sentido):
        if sentido in 'NSLO':
            self.sentido = sentido
        else:
            print('Somente permitidos N ou S ou L ou O para sentido')

    def setNacaca(self, val):
        self.estounacaca = val

    def goToPos(self, pos):

        tesX = int(pos[0])
        tesY = int(pos[2])

        if self.sentido in ['L', 'O']:
            if tesX > self.posX:
                self.goLeste(tesX)
            elif tesX < self.posX:
                self.goOeste(tesX)

            if tesY > self.posY:
                self.goNorte(tesY)
            elif tesY < self.posY:
                self.goSul(tesY)
            print("Cheguei na posicao: " + pos)

        elif self.sentido in ['N', 'S']:
            if tesY > self.posY:
                self.goNorte(tesY)
            elif tesY < self.posY:
                self.goSul(tesY)

            if tesX > self.posX:
                self.goLeste(tesX)
            elif tesX < self.posX:
                self.goOeste(tesX)
            print("Cheguei na posicao:" + pos)



    #retorna uma lista com as posicoes a serem percorridas
    #entre a posicao atual do robo (self.posX e self.posY) e a caca (self.goal)
    #exemplo: entre Robo em (0:0) virado para Norte ou sul
    #e Tesouro em (3:2) ele retorna uma lista assim:  ['0:1', '0:2', '1:2', '2:2', '3:2']
    #se fosse com o sentido em lLeste ou Oeste seria: ['1:0', '2:0', '3:0', '3:1', '3:2']
    def fazCaminho(self):

        #posicao tesouro em int
        tesX = int(self.goal[0])
        tesY = int(self.goal[2])

        #posicao robo em int
        robX = self.posX
        robY = self.posY

        #posicao robo e tesouro em String
        posRob = str(robX) + ':' + str(robY)
        posTes = str(tesX) + ':' + str(tesY)

        #lista de posicoes para ir na horizontal
        #lista de posicoes para ir na vertical
        lhorizontal = []
        lvertical   = []

        #sao o passo da funcao range, exemplos:
        #range(0, 5, 2) = [0, 2, 4]
        #range(0, 5, 1) = [0, 1, 2, 3, 4]
        aux = 666
        auy = 666

        #define se devemos ir somando ou subtraindo no passo do range
        #se o robo estiver a esquerda do tesouro:
        #   ele deve ir para a direita
        #se o robo estiver a direita do tesouro:
        #   ele deve ir para a esquerda
        if robX < tesX:
            aux = 1
        else:
            aux = -1
        #define se devemos ir somando ou subtraindo no passo do range
        #se o robo estiver para baixo do tesouro:
        #   ele deve ir para cima do tesouro
        #se o robo estiver para cima do tesouro:
        #   ele deve ir para baixo
        if robY < tesY:
            auy = 1
        else:
            auy = -1

        #se o robo nao esta em cima do tesouro:
        #   se o sentido atual for Norte ou Sul:
        #       deve primeiro se mexer/listar na vertical
        #   senao:
        #       deve primeiro se mexer/listar na horizontal
        if posRob != posTes:
            if self.sentido in ['N', 'S']:

                for i in range(robY+auy, tesY+auy, auy):
                    coordenada = str(robX) + ':' + str(i)
                    lvertical.append(coordenada)

                #soh existe variavel coordenada se ele faz o for aqui de cima
                #e ele soh entra nesse for se robo e tesouro nao estiverem na msm linha
                if robY != tesY:
                    robY = int(coordenada[2])

                for i in range(robX+aux, tesX+aux, aux):
                    coordenada = str(i) + ':' + str(robY)
                    lhorizontal.append(coordenada)

            else:
                for i in range(robX+aux, tesX+aux, aux):
                    coordenada = str(i) + ':' + str(robY)
                    lhorizontal.append(coordenada)

                #soh existe variavel coordenada se ele faz o for aqui de cima
                #e ele soh entra nesse for se robo e tesouro nao estiverem na msm coluna
                if robX != tesX:
                    robX = int(coordenada[0])

                for i in range(robY+auy, tesY+auy, auy):
                    coordenada = str(robX) + ':' + str(i)
                    lvertical.append(coordenada)

        if self.sentido in ['N', 'S']:
            return lvertical + lhorizontal
        else:
            return lhorizontal + lvertical

    # Exemplo: Robo esta em (0:0) e precisa ir pra (0:1), mas em (0:1) ha um adversario.
    # entao ele verifica qual a proxima posicao que deve ir depois de (0:1), vamos supor que seja (0:2).
    # entao ele faz um desvio pela lateral
    # Esse metodo nao movimenta o robo, apenas retorna uma lista das posicoes que devem ser tomadas para
    # contornar o adversario em forma de C
    def desviaEmC(self, proxProx):
        # Se existir uma posicao alem da proxima
        if proxProx != 0:
            # Se estiver na regiao e na mesma coluna
            if self.posX != 0 and self.posY < 5 and self.posX == int(proxProx[0]) and self.posY < int(proxProx[2]):
                pos1 = str(self.posX-1) + ':' + str(self.posY)
                pos2 = str(self.posX-1) + ':' + str(self.posY+1)
                pos3 = str(self.posX-1) + ':' + str(self.posY+2)
                return [pos1, pos2, pos3]

            # Se estiver na regiao e na mesma coluna
            elif self.posX != 0 and self.posY > 1 and self.posX == int(proxProx[0]) and self.posY > int(proxProx[2]):
                pos1 = str(self.posX-1) + ':' + str(self.posY)
                pos2 = str(self.posX-1) + ':' + str(self.posY-1)
                pos3 = str(self.posX-1) + ':' + str(self.posY-2)
                return [pos1, pos2, pos3]

            # Se estiver na regiao e na mesma linha
            elif self.posY != 6 and self.posX < 5 and self.posY == int(proxProx[2]) and self.posX < int(proxProx[0]):
                pos1 = str(self.posX) + ':' + str(self.posY+1)
                pos2 = str(self.posX+1) + ':' + str(self.posY+1)
                pos3 = str(self.posX+2) + ':' + str(self.posY+1)
                return [pos1, pos2, pos3]

            # Se estiver na regiao e na mesma linha
            elif self.posY != 6 and self.posX > 1 and self.posY == int(proxProx[2]) and self.posX > int(proxProx[0]):
                pos1 = str(self.posX) + ':' + str(self.posY+1)
                pos2 = str(self.posX-1) + ':' + str(self.posY+1)
                pos3 = str(self.posX-2) + ':' + str(self.posY+1)
                return [pos1, pos2, pos3]

            #tratando extremos daqui pra baixo
            elif self.posX == 0 and self.posY < 5 and int(proxProx[0]) == 0 and self.posY < int(proxProx[2]):
                pos1 = str(self.posX+1) + ':' + str(self.posY)
                pos2 = str(self.posX+1) + ':' + str(self.posY+1)
                pos3 = str(self.posX+1) + ':' + str(self.posY+2)
                return [pos1, pos2, pos3]

            elif self.posX == 0 and self.posY > 1 and int(proxProx[0]) == 0 and self.posY > int(proxProx[2]):
                pos1 = str(self.posX+1) + ':' + str(self.posY)
                pos2 = str(self.posX+1) + ':' + str(self.posY-1)
                pos3 = str(self.posX+1) + ':' + str(self.posY-2)
                return [pos1, pos2, pos3]

            elif self.posY == 6 and self.posX < 5 and int(proxProx[2]) == 6 and self.posX < int(proxProx[0]):
                pos1 = str(self.posX) + ':' + str(self.posY-1)
                pos2 = str(self.posX+1) + ':' + str(self.posY-1)
                pos3 = str(self.posX+2) + ':' + str(self.posY-1)
                return [pos1, pos2, pos3]

            elif self.posY == 6 and self.posX > 1 and int(proxProx[2]) == 6 and self.posX > int(proxProx[0]):
                pos1 = str(self.posX) + ':' + str(self.posY-1)
                pos2 = str(self.posX-1) + ':' + str(self.posY-1)
                pos3 = str(self.posX-2) + ':' + str(self.posY-1)
                return [pos1, pos2, pos3]

    #Deve se chamar essa funcao quando o robo esta na frente de uma posicao impedida por outro robo
    #Por exemplo: Se o robo esta em 1:3 e sentido norte e a funcao eh chamada, logo, presume-se que
    #a posicao que devemos desviar eh a posicao 1:4 pois seria a proxima que o robo iria.
    #Se o sentido fosse sul, a posicao bloqueada seria suposta como a 1:2
    #Se o sentido fosse oeste, a posicao bloqueada seria suposta como a 2:3
    #Se o sentido fosse leste, a posicao bloqueada seria suposta como a 0:3
    #A funcao retorna uma lista com as posicoes a serem percorridas ate a caca desviando da
    #posicao bloqueada
    def desviaEmL(self):

        tesX = int(self.goal[0])
        tesY = int(self.goal[2])

        robX = self.posX
        robY = self.posY

        posRob = str(robX) + ':' + str(robY)
        posTes = str(tesX) + ':' + str(tesY)

        lhorizontal = []
        lvertical   = []

        aux = 666
        auy = 666

        if robX < tesX:
            aux = 1
        else:
            aux = -1

        if robY < tesY:
            auy = 1
        else:
            auy = -1

        if posRob != posTes:
            if self.sentido in ['L', 'O']:

                for i in range(robY+auy, tesY+auy, auy):
                    coordenada = str(robX) + ':' + str(i)
                    lvertical.append(coordenada)

                if robY != tesY:
                    robY = int(coordenada[2])

                for i in range(robX+aux, tesX+aux, aux):
                    coordenada = str(i) + ':' + str(robY)
                    lhorizontal.append(coordenada)

            else:
                for i in range(robX+aux, tesX+aux, aux):
                    coordenada = str(i) + ':' + str(robY)
                    lhorizontal.append(coordenada)

                if robX != tesX:
                    robX = int(coordenada[0])

                for i in range(robY+auy, tesY+auy, auy):
                    coordenada = str(robX) + ':' + str(i)
                    lvertical.append(coordenada)

        if self.sentido in ['L', 'O']:
            return lvertical + lhorizontal
        else:
            return lhorizontal + lvertical

    def desvia(self, lcaminho, posOcupada):
        posOcupadaX = int(posOcupada[0])
        posOcupadaY = int(posOcupada[2])

        index = lcaminho.index(posOcupada)

        #tente pegar a proximo->proximo pos
        try:
            proxProx = lcaminho[index + 1] #isso da erro se n houver na lista
            proxProxX = int(proxProx[0])
            proxProxY = int(proxProx[2])
        except:
            proxProx = 0

        #se robo e 'proxima->proxima pos' estao na msm linha ou coluna, desvia em C
        if (self.posX == proxProxX or self.posY == proxProxY) and (proxProx != 0):
            ldesvio = self.desviaEmC(proxProx)
            formaDoDesvio = 'C'
        else:
            ldesvio = self.desviaEmL()
            formaDoDesvio = 'L'

        #versao mais facil
        for i in ldesvio:
            self.goToPos(i)

        return formaDoDesvio

        # #######################################################
        # for posDesv in ldesvio:
        #     if(not self.matar):
        #         if (self.treasure.getList()):
        #             print('Caminho de desvio: ')
        #             print(ldesvio)
        #             print('Indo para posicao de desvio: ')
        #             print(posDesv)
        #             self.parado = False
        #             ladversario = self.getladversario()
        #             if posDesv not in ladversario: #se a posicao que to indo n tem adversario
        #                 self.goToPos(posDesv)
        #             else:
        #                 self.desvia(lcaminho, posDesv)
        #             self.parado = True
        #             print("posicao do robo " + str(self.posX) + ":" + str(self.posY))
        #             print("posicao do goal " + str(self.goal))
        #             time.sleep(3)

        #             if(str(self.goal) == (str(self.posX) + ":" + str(self.posY))):
        #                 self.estounacaca = True
        #                 self.parado = True
        #                 time.sleep(3)
        #     else:
        #         self.setPausar()

        #     print("acabou o desvio")


    #NOVO'
    def moverAutomatico(self):

        formaDoDesvio = -1

        while(True):
            if(not self.matar):
                self.treasure.ordenaListaCaca(self.getPos())
                #lcaca = self.treasure.getList()
                print('Cacas a pegar: '  + self.treasure.getString())
                if (self.treasure.getList()):
                    self.goal = self.treasure.popTreasure()
                    print('Indo para caca: ' + str(self.goal))
                    print("CAMINHO")
                    print(self.fazCaminho())
                    lcaminho = self.fazCaminho()
                    for i in lcaminho:
                        if(not self.matar):
                            self.parado = False
                            print(i)
                            ladversario = self.getladversario()
                            if i not in ladversario: #se a posicao que to indo n tem adversario
                                self.goToPos(i)
                            else:
                                formaDoDesvio = self.desvia(lcaminho, i)
                            self.parado = True
                            print("posicao do robo " + (str(self.posX) + ":" + str(self.posY)))
                            print("posicao do goal " + str(self.goal))
                            time.sleep(3)
                        if formaDoDesvio == 'L':
                            print('Desvio feito em L. Indo para proximo tesouro')
                            break
                    if(str(self.goal) == (str(self.posX) + ":" + str(self.posY))):
                        self.estounacaca = True
                        self.parado = True
                        time.sleep(3)

                    #self.estounacaca = False
                    #self.parado = False

            else:
                self.setPausar()

            #print("acabou cacas")


    def goLeste(self, x):
        if self.sentido == 'N':
            self.moverDireita()
            while x > self.posX:
                self.moverFrente()
        elif self.sentido == 'L':
            while x > self.posX:
                self.moverFrente()
        elif self.sentido == 'S':
            self.moverEsquerda()
            while x > self.posX:
                self.moverFrente()
        elif self.sentido == 'O':
            self.moverRetornar()
            while x > self.posX:
                self.moverFrente()


    def goOeste(self, x):
        if self.sentido == 'N':
            self.moverEsquerda()
            while x < self.posX:
                self.moverFrente()
        elif self.sentido == 'L':
            self.moverRetornar()
            while x < self.posX:
                self.moverFrente()
        elif self.sentido == 'S':
            self.moverDireita()
            while x < self.posX:
                self.moverFrente()
        elif self.sentido == 'O':
            while x < self.posX:
                self.moverFrente()

    def goSul(self, y):
        if self.sentido == 'S':
            while y < self.posY:
                self.moverFrente()
        elif self.sentido == 'O':
            self.moverEsquerda()
            while y < self.posY:
                self.moverFrente()
        elif self.sentido == 'N':
            self.moverRetornar()
            while y < self.posY:
                self .moverFrente()
        elif self.sentido == 'L':
            self.moverDireita()
            while y < self.posY:
                self.moverFrente()

    def goNorte(self, y):
        if self.sentido == 'N':
            while y > self.posY:
                self.moverFrente()
        elif self.sentido == 'L':
            self.moverEsquerda()
            while y > self.posY:
                self.moverFrente()
        elif self.sentido == 'S':
            self.moverRetornar()
            while y > self.posY:
                self.moverFrente()
        elif self.sentido == 'O':
            self.moverDireita()
            while y > self.posY:
                self.moverFrente()


    def moverFrente(self):
        self.enviar = True
        self.parado = False
        print("movendo frente")
        #time.sleep(10)
        #self.parado = True
        self.cl.mode = 'COL-COLOR'
        if self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[
            self.cl.value()] == "blue":
            while self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[
                self.cl.value()] == "blue":
                self.r.run_forever(speed_sp=self.velocidade)
                self.l.run_forever(speed_sp=self.velocidade)
            else:
                self.setPausar()

        self.enviar = False

        if self.colors[self.cl.value()] == "unknown":
            while self.colors[self.cl.value()] != "black":
                self.r.run_forever(speed_sp=self.velocidade)

        while self.colors[self.cl.value()] != "green":
            while self.colors[self.cl.value()] == "black":
                self.r.run_forever(speed_sp=self.velocidade / 2)
                self.l.run_forever(speed_sp=self.velocidade)

            while self.colors[self.cl.value()] == "white":
                self.r.run_forever(speed_sp=self.velocidade)
                self.l.run_forever(speed_sp=self.velocidade / 2)

            if self.colors[self.cl.value()] == "yellow":
                self.l.run_forever(speed_sp=self.velocidade)
                self.r.run_forever(speed_sp=self.velocidade)
                time.sleep(0.1)
                break

            if self.colors[self.cl.value()] == "blue":
                self.l.run_forever(speed_sp=self.velocidade)
                self.r.run_forever(speed_sp=self.velocidade)
                time.sleep(0.1)
                break

        else:
            self.l.run_forever(speed_sp=self.velocidade)
            self.r.run_forever(speed_sp=self.velocidade)
            time.sleep(0.1)
        #self.enviar = False
        self.setPausar()

        if self.colors[self.cl.value()] == "green":
            #atualizando sentido
            if self.sentido == 'O':
                self.posX -= 1
            elif self.sentido == 'S':
                self.posY -= 1
            elif self.sentido == 'L':
                self.posX += 1
            elif self.sentido == 'N':
                self.posY += 1
        self.parado = True
        print("Posicao atual " + self.getPos())


    def moverEsquerda(self):
        self.parado = False
        print("Indo para esquerda")
        self.cl.mode = 'COL-COLOR'
        while self.colors[self.cl.value()] != "black":
            self.l.run_forever(speed_sp=0)
            self.r.run_forever(speed_sp=self.velocidade)

        else:
            self.setPausar()

        self.setPausar()

        #atualizando sentido
        if self.sentido == 'N':
            self.sentido = 'O'
        elif self.sentido == 'O':
            self.sentido = 'S'
        elif self.sentido == 'S':
            self.sentido = 'L'
        elif self.sentido == 'L':
            self.sentido = 'N'

        self.moverFrente()
        self.parado = True

    def moverDireita(self):
        self.parado = False
        print("Indo para direita")
        self.cl.mode = 'COL-COLOR'
        while self.colors[self.cl.value()] == "green":
           self.l.run_forever(speed_sp=self.velocidade)
           self.r.run_forever(speed_sp=self.velocidade)
        else:
            self.r.stop(stop_action="hold")

        #print(self.cl.value())

        while self.colors[self.cl.value()] == "black":
            self.l.run_forever(speed_sp=self.velocidade)
            self.r.run_forever(speed_sp=0)

       # print(self.cl.value())

        while self.colors[self.cl.value()] != "black":
            self.r.stop(stop_action="hold")
            self.l.run_forever(speed_sp=self.velocidade)
            #self.r.run_forever(speed_sp=40)
            #print(self.cl.value())

        #while
        #else:
           # self.r.run_forever(speed_sp=self.velocidade)

        #atualizando sentido
        if self.sentido == 'N':
            self.sentido = 'L'
        elif self.sentido == 'L':
            self.sentido = 'S'
        elif self.sentido == 'S':
            self.sentido = 'O'
        elif self.sentido == 'O':
            self.sentido = 'N'

        self.moverFrente()
        self.parado = True

    def moverRetornar(self):
        self.parado = False
        print("Retornando")
        self.cl.mode = 'COL-COLOR'
        while self.colors[self.cl.value()] == "green":
            self.l.run_forever(speed_sp=-self.velocidade)

        while self.colors[self.cl.value()] == "black":
            self.l.run_forever(speed_sp=-self.velocidade)

        while self.colors[self.cl.value()] != "black":
            self.l.run_forever(speed_sp=-self.velocidade)

        self.setPausar()

        #atualizando sentido
        if self.sentido == 'N':
            self.sentido = 'S'
        elif self.sentido == 'S':
            self.sentido = 'N'
        elif self.sentido == 'O':
            self.sentido = 'L'
        elif self.sentido == 'L':
            self.sentido = 'O'
        self.parado = True
        self.moverFrente()
