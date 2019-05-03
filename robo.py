from movimento import *
from dados import *
from coordenadas import *

class Robo:

    def __init__(self):
        self.mover = Movimento('outA', 'outD', 200)

    def setManual(self,  comando):
        if comando == "direita":
            self.mover.setDireita()
        elif comando == "esquerda":
            self.mover.setEsquerda()
        elif comando == "frente":
            self.mover.setFrente()
        elif comando == "parar":
            self.mover.setParar()
        elif comando == "retornar":
            self.mover.setRetornar()

