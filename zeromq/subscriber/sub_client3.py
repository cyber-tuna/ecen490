"""
   Pubsub envelope subscriber
"""

import sys
sys.path.append('/home/odroid/ecen490/')

#from MotionControl.scripts.kalman_filter.Robot import Robot
import MotionControl.scripts.kalman_filter.Robot as robot
import MotionControl.scripts.motor_control.velchange as velchange
import MotionControl.scripts.motor_control.roboclaw as roboclaw
import MotionControl.scripts.Point as Point
import MotionControl.scripts.param as param
from MotionControl.scripts.MotionSkills import MotionSkills
from threading import Thread, Lock
import math
#from MotionControl.scripts.gamepieces.Ball import Ball

import time
import thread
import zmq

ip = "192.168.1.24"
port = "5563"

mutex = Lock()

state = robot.State()
ball_x = 0
ball_y = 0
robot_angle = 0
robot_x = 0
robot_y = 0

# Define a function for the thread
def receive(threadName, *args):
    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s" % (ip, port))
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")

    while True:
        address, contents = subscriber.recv_multipart()
        print contents

        contentArray = contents.split()

        global ball_x
        global ball_y
        global robot_angle
        global robot_x
        global robot_y

        ball_x = contentArray[1]
        ball_y = contentArray[2]

        print "Ball x: %s  Ball y: %s" % (ball_x, ball_y)
        robot_angle = contentArray[5]
        robot_x = contentArray[6]
        robot_y = contentArray[7]

        try:
            mutex.release()
        except:
            print "Attempting to release unlocked mutex"

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()

def score_goal():
    print "Scoring Goal"

    rx = robot_x
    ry = robot_y
    ra = robot_angle
    bx = ball_x
    by = ball_y

    if rx == "NULL" or ry == "NULL" or ra == "NULL" or bx == "NULL" or by == "NULL":
        # print "NULL state values detected"
        return

    mutex.acquire()

    #Update the robot state
    state.pos_x_est = param.pixelToMeter(float(rx))
    state.pos_y_est = param.pixelToMeter(float(ry))
    state.pos_theta_est = param.degreeToRadian(float(ra))

    ball = Point.Point(param.pixelToMeter(float(bx)), param.pixelToMeter(float(by)))

    # print("Ball x: %s Ball y: %s" % (ball.x, ball.y))
    desiredPoint = MotionSkills.getPointBehindBall(ball)
    # print("Point behind ball x: %f y: %f" % (desiredPoint.x, desiredPoint.y))

    command = MotionSkills.go_to_point(state, desiredPoint)
    velchange.goXYOmega(command.vel_x, command.vel_y, 0)
    time.sleep(command.runTime)
    velchange.goXYOmega(0,0,0)

    #Update the robot state
    state.pos_x_est = param.pixelToMeter(float(rx))
    state.pos_y_est = param.pixelToMeter(float(ry))
    state.pos_theta_est = param.degreeToRadian(float(ra))

    command = MotionSkills.go_to_angle(state, param.HOME_GOAL)
    velchange.goXYOmega(0, 0, command.omega)
    time.sleep(command.runTime)
    velchange.goXYOmega(0,0,0)

    # #Update the robot state
    state.pos_x_est = param.pixelToMeter(float(rx))
    state.pos_y_est = param.pixelToMeter(float(ry))
    state.pos_theta_est = param.degreeToRadian(float(ra))

    currentPoint = Point.Point(state.pos_x_est, state.pos_y_est)
    distance = MotionSkills.disBetweenPoints(currentPoint, param.HOME_GOAL)
    length = math.sqrt((param.HOME_GOAL.x-state.pos_x_est)**2+(param.HOME_GOAL.y-state.pos_y_est)**2)
    runTime = length/0.5
    vel_x = 0.5
    velchange.goXYOmega(vel_x,0,0)
    time.sleep(runTime)
    velchange.goXYOmega(0,0,0)

    print "Finished score_goal"

