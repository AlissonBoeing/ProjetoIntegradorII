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

receive_fromSS = Communication("192.168.43.27", "50009", "fromSS")

send_toSS = Communication("192.168.43.27", "50008", "toSS")

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
                strcacas = msg[1:len(msg)] # msg[1:] tbm funciona
                print("Cacas " + strcacas)
            else:
                posin = msg
                print("Posicao inicial " + posin)

print("ROBO CONFIGURADO")

#instancia Robo
robot = Robo(100, cor, modo, "N", posin, strcacas)

j = 0
while(1):
    if(modo == "manual"):
        while(1):
            while(receive_fromSS.getCommandList()):
                comando = receive_fromSS.popCommandList()
                robot.command(comando)
                if(comando in "vV"):
                    send_toSS.send("V")

    else: # automatico
        if (j == 0):
            robot.start()
            j = j + 1
        else: #verificar sempre as listas de recebimento: attlist,configlist,commandlist

            if(receive_fromSS.getCommandList()): #recebeu algum comando
                pass

            if(receive_fromSS.getConfigList()): #recebeu alguma config
                pass

            if(receive_fromSS.getAttlist()): #recebeu atualizacao
                lista = receive_fromSS.popAttlist()
                robot.setLista("cacas," + lista)
            #se for diferente robot.setLcacas(getlistadecacas)

        #if(robot.isParado()):
            #send_toSS.send("att," + robot.getPos())
            #time.sleep(1)

        #if(not str(robot.getGoal()) in robot.getTreasure().getString() and robot.isParado()):
         #       robot.setPausar() #pausa o robo
          #      robot.join()#pausa a thread
           #     robot.start()     #reinicia a thread com a lista atualizada
                #robot.moverAutomatico()
        print ("to aqui")
        while(robot.isNacaca()):
            robot.setMatar(True)
            #robot.setPausar()
            print("ESTOU NA CACA")
            #robot.join()
            send_toSS.send("c,v") # + robot.getPos())
            if(receive_fromSS.getConfigList()):
                resp = receive_fromSS.popConfigList()
                if (resp == "OK"):
                    print("Recebido OK")
                    robot.setMatar(False)
                    robot.setNacaca(False)
                    teste = robot.getTreasure()
                    teste.removeCaca(robot.getGoal())
                    robot.setLista(teste.getString())
                    print(robot.getTreasure().getString())
                    #robot.getTreasure().removeCaca(robot.getGoal())
                    #robot.start()
            else:
                time.sleep(3)
                send_toSS.send("c,v")
                print("nao recebeu ok")

                   #pass #tirar da lista de caças

        #print("nao existe caca nessa posicao")
                 #   pass #Nao existe caça na posicao que esta


       # pass#robot.start()




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

