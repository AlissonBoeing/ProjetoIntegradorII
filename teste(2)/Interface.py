from Communication import *
from Treasure import *
import threading
import time
from os import system, name


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
    system('clear')
    while(1):
        atualizarmapa(c)
        if (mode == "manual"):
            print("Robô Manual - Escolha uma das opções abaixo:")
            command = input ("W - Mover para frente;\n"
                                "A - Mover para esquerda;\n"
                                "S - Mover para trás;\n"
                                "D - Mover para esquerda;\n"
                                "V - Validar caça;\n")
        if(command):
            sendSR.send(command)
            time.sleep(2)
      #  else:
           # pass

#teste = Communication('127.0.0.1', 7000, "teste");

#teste.connect();
#------------------------- Dados do SA ------------------------ #
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

send_toSR = Communication('127.0.0.1', "50009",'toSR')

receive_fromSR = Communication("127.0.0.1", "50008", "fromSR")

#receivefromSS = Communication('127.0.0.1', "50009", "fromSS")
interface_t = threading.Thread(target=interface, args=(modo, send_toSR))
#receive_t = threading.Thread(target=recSS.receiveMessage())
#send_t = threading.Thread(target=sendSR.sendMessage)
#atualizarmapa_t = threading.Thread(target=atualizarmapa())

send_toSR.start()

receive_fromSR.start()
#ip teles (SR) = 191.36.10.250, porta 7000

modo = "modo:manual"
#numcacas = "6"
#numcomp = "2"
cor = "cor:azul"

local = "cacas:1,1;2,3;5,2;6,6;4,3;2,1"

send_toSR.send(modo)
send_toSR.send(cor)
send_toSR.send()

#------------------------
#interface_t.start()
#print("asd)
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








