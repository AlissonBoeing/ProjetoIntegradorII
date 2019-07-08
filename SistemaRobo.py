from Communication import *
from Treasure import *
from threading import Thread
import time
from Robo import *
#-----------------------#
# Se conectar no SS -> envia mac, espera OK #
#------- Atributos do SR ---------#

isRobo = 0
confRobo = 0
strcacas = 0

#confs vindas do ss
mode = -1
lista_de_cacas = -1
posin = -1
sentido = -1
Partida = False



mac = "mac,02:16:53:45:b3:9a"
receive_fromSS = Communication("127.0.0.1", "50009", "fromSS")
send_toSS = Communication("127.0.0.1", "50008", "toSS")
receive_fromSS.start()
send_toSS.start()

print("Ligando Robo")

while(mode == -1 or lista_de_cacas == -1 or posin == -1 or sentido == -1):
    if (isRobo == 0):
        send_toSS.send(mac)
        time.sleep(1)
        if (receive_fromSS.getConfigList()):
            #print("AQQUI")
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
            if(msg == "manual"):
                mode = "manual"
                print ("modo " + str(mode))
            elif(msg == "automatico"):
                mode = "automatico"
                print("modo " + str(mode))
            elif(msg[0] == "@"):
                strcacas = msg[1:len(msg)] # msg[1:] tbm funciona
                print("Cacas " + strcacas)
                lista_de_cacas = strcacas
            elif(msg in "NnSsLlOo"):
                sentido = msg
                print ("sentido " + msg)
            elif(msg == "start"):
                Partida = True
            else:
                posin = msg
                print("Posicao inicial " + posin)

print("ROBO CONFIGURADO")




#instancia Robo
robot = Robo(200, mode, sentido, posin, strcacas)



j = 0
while(1):
    if (receive_fromSS.getConfigList()):  # recebeu alguma config
        msg = receive_fromSS.popConfigList()
        if(msg == "start"):
            Partida = True
        elif(msg == "stop"):
            j = 0;
            Partida = False

    if(mode == "manual" and Partida):
        #print("entrou no manual")
        while(1):
            while(receive_fromSS.getCommandList()):
                comando = receive_fromSS.popCommandList()
                robot.command(comando)
                if(comando in "vV"):
                    send_toSS.send("V")

    elif(mode == "automatico" and Partida): # automatico
        #print("entrou no automatico")
        if (j == 0):
            robot.start()
            j = j + 1
        else: #verificar sempre as listas de recebimento: attlist,configlist,commandlist


            if(robot.enviar):
                send_toSS.send("att," + str(robot.getPos()))
                time.sleep(1)


            if(receive_fromSS.getCommandList()):#recebeu algum comando
                msg = receive_fromSS.popCommandList()
                if(msg == "stop"):
                    Partida = False

            if(receive_fromSS.getConfigList()):
                msg = receive_fromSS.popConfigList()
                robot.setladversario(msg)

            if(receive_fromSS.getAttlist()): #recebeu atualizacao
                lista = receive_fromSS.popAttlist()
                robot.setLista(lista)

        i = 0
        while(robot.isNacaca()):
            robot.setMatar(True)
            print("ESTOU NA CACA")
            if (i < 2):
                send_toSS.send("c,v") # + robot.getPos())
                i = i + 1
            if(receive_fromSS.getConfigList()):
                resp = receive_fromSS.popConfigList()
                if (resp == "OK"):
                    print("Recebido OK")
                    robot.setMatar(False)
                    robot.setNacaca(False)
                elif(resp == "NOK"):
                    robot.setMatar(False)
                    robot.setNacaca(False)
            else:
                time.sleep(3)
                print("nao recebeu ok")
