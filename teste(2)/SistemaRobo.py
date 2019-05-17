from Communication import *
from Treasure import *
from threading import Thread
import time

#-----------------------#
# Se conectar no SS -> envia mac, espera OK #
#

mac = "02:16:53:45:b3:9a"

receive_fromSS = Communication("127.0.0.1", "50009", "fromSS")

send_toSS = Communication("127.0.0.1", "50008", "toSS")

#send_toSS = Communication("127.0.0.1", "50010", "toSS")

#send_toSS.start()

receive_fromSS.start()

send_toSS.start()



while(1):
    commandList = list(receive_fromSS.getCommandList())

    while(commandList):
        commandList.pop()


#send_toSS.send(mac)


#while(1):
    #print("teste")
    #send_toSS.send(mac)
#    time.sleep(1)

