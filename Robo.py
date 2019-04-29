from ev3dev.ev3 import *
from time import sleep

class Robo:

	def __init__(self, vel, cor):
		self.vel    = vel
		self.m1     = LargeMotor('outA')# esquerda
		self.m2     = LargeMotor('outD')# direita		
		self.color  = ColorSensor()
		self.colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
		self.id     = 'a0:f3:c1:0b:3c:48'
		self.cor    = cor

	def setVel(self, vel)
		self.vel = vel



	def moverFrente(self)
	        self.cl.mode = 'COL-COLOR'
        	if self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[self.cl.value()] == "blue":
        	    while self.colors[self.cl.value()] == "green" or self.colors[self.cl.value()] == "yellow" or self.colors[self.cl.value()] == "blue":
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


	def moverEsquerda(self)
		pass

	def moverDireita(self)
		pass

	def moverRetornar(self)
		pass

	def setParar(self)
		pass

	def getId(self)
		return self.id

	def getColor(self)
		return self.color






