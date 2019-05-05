from ev3dev.ev3 import *
from time import sleep

class Robo:
    def __init__(self, vel, cor):
        self.velocidade = vel
        self.l          = LargeMotor('outA')# esquerda
        self.r          = LargeMotor('outD')# direita
        self.cl         = ColorSensor()
        self.colors     = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
        self.id         = 'a0:f3:c1:0b:3c:48'
        self.cor        = cor
        self.sentido    = 'N'
        self.posX       = 0
        self.posY       = 0

    def getId(self):
        return self.id

    def getColor(self):
        return self.color

    def setVel(self, vel):
        if vel < 1000 & vel > 0:
            self.velocidade = vel
        else:
            print('Somente valores de 0 a 999')

    def setParar(self):
        self.r.stop(stop_action="hold")
        self.l.stop(stop_action="hold")

    def setSentido(self, sentido):
        if sentido in 'NSLO':
            self.sentido = sentido
        else:
            print('Somente permitidos N ou S ou L ou O para sentido')

    #posicao tesouro >>>> (tesX, tesY)
    #posicao robo    >>>> (posX, posY)
    def moverAutomatico(self, tesX, tesY):
        if tesX > self.posX:
            self.goLeste(tesX)
        else:
            self.goOeste(tesX)

        if tesY > self.posY:
            self.goNorte(tesY)
        else:
            self.goSul(tesY)

        print('Chegou na caça!')
        print('Pos atual robo:')
        print('PosX: ' + self.posX )
        print('PosY: ' + self.posY )

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
                self.moverFrente
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
                self .moverFrente
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
        self.cl.mode = 'COL-COLOR'
        if self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[
            self.cl.value()] == "blue":
            while self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[
                self.cl.value()] == "blue":
                self.r.run_forever(speed_sp=self.velocidade)
                self.l.run_forever(speed_sp=self.velocidade)
            else:
                self.setParar()
                ## Colocar o resto do codico no else

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
                sleep(0.1)
                break

            if self.colors[self.cl.value()] == "blue":
                self.l.run_forever(speed_sp=self.velocidade)
                self.r.run_forever(speed_sp=self.velocidade)
                sleep(0.1)
                break

        else:
            self.l.run_forever(speed_sp=self.velocidade)
            self.r.run_forever(speed_sp=self.velocidade)
            sleep(0.1)

        self.setParar()

        #atualizando sentido
        if self.sentido == 'O':
            self.posX -= 1
        elif self.sentido == 'S':
            self.posY -= 1
        elif self.sentido == 'L':
            self.posX += 1
        elif self.sentido == 'N':
            self.posY += 1

    def moverEsquerda(self):
        self.cl.mode = 'COL-COLOR'
        while self.colors[self.cl.value()] != "black":
            self.l.run_forever(speed_sp=-self.velocidade/2)
            self.r.run_forever(speed_sp=self.velocidade)

        else:
            #sleep(0.1)
            self.setParar()

        self.setParar()

        self.moverFrente()

        #atualizando sentido
        if self.sentido == 'N':
            self.sentido = 'O'
            self.posX -= 1
        elif self.sentido == 'O':
            self.sentido = 'S'
            self.posY -= 1
        elif self.sentido == 'S':
            self.sentido = 'L'
            self.posX += 1
        elif self.sentido == 'L':
            self.sentido = 'N'
            self.posY += 1

    def moverDireita(self):
        self.cl.mode = 'COL-COLOR'
        while self.colors[self.cl.value()] == "green":
            self.l.run_forever(speed_sp=self.velocidade)
            self.r.run_forever(speed_sp=self.velocidade/2)
        else:
            self.r.stop(stop_action="hold")

        while self.colors[self.cl.value()] == "black":
            self.l.run_forever(speed_sp=self.velocidade)

        while self.colors[self.cl.value()] != "black":
            self.l.run_forever(speed_sp=self.velocidade)

        else:
            self.l.run_forever(speed_sp=self.velocidade)

        #self.setParar()

        self.moverFrente()

        #atualizando sentido
        if self.sentido == 'N':
            self.sentido = 'L'
            self.posX += 1
        elif self.sentido == 'L':
            self.sentido = 'S'
            self.posY -= 1
        elif self.sentido == 'S':
            self.sentido = 'O'
            self.posX -= 1
        elif self.sentido == 'O':
            self.sentido = 'N'
            self.posY += 1

    def moverRetornar(self):
        self.cl.mode = 'COL-COLOR'
        while self.colors[self.cl.value()] == "green":
            self.l.run_forever(speed_sp=-self.velocidade)
           #self.r.run_forever(speed_sp=-self.velocidade/2)

        #sleep(0.1)
        #self.setParar()

        while self.colors[self.cl.value()] == "black":
            #			self.r.run_forever(speed_sp=self.velocidade)
            self.l.run_forever(speed_sp=-self.velocidade)

        while self.colors[self.cl.value()] != "black":
            #self.setParar()
            self.l.run_forever(speed_sp=-self.velocidade)

        self.setParar()
        self.moverFrente()

        #atualizando sentido
        if self.sentido == 'N':
            self.sentido = 'S'
            self.posY -= 1
        elif self.sentido == 'S':
            self.sentido = 'N'
            self.posY += 1
        elif self.sentido == 'O':
            self.sentido = 'L'
            self.posX += 1
        elif self.sentido == 'L':
            self.sentido = 'O'
            self.posX -= 1