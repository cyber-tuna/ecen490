'''
    File name: pub_server.py
    Author: BaeMax
'''

import zmq
import random
import sys

sys.path.append('/home/odroid/ecen490/MotionControl/scripts')

import time
import msgpack
import State


# VektorKrum's Robot.py
# class State:
#     def __init__(self):
#         self.time = 0.0
#         self.pos_x_est = 0.0
#         self.pos_x_des = 0.0
#         self.pos_y_est = 0.0
#         self.pos_y_des = 0.0
#         self.pos_theta_est = 0.0
#         self.pos_theta_des = 0.0
#         self.vel_x = 0.0
#         self.vel_y = 0.0
#         self.omega = 0.0
#         self.kill = 0.0

# state_dict = {
#     "time": 0.0,
#     "pos_x": {
#         "est": 0.0,
#         "des": 0.0,
#     },
#     "pos_y": {
#         "est": 0.0,
#         "des": 0.0,
#     },
#     "pos_theta": {
#         "est": 0.0,
#         "des": 0.0,
#     },
#     "vel_x": 0.0,
#     "vel_y": 0.0,
#     "omega": 0.0,
#     "kill": 0.0,
# }



#msg = msgpack.packb(state_dict);

robot_state = State.State(54,22,2,1)
msg = robot_state.pack()

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = 10001
    # print topic, state_dict
    socket.send("%d %s" % (topic, msg))
    time.sleep(1)
