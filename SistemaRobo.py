from Communication import *
from Treasure import *
from threading import Thread
import time
from Robo import *
#-----------------------#
# Se conectar no SS -> envia mac, espera OK #
#

#------- Atributos do SR ---------#

isRobo = 0
cor = 0
modo = 0
confRobo = 0
strcacas = 0
posin = 0


mac = "mac,02:16:53:45:b3:9a"

receive_fromSS = Communication("192.168.43.130", "50009", "fromSS")

send_toSS = Communication("192.168.43.130", "50008", "toSS")

#send_toSS = Communication("127.0.0.1", "50010", "toSS")

#send_toSS.start()

receive_fromSS.start()

send_toSS.start()

print("Ligando Robo")

while(confRobo != 2):
    if (isRobo == 0):
        #print("Enviando MAC")
        send_toSS.send(mac)
        time.sleep(1)
        if (receive_fromSS.getConfigList()):
            print("AQQUI")
            if (receive_fromSS.popConfigList() == "OK"):
                print("Robo Cadastrado no SS")
                isRobo = 1
            else:
                print("Enviando MAC")
                send_toSS.send(mac)
                time.sleep(4)
    else:

        while(receive_fromSS.getConfigList()):
            msg = receive_fromSS.popConfigList()
            if(msg == "azul" or msg == "verde"):
                cor = msg
                print("cor "+ cor)
                confRobo = confRobo + 1
            elif(msg == "manual" or msg == "automatico"):
                modo = msg
                print ("modo " + modo)
                confRobo = confRobo + 1
            elif(msg[0] == "@"):
                strcacas = msg[1:len(msg)]
                print("Cacas " + strcacas)
            else:
                posin = msg
                print("Posicao inicial " + posin)

print("ROBO CONFIGURADO")

#instancia Robo
robot = Robo(100, cor, modo, "N", posin, strcacas)

j = 0
#robot.start()
#lista temporaria
while(1):
    #if parado
    #send_toSS(posicao)

    #if estou em uma caca
    #send_toSS(posicao) set_Estounacaa = false

    if(modo == "manual"):
        #robot.start()
        while(receive_fromSS.getCommandList()):
            comando = receive_fromSS.popCommandList()
            robot.command(comando)
    else: # automatico
        if (j == 0):
            robot.moverAutomatico()
            j = j + 1
        else:
            if(receive_fromSS.getAttlist()):
                lista = receive_fromSS.popAttlist()
                robot.setLista(lista)
            #se for diferente robot.setLcacas(getlistadecacas)

        if(robot.isParado()):
            send_toSS.send(robot.getPos())
            time.sleep(1)

        if(robot.isNacaca()):
            send_toSS.send("v" + robot.getPos())
            while(not receive_fromSS.getConfigList()):
                time.sleep(1)
            else:
                resp = receive_fromSS.popConfigList()
                if(resp == "OK"):
                    pass #tirar da lista de caças
                else:
                    pass #Nao existe caça na posicao que esta


        pass#robot.start()




#def __init__(self, vel, cor, sentido, posX, posY, lcaca):


        #print(send_toSS.getSendList())
        #time.sleep(5)
        #print("pronto para comandos")# print("Robo iniciado no modo" + modo + "com a cor" + cor)
       # if(receive_fromSS.getCommandList()):




#send_toSS.send(mac)


#while(1):
    #print("teste")
    #send_toSS.send(mac)
#    time.sleep(1)

