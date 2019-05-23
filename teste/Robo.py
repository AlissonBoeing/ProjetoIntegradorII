#from ev3dev.ev3 import *
from time import sleep

import threading

class Robo(threading.Thread):

    def __init__(self, vel, cor, modo,  sentido, posin, lcaca):
        threading.Thread.__init__(self)
        self.velocidade = vel
       # self.l          = LargeMotor('outA')# esquerda
       # self.r          = LargeMotor('outD')# direita
       # self.cl         = ColorSensor()
        self.colors     = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
        self.id         = 'a0:f3:c1:0b:3c:48'
        self.cor        = cor
        self.sentido    = sentido
        posX = posin[0]
        posY = posin[2]
        self.modo = modo
        self.posX       = posX
        self.posY       = posY
        self.lcaca      = lcaca
        self.parado = True
        self.estounacaca = False

    def run(self):
        while(1):
            i
        pass

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

    # #deve-se finalizar esta def
    def obterCaca(self):
        self.estounacaca = True
        pass #        coord = self.posX, self.posY
    #     if coord in self.lcaca:
    #         pass
    #         #Aqui o robo deve enviar uma msg para SS informando que encontrou uma caça
    #         #aqui o robo deve usar uma função desta classe para enviar a msg
    #         #esta funcao de enviar msg ainda n foi criada
    #
    # def atualizarMapa(self):
    #     pass#     #enviar coord do robo
    #     #verificar se a caça que esta sendo procurada ainda n foi caçada
    #     pass
    #
    # def getId(self):
    #     return self.id
    #
    # def getColor(self):
    #     return self.color
    #
    # def setVel(self, vel):
    #     if vel < 1000 and vel > 0:
    #         self.velocidade = vel
    #     else:
    #         print('Somente valores de 0 a 999')
    #
    # def setPausar(self):
    #     self.r.stop(stop_action="hold")
    #     self.l.stop(stop_action="hold")
    #
    # def setSentido(self, sentido):
    #     if sentido in 'NSLO':
    #         self.sentido = sentido
    #     else:
    #         print('Somente permitidos N ou S ou L ou O para sentido')
    #
    # def moverAutomatico(self):
    #
    #     for index in self.lcaca:
    #         tesX = index[0]
    #         tesY = index[1]
    #
    #         if tesX > self.posX:
    #             self.goLeste(tesX)
    #         elif tesX < self.posX:
    #             self.goOeste(tesX)
    #
    #         if tesY > self.posY:
    #             self.goNorte(tesY)
    #         elif tesY < self.posY:
    #             self.goSul(tesY)
    #
    # def goLeste(self, x):
    #     if self.sentido == 'N':
    #         self.moverDireita()
    #         while x > self.posX:
    #             self.moverFrente()
    #     elif self.sentido == 'L':
    #         while x > self.posX:
    #             self.moverFrente()
    #     elif self.sentido == 'S':
    #         self.moverEsquerda()
    #         while x > self.posX:
    #             self.moverFrente()
    #     elif self.sentido == 'O':
    #         self.moverRetornar()
    #         while x > self.posX:
    #             self.moverFrente()
    #
    #
    # def goOeste(self, x):
    #     if self.sentido == 'N':
    #         self.moverEsquerda()
    #         while x < self.posX:
    #             self.moverFrente()
    #     elif self.sentido == 'L':
    #         self.moverRetornar()
    #         while x < self.posX:
    #             self.moverFrente()
    #     elif self.sentido == 'S':
    #         self.moverDireita()
    #         while x < self.posX:
    #             self.moverFrente()
    #     elif self.sentido == 'O':
    #         while x < self.posX:
    #             self.moverFrente()
    #
    # def goSul(self, y):
    #     if self.sentido == 'S':
    #         while y < self.posY:
    #             self.moverFrente()
    #     elif self.sentido == 'O':
    #         self.moverEsquerda()
    #         while y < self.posY:
    #             self.moverFrente()
    #     elif self.sentido == 'N':
    #         self.moverRetornar()
    #         while y < self.posY:
    #             self .moverFrente()
    #     elif self.sentido == 'L':
    #         self.moverDireita()
    #         while y < self.posY:
    #             self.moverFrente()
    #
    # def goNorte(self, y):
    #     if self.sentido == 'N':
    #         while y > self.posY:
    #             self.moverFrente()
    #     elif self.sentido == 'L':
    #         self.moverEsquerda()
    #         while y > self.posY:
    #             self.moverFrente()
    #     elif self.sentido == 'S':
    #         self.moverRetornar()
    #         while y > self.posY:
    #             self.moverFrente()
    #     elif self.sentido == 'O':
    #         self.moverDireita()
    #         while y > self.posY:
    #             self.moverFrente()


    def moverFrente(self):
        print("Indo para frente")
        # self.cl.mode = 'COL-COLOR'
        # if self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[
        #     self.cl.value()] == "blue":
        #     while self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[
        #         self.cl.value()] == "blue":
        #         self.r.run_forever(speed_sp=self.velocidade)
        #         self.l.run_forever(speed_sp=self.velocidade)
        #     else:
        #         self.setPausar()
        #
        # if self.colors[self.cl.value()] == "unknown":
        #     while self.colors[self.cl.value()] != "black":
        #         self.r.run_forever(speed_sp=self.velocidade)
        #
        # while self.colors[self.cl.value()] != "green":
        #     while self.colors[self.cl.value()] == "black":
        #         self.r.run_forever(speed_sp=self.velocidade / 2)
        #         self.l.run_forever(speed_sp=self.velocidade)
        #
        #     while self.colors[self.cl.value()] == "white":
        #         self.r.run_forever(speed_sp=self.velocidade)
        #         self.l.run_forever(speed_sp=self.velocidade / 2)
        #
        #     if self.colors[self.cl.value()] == "yellow":
        #         self.l.run_forever(speed_sp=self.velocidade)
        #         self.r.run_forever(speed_sp=self.velocidade)
        #         sleep(0.1)
        #         break
        #
        #     if self.colors[self.cl.value()] == "blue":
        #         self.l.run_forever(speed_sp=self.velocidade)
        #         self.r.run_forever(speed_sp=self.velocidade)
        #         sleep(0.1)
        #         break
        #
        # else:
        #     self.l.run_forever(speed_sp=self.velocidade)
        #     self.r.run_forever(speed_sp=self.velocidade)
        #     sleep(0.1)
        #
        # self.setPausar()

        # if self.colors[self.cl.value()] == "green":
        #     #atualizando sentido
        #     if self.sentido == 'O':
        #         self.posX -= 1
        #     elif self.sentido == 'S':
        #         self.posY -= 1
        #     elif self.sentido == 'L':
        #         self.posX += 1
        #     elif self.sentido == 'N':
        #         self.posY += 1

    def moverEsquerda(self):
        print("Indo para esquerda")
        # self.cl.mode = 'COL-COLOR'
        # while self.colors[self.cl.value()] != "black":
        #     self.l.run_forever(speed_sp=-self.velocidade/2)
        #     self.r.run_forever(speed_sp=self.velocidade)
        #
        # else:
        #     self.setPausar()
        #
        # self.setPausar()
        #
        # #atualizando sentido
        # if self.sentido == 'N':
        #     self.sentido = 'O'
        # elif self.sentido == 'O':
        #     self.sentido = 'S'
        # elif self.sentido == 'S':
        #     self.sentido = 'L'
        # elif self.sentido == 'L':
        #     self.sentido = 'N'
        #
        # self.moverFrente()

    def moverDireita(self):
        print("Indo para direita")
        # self.cl.mode = 'COL-COLOR'
        # while self.colors[self.cl.value()] == "green":
        #     self.l.run_forever(speed_sp=self.velocidade)
        #     self.r.run_forever(speed_sp=self.velocidade/2)
        # else:
        #     self.r.stop(stop_action="hold")
        #
        # while self.colors[self.cl.value()] == "black":
        #     self.l.run_forever(speed_sp=self.velocidade)
        #
        # while self.colors[self.cl.value()] != "black":
        #     self.l.run_forever(speed_sp=self.velocidade)
        #
        # else:
        #     self.l.run_forever(speed_sp=self.velocidade)
        #
        # #atualizando sentido
        # if self.sentido == 'N':
        #     self.sentido = 'L'
        # elif self.sentido == 'L':
        #     self.sentido = 'S'
        # elif self.sentido == 'S':
        #     self.sentido = 'O'
        # elif self.sentido == 'O':
        #     self.sentido = 'N'
        #
        # self.moverFrente()



    def moverRetornar(self):
         print("Retornando")
        # self.cl.mode = 'COL-COLOR'
        # while self.colors[self.cl.value()] == "green":
        #     self.l.run_forever(speed_sp=-self.velocidade)
        #
        # while self.colors[self.cl.value()] == "black":
        #     self.l.run_forever(speed_sp=-self.velocidade)
        #
        # while self.colors[self.cl.value()] != "black":
        #     self.l.run_forever(speed_sp=-self.velocidade)
        #
        # self.setPausar()
        #
        # #atualizando sentido
        # if self.sentido == 'N':
        #     self.sentido = 'S'
        # elif self.sentido == 'S':
        #     self.sentido = 'N'
        # elif self.sentido == 'O':
        #     self.sentido = 'L'
        # elif self.sentido == 'L':
        #     self.sentido = 'O'

#self.moverFrente()