import socket
import threading
import zmq
import random
import sys
import time

class Communication(threading.Thread):

    def __init__(self, ip, port, tag):
        self.sendlist = list()
        threading.Thread.__init__(self)

        if(tag == "toSR"):                                   #se objeto for criado para enviar por SR, topico 2,
            self.Stopic = "1"
            self.context = zmq.Context()
            self.s= self.context.socket(zmq.PUB)
            self.s.bind("tcp://*:7000")           #substituir por ip do SR
            print("conectado")

        if(tag == "fromSR"): #se for criado para receber do SR, topico 1,
            self.Stopic = 1
            int(port)
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.SUB)
            self.socket.connect("tcp://localhost:%s" % port)
            self.socket.setsockopt(zmq.SUBSCRIBE, self.Stopic)



        if(tag == "toSS"):
            self.Stopic = 1
            int(port)
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.PUB)
            self.socket.bind("tcp://*:%s" % port)           #substituir por ip do SS

        if (tag == "fromSS"):
            self.Stopic = "2"
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.SUB)
            self.socket.connect("tcp://localhost:%s" % port)
            #assert isinstance(socket, object)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, self.Stopic)

    def sendMessage(self):
        if(self.sendlist):
            messagedata = self.sendlist.pop()
            print (self.Stopic, messagedata)
            self.s.send(messagedata.encode('utf-8'))
            time.sleep(1)
        else:
            print("Nenhum comando para enviar")

    def receiveMessage(self):
        i = 300
       # while(True):
        i = i - 1
        print ("teste" + str(i))
        self.string = self.socket.recv()
        self.Stopic, messagedata = self.string.split()
        print (self.Stopic, messagedata)
        print("teste2")
        #self.join()

    def run(self):
        print("iniciou ")
        while(1):
            #self.sendlist
            #self.sendMessage()
           # print("entrou")
           # self.receiveMessage();
            print("teste")
            time.sleep(1)


    def send(self, msg):
        self.sendlist.append(msg)


