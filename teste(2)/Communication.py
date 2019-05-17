import socket
import threading
import zmq
import random
import sys
import time

class Communication(threading.Thread):

    def __init__(self, ip, port, tag):

        self.sendlist = list()
        self.receivelist = list()
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
                messagedata = self.sendlist.pop()
                print (self.Stopic, messagedata)
                self.s.send(str("1" + messagedata).encode('utf-8'))
                time.sleep(2)
        else:
            if (self.sendlist):
                messagedata = self.sendlist.pop()
                print(self.Stopic, messagedata)
                self.s.send(str("2" + messagedata).encode('utf-8'))
                time.sleep(2)
            #print("Nenhum comando para enviar")

    def receiveMessage(self):
        self.string = self.socket.recv()
        messagedata = str(self.string)
        messagedata = messagedata[3:-1]
        if(messagedata in "WASDVwasdv"):
            self.commandlist.append(messagedata)
        print ("Recebido " + messagedata)

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
