from Communication import *
from Treasure import *
import threading
import time
from Treasure import *
from os import system, name
from Comunica_SA import *
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

def traduzirListacacas(lista):
    # chega do SA[(0, 1), (1, 2), (2, 3), (3, 4), (1, 1)]
    # deve sair 1:1;2:3;5:2;6:6;4:3;2:1"

    strlista = ""
    for i in lista:
        strlista = strlista + (str(i[0]) + ":" + str(i[1]) + ";")
    return strlista[0:-1]

# atributos da partida

Partida = False
mode = -1
posAtual = -1
listacacasSS = -1
posin = "0:0"



# comunicacoes #
send_toSR = Communication("192.168.1.127", "50009",'toSR')
receive_fromSR = Communication("192.168.1.127", "50008", "fromSR")
send_toSR.start()
receive_fromSR.start()
com_SA = Comunica_SA(8888, '127.0.0.1')
com_SA.run()
com_SA.login("AlissonTeles", (posin[0],posin[2]))

#-------- Recebe conexao do SR -> loga no SA -> recebe as configurações e Inicia quando receber start ----- #


#atributos da partida




while (1):

    if(isRobo == 0):
        if(receive_fromSR.getConfigList()):
            if (len(receive_fromSR.popConfigList()) == 17):
                print("Endereço MAC recebido")
                isRobo = 1
                send_toSR.send("ack,OK")
                time.sleep(2)
                send_toSR.send("posin," + posin)
                send_toSR.send("comm,N")
                #--- Robo cadastrado
    else:

        if(Partida):
            #print("PARTIDA INICIADA")


            if(mode == "manual"):
                while (1):
                    if (com_SA.get_flags_list()):
                        msg = com_SA.pop_flags_list()
                        msg = traduzirListacacas(msg)
                        listacacasSS = msg

                        send_toSR.send("cacas," + msg)
                    if (com_SA.get_commands_list()):
                        msg = com_SA.pop_commands_list()
                        if(msg == 200):
                            send_toSR.send("ack,OK")
                        if(msg == 400):
                            send_toSR.send("ack,NOK")

                        if (msg == "start"):
                            # mensagem do SA para comecar a partida, enviar para o SR
                            Partida = True
                            send_toSR.send("comm,start")
                        elif (msg == "stop"):
                            send_toSR.send("comm,stop")
                            # apenas com a partida iniciada#
                            Partida = False
                            break

                    print("Robô Manual - Escolha uma das opções abaixo:")
                    print("Lista de cacas disponiveis " + listacacasSS)
                    entrada = input("W - Mover para frente;\n"
                                    "A - Mover para esquerda;\n"
                                    "S - Mover para trás;\n"
                                    "D - Mover para esquerda;\n"
                                    "V - Validar caça;\n")

                    if (com_SA.get_commands_list()):
                        msg = com_SA.pop_commands_list()
                        if(msg == 200):
                            send_toSR.send("ack,OK")
                        if(msg == 400):
                            send_toSR.send("ack,NOK")

                        if (msg == "start"):
                            # mensagem do SA para comecar a partida, enviar para o SR
                            Partida = True
                            send_toSR.send("comm,start")
                        elif (msg == "stop"):
                            send_toSR.send("comm,stop")
                            # apenas com a partida iniciada#
                            Partida = False
                            break


                    if (entrada and Partida == True):
                        if (entrada in "vV"):
                            caca = input("digite sua posicao x:y")
                            com_SA.get_flag((int(caca[0]), int(caca[2])))
                            time.sleep(2)
                        else:
                            # com_SA.try_move((int(posAtual[0]),int(posAtual[2])))
                            send_toSR.send("c," + entrada)

            if (receive_fromSR.getAttlist()):  # recebeu alguma atualizacao
                posAtual = receive_fromSR.popAttlist()
                com_SA.try_move((int(posAtual[0]), int(posAtual[2])))

            if (receive_fromSR.getConfigList()):  # recebeu alguma config
                pass

            if(receive_fromSR.getCommandList()):
                msg = receive_fromSR.popCommandList()
                print("DENTRO DO RECEIVE")
                print(msg)
                if (msg in "vV"):
                    print("CHEGOU O V DO SR")
                    com_SA.get_flag((int(posAtual[0]), int(posAtual[2])))


            if (com_SA.get_commands_list()):
                msg = com_SA.pop_commands_list()
                if (msg == "start"):
                    # mensagem do SA para comecar a partida, enviar para o SR
                    Partida = True
                    send_toSR.send("comm,start")
                elif (msg == "stop"):
                    send_toSR.send("comm,stop")
                    #apenas com a partida iniciada#

                    Partida = False

                if (msg == 200):
                    send_toSR.send("ack,OK")
                elif(msg == 400):
                    send_toSR.send("ack,NOK")

                elif (msg == "manual"):
                    mode = "manual"
                    send_toSR.send("comm,manual")
                elif (msg == "automatico"):
                    mode = "automatico"
                    send_toSR.send("comm,automatico")

            if (com_SA.get_flags_list()):
                msg = com_SA.pop_flags_list()
                msg = traduzirListacacas(msg)
                listacacasSS = msg
                send_toSR.send("cacas," + msg)
                # print("FLAGS NO SS" + str(msg))


            if (com_SA.get_map_list()):
                msg = com_SA.pop_map_list()
                if (not None in msg):
                    msg = traduzirListacacas(msg)
                    send_toSR.send("adv," + msg)
                print(msg)

        else:

            if(com_SA.get_commands_list()):
                msg = com_SA.pop_commands_list()
                if(msg == "start"):
                    #mensagem do SA para comecar a partida, enviar para o SR
                    Partida = True
                    send_toSR.send("comm,start")
                elif(msg == "stop"):
                    send_toSR.send("comm,stop")
                    Partida = False
                elif(msg == "manual"):
                    mode = "manual"
                    send_toSR.send("comm,manual")
                elif(msg == "automatico"):
                    mode = "automatico"
                    send_toSR.send("comm,automatico")

            if(com_SA.get_flags_list()):
                msg = com_SA.pop_flags_list()
                msg = traduzirListacacas(msg)
                listacacasSS = msg
                send_toSR.send("cacas," + msg)
                #print("FLAGS NO SS" + str(msg))
                pass

            if(com_SA.get_map_list()):
                msg = com_SA.pop_map_list()
                if(not None in msg):
                    msg = traduzirListacacas(msg)
                    send_toSR.send("adv," + msg)
                print(msg)
                #pass







        #break
        #pass
        #print(send_toSR.getSendList())
        #time.sleep(5)
       #pass
       #print(len(receive_fromSR.getConfigList()))







