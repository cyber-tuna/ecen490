"""
    Envelope Subscriber
"""

import sys
sys.path.append('/home/odroid/ecen490/')

import math
import time
import thread
import zmq
from timeit import default_timer

import MotionControl.scripts.kalman_filter.Robot as robot
import MotionControl.scripts.motor_control.velchange as velchange
import MotionControl.scripts.motor_control.roboclaw as roboclaw
import MotionControl.scripts.Point as Point
import MotionControl.scripts.param as param
from MotionControl.scripts.MotionSkills import MotionSkills
from threading import Thread, Lock
from MotionControl.scripts.utilities import kick

ip = "192.168.1.45"
port = "5563"
robot_update_delay = 0.01
goalie_update_delay = 0.004

mutex = Lock()

team1_robot_state = robot.State()
# team2_robot_state = robot.State()
ball = Point.Point()

# Define a function for the thread
def receive(threadName, *args):
    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s" % (ip, port))
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")

    while True:
        address, contents = subscriber.recv_multipart()

        contentArray = contents.split()
        # print contentArray

        home_robot_angle = contentArray[0]
        home_robot_x = contentArray[1]
        home_robot_y = contentArray[2]

        # away_robot_angle = contentArray[3]
        # away_robot_x = contentArray[4]
        # away_robot_y = contentArray[5]

        ball_x = float(contentArray[6])
        ball_y = float(contentArray[7])

        # keep the robot in vision
        if ball_y > 170:
            ball_y = 170.0
        elif ball_y < -170:
            ball_y = -170.0

        ball.x = param.pixelToMeter(ball_x)
        ball.y = param.pixelToMeter(ball_y)

        team1_robot_state.pos_theta_est = param.degreeToRadian(float(home_robot_angle))
        team1_robot_state.pos_x_est = param.pixelToMeter(float(home_robot_x))
        team1_robot_state.pos_y_est = param.pixelToMeter(float(home_robot_y))

        # team2_robot_state.pos_theta_est = param.degreeToRadian(float(away_robot_angle))
        # team2_robot_state.pos_x_est = param.pixelToMeter(float(away_robot_x))
        # team2_robot_state.pos_y_est = param.pixelToMeter(float(away_robot_y))

        try:
            mutex.release()
        except:
            pass

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()

def go_prepare_spin():
    mutex.acquire()

    desiredPoint = Point.Point(param.pixelToMeter(90), 0)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.1) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.1)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.1) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.1)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, 2.0, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
    velchange.goXYOmega(0,0,angular_command.omega)
    time.sleep(angular_command.runTime)

    velchange.goXYOmega(0,0,0)

def main():
    """ main method """

    print "Calibrating Roboclaws..."
    roboclaw.calibrateRoboclaws()
    print "...Done"

    try:
        thread.start_new_thread(receive, ("ReceiverThread", 1))
    except:
        print "Error: unable to start thread"

    mutex.acquire()

    go_prepare_spin()

if __name__ == "__main__":
    main()
