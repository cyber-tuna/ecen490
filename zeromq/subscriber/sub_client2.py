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

home_robot_state = robot.State()
away_robot_state = robot.State()

ball_x = 0
ball_y = 0

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

        home_robot_angle = contentArray[0]
        home_robot_x = contentArray[1]
        home_robot_y = contentArray[2]

        away_robot_angle = contentArray[3]
        away_robot_x = contentArray[4]
        away_robot_y = contentArray[5]

        ball_x = param.pixelToMeter(float(contentArray[6]))
        ball_y = param.pixelToMeter(float(contentArray[7]))

        home_robot_state.pos_theta_est = param.degreeToRadian(float(home_robot_angle))
        home_robot_state.pos_x_est = param.pixelToMeter(float(home_robot_x))
        home_robot_state.pos_y_est = param.pixelToMeter(float(home_robot_y))

        away_robot_state.pos_theta_est = param.degreeToRadian(float(away_robot_angle))
        away_robot_state.pos_x_est = param.pixelToMeter(float(away_robot_x))
        away_robot_state.pos_y_est = param.pixelToMeter(float(away_robot_y))

        try:
            mutex.release()
        except:
            print "Attempting to release unlocked mutex"

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


def go_to_point_behind_ball():

    mutex.acquire()

    ball = Point.Point(ball_x, ball_y)
    desiredPoint = MotionSkills.getPointBehindBall(ball)

    while (home_robot_state.pos_x_est > (desiredPoint.x + 0.05) or home_robot_state.pos_x_est < (desiredPoint.x - 0.05)) and /
            (home_robot_state.pos_y_est > (desiredPoint.y + 0.05) or home_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        command = MotionSkills.go_to_point(home_robot_wstate, desiredPoint)
        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, 0, home_robot_state.pos_theta_est)
        time.sleep(0.01)


    velchange.goXYOmega(0,0,0)


def score_goal():
    print "Scoring Goal"

    mutex.acquire()

    #Update the robot state
    # while robot_x == "NULL" or robot_y == "NULL" or robot_angle == "NULL" or ball_x == "NULL" or ball_y == "NULL":
    #     print "NULL state values detected"

    state.pos_x_est = param.pixelToMeter(float(robot_x))
    state.pos_y_est = param.pixelToMeter(float(robot_y))
    state.pos_theta_est = param.degreeToRadian(float(robot_angle))

    ball = Point.Point(param.pixelToMeter(float(ball_x)), param.pixelToMeter(float(ball_y)))

    # print("Ball x: %s Ball y: %s" % (ball.x, ball.y))
    desiredPoint = MotionSkills.getPointBehindBall(ball)
    # print("Point behind ball x: %f y: %f" % (desiredPoint.x, desiredPoint.y))

    command = MotionSkills.go_to_point(state, desiredPoint)
    velchange.goXYOmega(command.vel_x, command.vel_y, 0)
    time.sleep(command.runTime)
    velchange.goXYOmega(0,0,0)

    #Update the robot state
    while robot_x == "NULL" or robot_y == "NULL" or robot_angle == "NULL" or ball_x == "NULL" or ball_y == "NULL":
        print "NULL state values detected"

    state.pos_x_est = param.pixelToMeter(float(robot_x))
    state.pos_y_est = param.pixelToMeter(float(robot_y))
    state.pos_theta_est = param.degreeToRadian(float(robot_angle))

    command = MotionSkills.go_to_angle(state, param.HOME_GOAL)
    velchange.goXYOmega(0, 0, command.omega)
    time.sleep(command.runTime)
    velchange.goXYOmega(0,0,0)

    while robot_x == "NULL" or robot_y == "NULL" or robot_angle == "NULL" or ball_x == "NULL" or ball_y == "NULL":
        print "NULL state values detected"

    state.pos_x_est = param.pixelToMeter(float(robot_x))
    state.pos_y_est = param.pixelToMeter(float(robot_y))
    state.pos_theta_est = param.degreeToRadian(float(robot_angle))
    #
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
        if robot_x == "NULL" or robot_y == "NULL" or robot_angle == "NULL" or ball_x == "NULL" or ball_y == "NULL":
            velchange.goXYOmega(0,0,0)
            continue

        #Update the robot state
        state.pos_x_est = param.pixelToMeter(float(robot_x))
        state.pos_y_est = param.pixelToMeter(float(robot_y))
        state.pos_theta_est = param.degreeToRadian(float(robot_angle));

        if robot_x == "NULL" or robot_y == "NULL" or robot_angle == "NULL" or ball_x == "NULL" or ball_y == "NULL":
            velchange.goXYOmega(0,0,0)
            continue
        if (state.pos_y_est > param.pixelToMeter(float(ball_y)) - 0.1) and (state.pos_y_est < param.pixelToMeter(float(ball_y)) + 0.1):
            velchange.goXYOmega(0,0,0)

            if abs(MotionSkills.deltaBetweenAngles(state.pos_theta_est,0)) > param.degreeToRadian(float(3)):
                print abs(MotionSkills.deltaBetweenAngles(state.pos_theta_est,0))
                zeroAngle = Point.Point(param.pixelToMeter(350), param.pixelToMeter(float(robot_y)))
                command = MotionSkills.go_to_angle(state, zeroAngle)
                velchange.goXYOmega(0, 0, command.omega)
                time.sleep(command.runTime)
                velchange.goXYOmega(0,0,0)
        else:
            #desiredPoint = Point.Point(param.pixelToMeter(float(ball_x)), param.pixelToMeter(float(ball_y)))

            if float(ball_y) < 85 and float(ball_y) > -75:
                if state.pos_y_est > param.pixelToMeter(float(ball_y)):
                    vel_x = -0.7
                else:
                    vel_x = 0.7
                velchange.goXYOmega(0,vel_x,0)
            else:
                velchange.goXYOmega(0,0,0)

        #time.sleep(command.runTime)
        #velchange.goXYOmega(0,0,0)


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

    defend_goal()
    # score_goal()

if __name__ == "__main__":
    print "Calibrating Roboclaws"
    roboclaw.calibrateRoboclaws()
    main()