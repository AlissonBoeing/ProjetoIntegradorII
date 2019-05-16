from Communication import *
from Treasure import *
import threading
import time

def atualizarmapa(lista):
    A = list(lista)

    for x in range(0, 8):
        for y in range (0, 8):
            A = list(lista)
            if(y==0):
                print(x, end = " ")
            elif(x==0):
                print ("     " + str(y), end = " ")
            else:
                while(A):
                    c = A.pop()
                    if(c.getPosx() == x and c.getPosy() == y):
                        print("    " + c.id, end = " ")

                print("    -", end=" ")
        print("\n")


def interface(mode, sendSR):
    while(1):
        atualizarmapa(c)
        if (mode == "manual"):
            print("Robô Manual - Escolha uma das opções abaixo:")
            command = input("W - Mover para frente;\n"
                                 "A - Mover para esquerda;\n"
                                 "S - Mover para trás;\n"
                                 "D - Mover para esquerda;\n"
                                 "V - Validar caça;\n")
            sendSR.send(command)
            
#teste = Communication('127.0.0.1', 7000, "teste");

#teste.connect();
#------------------------- Dados do SA ------------------------ #

#ip teles (SR) = 191.36.10.250, porta 7000
modo = "manual"
numcacas = 6
numcomp = 2
cor = 'azul'
local = '1,1;2,3;5,2;6,6;4,3;2,1'
#------------------------



### teste lista de caças ###
c = list()
c.append(Treasure(1,1,'c1'))
c.append(Treasure(2,2,'c2'))
c.append(Treasure(3,3,'c3'))
c.append(Treasure(3,4,'c4'))
c.append(Treasure(5,5,'c5'))
c.append(Treasure(6,6,'c6'))
c.append(Treasure(7,7,'c7'))
c.append(Treasure(1,2, 'c8'))
#------------------------###

sendSR = Communication('192.168.43.223', "7000",'toSR')

recSS = Communication('192.168.43.223', "7001", "fromSS")

interface_t = threading.Thread(target=interface(modo, sendSR))

receive_t = threading.Thread(target=recSS.receiveMessage())

send_t = threading.Thread(target=sendSR.sendMessage())

#atualizarmapa_t = threading.Thread(target=atualizarmapa())

interface_t.start()

#while(1):
   # print("Iniciou")


#inicia o jogo enviando configs pro robo



 #   receiveSR = Communication('127.0.0.1', 7000, 'fromSS')




#receiveSR.receiveMessage()
#sendSR.send(10)

#receiveSR.start()

#print(i)






    #inicia robo e menu no manual
    #inicia robo e menu no automatico

#mantém menu e lista de caças na tela


#inicia thread de atualização das caças (recebe do SA e envia pro SR)








