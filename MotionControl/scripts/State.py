'''
    File name: State.py
    Author: BaeMax
'''

import msgpack

class State:
    'Wrapper for a state dictionary'
    def __init__(self, pos_x_est = None, pos_y_est = None, \
                       pos_x_des = None, pos_y_des = None, \
                       pos_theta_est = None , pos_theta_des = None, \
                       vel_x = None, vel_y = None, omega = None, time = None):
        self.state_dict = {}

        self.state_dict["pos_x"] = {}
        self.state_dict["pos_x"]["est"] = pos_x_est
        self.state_dict["pos_x"]["des"] = pos_x_des

        self.state_dict["pos_y"] = {}
        self.state_dict["pos_y"]["est"] = pos_y_est
        self.state_dict["pos_y"]["des"] = pos_y_des

        self.state_dict["pos_theta"] = {}
        self.state_dict["pos_theta"]["est"] = pos_y_est
        self.state_dict["pos_theta"]["des"] = pos_y_des

        self.state_dict["vel_x"] = vel_x
        self.state_dict["vel_y"] = vel_y
        self.state_dict["omega"] = omega
        self.state_dict["time"] = time

    def pack(self):
        'Returns a MessagePack string representation of the state dictionary'
        return msgpack.packb(self.state_dict);
