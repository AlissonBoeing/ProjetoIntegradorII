#!/usr/bin/env python3
from Robo import *
#from SensorLum import *

cor = input("Cor: ")
vel = input("Velocidade: ")
direcao = input("dir: ")

robot = Robo(vel, cor)

while (direcao != "exit"):

	if direcao == 'w':
		robot.moverFrente()

	elif direcao == 'a':
		robot.moverEsquerda()

	elif direcao == 's':
		robot.moverRetornar()

	elif direcao == 'd':
		robot.moverDireita()

	elif direcao == 'v':
		vel = input("Velocidade: ")
		robot.setVel(vel)

	elif direcao == 'c':
		cor = input("Cor: ")

	direcao = input("dir: ")