# -*- coding: utf-8 -*-
#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import msgpack

class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1

   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary


useful_dict = {
    "id": 1,
    "created": "feb 5",
}

jared = Employee("Jared", 2000)

msg = msgpack.packb(useful_dict);

this_dict_again = msgpack.unpackb(msg)
print(useful_dict['id']);

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.40:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    socket.send(msg)

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))