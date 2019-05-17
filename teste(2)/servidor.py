#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zmq

context = zmq.Context()
s = context.socket(zmq.REP) # create reply socket

s.bind('tcp://*:50007') # bind socket to address
while True:
    message = s.recv() # wait for incoming message
    sMsg = message.decode()
    if not "STOP" in sMsg: # if not to stop...
        print("Sending reply")
        s.send(str("Echo: " + sMsg).encode('utf-8'))
    else: # else...
        break # break out of loop and end
