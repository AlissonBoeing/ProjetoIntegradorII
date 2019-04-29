#!/usr/bin/env python3
from Robo import *
from SensorLum import *


direcao = input("dir")
robot = Robo(100, 'Azul')


while (direcao != "exit"):

	if direcao == 'w':
		robot.moverFrente()

	elif direcao == 'a':
		print("nao implementado ainda")

	elif direcao == 's':
		print("nao implementado ainda")

	elif direcao == 'd':
		print("nao implementado ainda")


	direcao = input("direcao")
