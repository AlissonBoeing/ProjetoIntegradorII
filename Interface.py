from Communication import *
from Treasure import *
import threading
import time
from Treasure import *
from os import system, name

#------- atributos do SS --------- #
isRobo = 0



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
        print(local)
        if (mode == "modo,manual"):
            print("Robô Manual - Escolha uma das opções abaixo:")
            entrada = input("W - Mover para frente;\n"
                                "A - Mover para esquerda;\n"
                                "S - Mover para trás;\n"
                                "D - Mover para esquerda;\n"
                                "V - Validar caça;\n")
            if(entrada):
                if(entrada in "vV"):
                    send_toSA.send("c," + entrada)
                    if(atual in a):
                        print("CACA PEGA OK")
                        a.removeCaca(atual)
                        time.sleep(2)
                else:
                    send_toSR.send("c," + entrada)
        else:
            pass
            #atualizarmapa(c)



#teste = Communication('127.0.0.1', 7000, "teste");

#teste.connect();
#------------------------- Dados do SA ------------------------ #

modo = "modo,manual"
cor = "cor,azul"
local = "cacas,2:0;4:3;4:5"
posin = "posin,0:6"
atual = "0:6"
local2 = "2:0;4:3;4:5"
### teste lista de caças ###

a = Treasure(local2)
#------------------------##

send_toSR = Communication("192.168.43.248", "50009",'toSR')

receive_fromSR = Communication("192.168.43.248", "50008", "fromSR")

send_toSA = Communication("127.0.0.1", "50006",'toSA')

receive_fromSA = Communication("127.0.0.1", "50007", "fromSA")

#receivefromSS = Communication('127.0.0.1', "50009", "fromSS")
interface_t = threading.Thread(target=interface, args=(modo, send_toSR))
#receive_t = threading.Thread(target=recSS.receiveMessage())
#send_t = threading.Thread(target=sendSR.sendMessage)
#atualizarmapa_t = threading.Thread(target=atualizarmapa())

send_toSA.start()

receive_fromSA.start()

send_toSR.start()

receive_fromSR.start()

#ip teles (SR) = 191.36.10.250, porta 7000





#send_toSR.send(modo)
#send_toSR.send(cor)
#send_toSR.send(local)

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


print("Esperando endereço MAC do robô")


while (1):
    if(isRobo == 0):
        if(receive_fromSR.getConfigList()):
            #if (len(receive_fromSR.getConfigList().pop()) == 17):
            #receive_fromSR.popConfigList()
            if (len(receive_fromSR.popConfigList()) == 17):
                print("Endereço MAC recebido")
                isRobo = 1
                send_toSR.send("ack,OK")
                time.sleep(2)
                send_toSR.send(modo)
                send_toSR.send(cor)
                send_toSR.send(local)
                send_toSR.send(posin)
                if(modo == "modo,manual"):
                    interface_t.start()
    else: #apos configurar e startar o robo, verificar listas de recebimento

        if (receive_fromSR.getAttlist()):  # recebeu alguma atualizacao
            atual = receive_fromSR.popAttlist()

        if (receive_fromSR.getConfigList()):  # recebeu alguma config
            pass

        if(receive_fromSR.getCommandList()):
            msg = receive_fromSR.popCommandList()
            if (msg in "vV"):
                resp = input("Existe caca na posicao ")
                send_toSR.send("ack," + resp)

        if(receive_fromSA.getAttlist()):
            listatt = receive_fromSA.popAttlist()
            send_toSR.send("cacass," + listatt)
            send_toSR.send("ack,OK")
            send_toSR.send(local)
            time.sleep(5)

        #break
        #pass
        #print(send_toSR.getSendList())
        #time.sleep(5)
       #pass
       #print(len(receive_fromSR.getConfigList()))







