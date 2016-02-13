# -*- coding: utf-8 -*-
#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import msgpack

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://192.168.1.40:5555")

print("Starting the hello world server…")

while True:
    #  Wait for next request from client
    message = socket.recv()

    decoded_message = msgpack.unpackb(message)

    print("Received request: %s" % decoded_message['created'])

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")