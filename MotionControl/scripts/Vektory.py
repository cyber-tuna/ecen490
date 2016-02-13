#!/usr/bin/env python

import math
import rospy
import sys
import time
#from robot_soccer.srv import *
from MotionSkills import *
from motor_control import roboclaw
from gamepieces.HomeRobot import HomeRobot
from gamepieces.HomeRobot import RobotCommand
#from kalman_filter.Ball import *
from param import *
from utilities.kick import kick
from kalman_filter.Locations import *
import sched
import cPickle as pickle

#from enum import Enum
#class GameState(Enum):
#  stop = 1
#  play = 2
#  center = 3
#  startPosition = 4
#  test = 5

#class State(Enum):
#  rushGoal = 1
#  getBehindBall = 2
#  rotateToAngleBehindBall = 3
#  check = 4
#  returnToPlay = 5

#class TestState(Enum):
#  check = 1
#  rushGoal = 2
#  getBehindBall = 3

#class Rotate(Enum):
#  none = 1
#  clockwise = 2
#  counterClockwise = 3

class Vektory:
  def __init__(self):
    self.locations = None
#    self.ball = Ball()
    self.robotLocation_x = 0
    self.robotLocation_y = 0
    self.robotLocation_theta = 0
    self.distanceToBall = 0
#    self.state = State.check
#    self.rotate = Rotate.none
#    self.stopRushingGoalTime = 0
    self.newCommand = False
    self.vel_x = 0
    self.vel_y = 0
    self.omega = 0
#    self.gameState = GameState.stop
#    self.stopped = True
#    self.testState = TestState.check

  def sendCommand(self, vel_x, vel_y, omega, theta = 0):
    command = RobotCommand(-1,vel_x, vel_y, omega, theta)
    command.execute()
    # sendCommand = rospy.ServiceProxy('commandSent', commandsent)
    # try:
    #   resp1 = sendCommand(*(command.getCommandToSend()))
    # except rospy.ServiceException as exc:
    #   print("Service did not process request: " + str(exc))

  def setRobotXY(self, xvalue, yvalue, thetavalue):
    self.robotLocation_x = xvalue
    self.robotLocation_y = yvalue
    self.robotLocation_theta = thetavalue

  def go_to_point(self,x, y, lookAtPoint):
    #print "go_to_point"
    desired_x = x
    desired_y = y

    vektor_x = (desired_x-self.robotLocation_x) * SCALE_VEL
    vektor_y = (desired_y-self.robotLocation_y) * SCALE_VEL

    mag = math.sqrt(vektor_x**2+vektor_y**2)
    angle = math.atan2(lookAtPoint[1]-self.robotLocation_y, lookAtPoint[0]-self.robotLocation_x)

    delta_angle = angle-self.robotLocation_theta

    bestDelta = math.atan2(math.sin(delta_angle), math.cos(delta_angle)) * SCALE_OMEGA
    #print bestDelta
    if mag >= MAX_SPEED:
      vektor_x = (MAX_SPEED/mag)*vektor_x
      vektor_y = (MAX_SPEED/mag)*vektor_y
    elif mag < MIN_SPEED:
      vektor_x = 0
      vektor_y = 0

    if bestDelta < MIN_DELTA and bestDelta > -MIN_DELTA:
      bestDelta = 0
    self.sendCommand(vektor_x, vektor_y, bestDelta, self.robotLocation_theta)

if __name__ == '__main__':
  #winner = Vektory()
  #winner.go()
  obj = Vektory()
  obj.setRobotXY(126, 145, 201)
  obj.go_to_point(0, 0, (0, 0))

