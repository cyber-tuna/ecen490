from kalman_filter import Robot
from param import *
from motor_control import velchange
import Point
import MotionSkills
import time
from motor_control import roboclaw

#this sets the pid constants
roboclaw.calibrateRoboclaws()

Motion_Skills = MotionSkills.MotionSkills()

state = Robot.State()

desiredPoint = Point.Point(1,2)

command = Motion_Skills.go_to_point(state, desiredPoint)

velchange.goXYOmega(command.vel_x, command.vel_y, 3.1459)

time.sleep(command.runTime)

velchange.goXYOmega(0,0,0)
