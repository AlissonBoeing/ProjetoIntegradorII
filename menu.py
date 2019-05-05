#!/usr/bin/env python3
from Robo import *
#from SensorLum import *

cor     = input("Cor: ")
comando = input("dir: ")
vel     = input("Velocidade: ")

robot = Robo(vel, cor)

print('Comandos: ')
print('w-a-s-d -> frente-esquerda-retorna-direita')
print('v - altera velocidade')
print('c - altera cor')
print('auto - altera para modo automático')

while (comando != "exit"):

	if comando == 'w':
		robot.moverFrente()

	elif comando == 'a':
		robot.moverEsquerda()

	elif comando == 's':
		robot.moverRetornar()

	elif comando == 'd':
		robot.moverDireita()

	elif comando == 'v':
		vel = input("Velocidade: ")
		robot.setVel(vel)

	elif comando == 'c':
		cor = input("Cor: ")

	elif comando == 'auto':
		posX = input('PosX tesouro: ')
		posY = input('PosY tesouro: ')
		robot.moverAutomatico(posX, posY)

	direcao = input("dir: ")