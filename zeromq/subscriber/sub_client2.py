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

ip = "192.168.1.28"
port = "5563"

mutex = Lock()

home_robot_state = robot.State()
away_robot_state = robot.State()

ball = Point.Point()

# Define a function for the thread
def receive(threadName, *args):
    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s" % (ip, port))
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")

    print "receive"

    while True:
        address, contents = subscriber.recv_multipart()

        contentArray = contents.split()

        home_robot_angle = contentArray[0]
        home_robot_x = contentArray[1]
        home_robot_y = contentArray[2]

        away_robot_angle = contentArray[3]
        away_robot_x = contentArray[4]
        away_robot_y = contentArray[5]

        ball_x = param.pixelToMeter(float(contentArray[6]))
        ball_y = param.pixelToMeter(float(contentArray[7]))
        ball.x = ball_x
        ball.y = ball_y

        home_robot_state.pos_theta_est = param.degreeToRadian(float(home_robot_angle))
        home_robot_state.pos_x_est = param.pixelToMeter(float(home_robot_x))
        home_robot_state.pos_y_est = param.pixelToMeter(float(home_robot_y))

        away_robot_state.pos_theta_est = param.degreeToRadian(float(away_robot_angle))
        away_robot_state.pos_x_est = param.pixelToMeter(float(away_robot_x))
        away_robot_state.pos_y_est = param.pixelToMeter(float(away_robot_y))

        try:
            mutex.release()
        except:
            pass

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


def rush_goal():
    mutex.acquire()


    desiredPoint = param.HOME_GOAL

    while (home_robot_state.pos_x_est < (desiredPoint.x - 0.4)) or \
            (home_robot_state.pos_y_est > (desiredPoint.y + 0.4) or home_robot_state.pos_y_est < (desiredPoint.y - 0.4)):

        command = MotionSkills.go_to_point(home_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(home_robot_state, param.HOME_GOAL)
        omega = angular_command.omega


        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, home_robot_state.pos_theta_est)
        time.sleep(0.01)

    velchange.goXYOmega(0,0,0)

def follow_behind_ball():
    mutex.acquire()

    while True:
        desiredPoint = MotionSkills.getPointBehindBall(ball)

        if (home_robot_state.pos_x_est > (desiredPoint.x + 0.05) or home_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (home_robot_state.pos_y_est > (desiredPoint.y + 0.05) or home_robot_state.pos_y_est < (desiredPoint.y - 0.05)):
            go_to_point_behind_ball()

def go_to_point_behind_ball():
    mutex.acquire()

    desiredPoint = MotionSkills.getPointBehindBall(ball)

    robot_point = Point.Point(home_robot_state.pos_x_est, home_robot_state.pos_y_est)
    desiredAngle = MotionSkills.angleBetweenPoints(robot_point, param.HOME_GOAL)

    print "angle", param.radianToDegree(home_robot_state.pos_theta_est)
    print "desiredAngle", param.radianToDegree(desiredAngle)

    while (home_robot_state.pos_x_est > (desiredPoint.x + 0.04) or home_robot_state.pos_x_est < (desiredPoint.x - 0.04)) or \
            (home_robot_state.pos_y_est > (desiredPoint.y + 0.04) or home_robot_state.pos_y_est < (desiredPoint.y - 0.04)):

        command = MotionSkills.go_to_point(home_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(home_robot_state, param.HOME_GOAL)
        omega = angular_command.omega


        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega , home_robot_state.pos_theta_est)
        time.sleep(0.01)


    angular_command = MotionSkills.go_to_angle(home_robot_state, param.HOME_GOAL)
    velchange.goXYOmega(0,0,angular_command.omega)
    time.sleep(angular_command.runTime)

    velchange.goXYOmega(0,0,0)

def go_to_center():
    mutex.acquire()

    desiredPoint = param.CENTER

    while (home_robot_state.pos_x_est > (desiredPoint.x + 0.05) or home_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (home_robot_state.pos_y_est > (desiredPoint.y + 0.05) or home_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        command = MotionSkills.go_to_point(home_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(home_robot_state, param.HOME_GOAL)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega , home_robot_state.pos_theta_est)
        time.sleep(0.01)

    velchange.goXYOmega(0,0,0)

def defend_goal():
    mutex.acquire()

    desiredPoint = Point.Point(0.5, ball.y)

    while (home_robot_state.pos_x_est > (desiredPoint.x + 0.05) or home_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (home_robot_state.pos_y_est > (desiredPoint.y + 0.05) or home_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        command = MotionSkills.go_to_point(home_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(home_robot_state, Point.Point(ball.x, ball.y))
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, 0 , home_robot_state.pos_theta_est)
        time.sleep(0.01)

    velchange.goXYOmega(0,0,0)


def score_goal():
    print "score goal"
    mutex.acquire()

    go_to_point_behind_ball()
    rush_goal()
    go_to_center()


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
    #


    #follow_behind_ball()
    #rush_goal()
    score_goal()
    # go_to_point_behind_ball()

if __name__ == "__main__":
    print "Calibrating Roboclaws"
    roboclaw.calibrateRoboclaws()
    main()
