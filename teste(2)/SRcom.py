import socket
import threading
import zmq
import random
import sys
import time

class SRcom(threading.Thread):

    def __init__(self, ip, port, tag):
        self.sendlist = list()
        threading.Thread.__init__(self)
        if(tag == "toSR"):                                   #se objeto for criado para enviar por SR, topico 2,
            self.Stopic = 2
            int(port)
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.PUB)
            self.socket.bind('tcp://127.0.0.1:%s' % port)           #substituir por ip do SR
            print("conectado")