def defend_goal():
    while True:

        rx = robot_x
        ry = robot_y
        ra = robot_angle
        bx = ball_x
        by = ball_y

        if rx == "NULL" or ry == "NULL" or ra == "NULL" or bx == "NULL" or by == "NULL":
            velchange.goXYOmega(0,0,0)
            continue

        mutex.acquire()

        #Update the robot state
        state.pos_x_est = param.pixelToMeter(float(rx))
        state.pos_y_est = param.pixelToMeter(float(ry))
        state.pos_theta_est = param.degreeToRadian(float(ra));

        if rx == "NULL" or ry == "NULL" or ra == "NULL" or bx == "NULL" or by == "NULL":
            velchange.goXYOmega(0,0,0)
            continue
        if (state.pos_y_est > param.pixelToMeter(float(by)) - 0.1) and (state.pos_y_est < param.pixelToMeter(float(by)) + 0.1):
            velchange.goXYOmega(0,0,0)

            if abs(MotionSkills.deltaBetweenAngles(state.pos_theta_est,0)) > param.degreeToRadian(float(3)):
                print abs(MotionSkills.deltaBetweenAngles(state.pos_theta_est,0))
                zeroAngle = Point.Point(param.pixelToMeter(350), param.pixelToMeter(float(ry)))
                command = MotionSkills.go_to_angle(state, zeroAngle)
                velchange.goXYOmega(0, 0, command.omega)
                time.sleep(command.runTime)
                velchange.goXYOmega(0,0,0)
        else:
            #desiredPoint = Point.Point(param.pixelToMeter(float(bx)), param.pixelToMeter(float(by)))

            if float(by) < 85 and float(by) > -75:
                if state.pos_y_est > param.pixelToMeter(float(by)):
                    vel_x = -0.7
                else:
                    vel_x = 0.7
                velchange.goXYOmega(0,vel_x,0)
            else:
                velchange.goXYOmega(0,0,0)

        #time.sleep(command.runTime)
        #velchange.goXYOmega(0,0,0)

def follow_ball():
    while True:
        # elif contentArray[0] == "ball":
        # ball_x = contentArray[1]
        # by = contentArray[2]

        # print("[%s] %s" % (address, contents))
        # print

        #
        # print("Desired x: %s" % desiredPoint.x)
        # print("Desired y: %s" % desiredPoint.y)
        #
        # print("Robot x: %s" % state.pos_x_est)
        # print("Robot y: %s" % state.pos_y_est)

        if robot_x == "NULL" or robot_y == "NULL" or robot_angle == "NULL" or ball_x == "NULL" or ball_y == "NULL":
            continue

        #Update the robot state
        state.pos_x_est = param.pixelToMeter(float(robot_x))
        state.pos_y_est = param.pixelToMeter(float(robot_y))
        state.pos_theta_est = param.degreeToRadian(float(robot_angle));
        #
        # desiredPoint = Point.Point(param.pixelToMeter(float(ball_x)), param.pixelToMeter(float(ball_y)))
        # zeroAngle = Point.Point(param.pixelToMeter(350), param.pixelToMeter(float(robot_y)))
        #
        # command = MotionSkills.go_to_angle(state, zeroAngle)
        # velchange.goXYOmega(0, 0, command.omega)
        # time.sleep(command.runTime)
        # velchange.goXYOmega(0,0,0)
        #
        # command = MotionSkills.go_to_point(state, desiredPoint)
        # velchange.goXYOmega(command.vel_x, command.vel_y, 0)
        # # print("Run Time: %s" % command.runTime)
        # time.sleep(command.runTime)
        # velchange.goXYOmega(0,0,0)
        # command = MotionSkills.go_to_point(state, desiredPoint)
        # velchange.goXYOmega(command.vel_x, command.vel_y, 0)
        # time.sleep(command.runTime)
        # velchange.goXYOmega(0,0,0)

        # return


def main():
    """ main method """

    # if len(sys.argv) != 2:
    #     print "Usage: <skill>"
    #
    # skill = argv[1]

    try:
        thread.start_new_thread(receive, ("ReceiverThread", 1))
    except:
        print "Error: unable to start thread"

    mutex.acquire()

    # if skill == "score":
    #     score_goal()
    # elif skill == "follow":
    #     follow_ball()
    # else:
    #     print "invalid skill"
    #     return

    #defend_goal()
    score_goal()

if __name__ == "__main__":
    print "Calibrating Roboclaws"
    roboclaw.calibrateRoboclaws()
    main()
