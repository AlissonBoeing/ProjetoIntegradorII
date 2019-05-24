import socket
import threading
import zmq
import random
import sys
import time

class Communication(threading.Thread):

    def __init__(self, ip, port, tag):

        self.sendlist = list()
        self.configlist = list()
        self.commandlist = list()
        self.attlist = list()

        threading.Thread.__init__(self)
        self.tag = tag

        if(tag == "toSR"):                                   #se objeto for criado para enviar por SR, topico 2,
            self.Stopic = b"1"
            self.context = zmq.Context()
            self.s= self.context.socket(zmq.PUB)
            self.s.bind("tcp://*:" + port)           #substituir por ip do SR
            print("conectado")

        if(tag == "fromSR"): #se for criado para receber do SR, topico 1,
            self.Stopic = b"2"
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.SUB)
            self.socket.connect("tcp://" + ip + ":%s" % port)
            # assert isinstance(socket, object)
            self.socket.setsockopt(zmq.SUBSCRIBE, self.Stopic)


        if(tag == "toSS"):
            self.Stopic = b"2"
            self.context = zmq.Context()
            self.s = self.context.socket(zmq.PUB)
            self.s.bind("tcp://*:" + port)  # substituir por ip do SR
            print("conectado")

        if (tag == "fromSS"):
            self.Stopic = b"1"
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.SUB)
            self.socket.connect("tcp://"+ ip + ":%s" % port)
            #assert isinstance(socket, object)
            self.socket.setsockopt(zmq.SUBSCRIBE, self.Stopic)

    def sendMessage(self):
        if(self.tag == "toSR"):
            if(self.sendlist):
                #print(len(self.sendlist))
                messagedata = self.sendlist.pop()
                #print (self.Stopic, messagedata)
                self.s.send(str("1" + messagedata).encode('utf-8'))
                time.sleep(1)
        else:
            if (self.sendlist):
                messagedata = self.sendlist.pop()
               # print(self.Stopic, messagedata)
                self.s.send(str("2" + messagedata).encode('utf-8'))
                time.sleep(1)
            #print("Nenhum comando para enviar")

    def receiveMessage(self): #verificar modo que recebemos dados
        self.string = self.socket.recv()
        messagedata = str(self.string)
        messagedata = messagedata[3:-1]
        messagedata = messagedata.split(",")
        if(messagedata[1] in "WASDVwasdv"):
            self.commandlist.append(messagedata[1])
        elif(messagedata[0] == "mac" or messagedata[0] == "cor" or messagedata[0] == "modo" or messagedata[0] == "ack" or messagedata[0] == "posin" or messagedata[0] == "cacas"):
            if(messagedata[0] == "cacas"):
                self.configlist.append("@"+ messagedata[1])
            else:
                self.configlist.append(messagedata[1])
        else:
            self.attlist.append(messagedata[1])
        print ("Recebido " + messagedata[1])


    def run(self):
        print("iniciou ")
        while(1):
            if(self.tag == "toSS" or self.tag == "toSR"):
                self.sendMessage()
                time.sleep(1.5)
            else:
                self.receiveMessage()



    def send(self, msg):
        self.sendlist.append(msg)


    def getCommandList(self):
        return self.commandlist

    def popCommandList(self):
        return self.commandlist.pop()

    def getConfigList(self):
        return self.configlist

    def getAttlist(self):
        return self.attlist

    def popAttlist(self):
        return self.attlist.pop()

    def popConfigList(self):
        return self.configlist.pop()

    def getSendList(self):
        return self.sendlist


