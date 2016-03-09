"""
   Pubsub envelope subscriber
"""

import sys
from timeit import default_timer
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
robot_update_delay = 0.01

mutex = Lock()

team1_robot_state = robot.State()
team2_robot_state = robot.State()
ball = Point.Point()
goal = param.HOME_GOAL

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

        team1_robot_state.pos_theta_est = param.degreeToRadian(float(home_robot_angle))
        team1_robot_state.pos_x_est = param.pixelToMeter(float(home_robot_x))
        team1_robot_state.pos_y_est = param.pixelToMeter(float(home_robot_y))

        team2_robot_state.pos_theta_est = param.degreeToRadian(float(away_robot_angle))
        team2_robot_state.pos_x_est = param.pixelToMeter(float(away_robot_x))
        team2_robot_state.pos_y_est = param.pixelToMeter(float(away_robot_y))

        try:
            mutex.release()
        except:
            pass

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


def rush_goal():
    print "rush goal"

    mutex.acquire()

    desiredPoint = goal

    while (team1_robot_state.pos_x_est < (desiredPoint.x - 0.4)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.4) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.4)):

        if team1_robot_state.pos_x_est > ball.x:
            break

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, goal)
        omega = angular_command.omega


        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    velchange.goXYOmega(0,0,0)

def follow_behind_ball():
    mutex.acquire()

    while True:
        desiredPoint = MotionSkills.getPointBehindBall(ball)

        if (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):
            go_to_point_behind_ball()

def go_to_point_behind_ball():
    robot_point = Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est)
    desiredPoint = MotionSkills.getPointBehindBall(ball, goal)
    desiredAngle = MotionSkills.angleBetweenPoints(robot_point, goal)

    # print "angle", param.radianToDegree(team1_robot_state.pos_theta_est)
    # print "desiredAngle", param.radianToDegree(desiredAngle)
    # print "desiredPoint", param.meterToPixel(desiredPoint.x), param.meterToPixel(desiredPoint.y)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, goal)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega , team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    angular_command = MotionSkills.go_to_angle(team1_robot_state, goal)
    velchange.goXYOmega(0,0,angular_command.omega)
    time.sleep(angular_command.runTime)

    velchange.goXYOmega(0,0,0)

def go_to_center():
    mutex.acquire()

    desiredPoint = param.CENTER

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, goal)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega , team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    velchange.goXYOmega(0,0,0)

def defend_goal():
    desiredPoint = Point.Point(param.AWAY_GOAL.x + 0.5 , ball.y)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, goal)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(0.001)

    velchange.goXYOmega(0,0,0)

def go_to_home():
    print "going home"
    mutex.acquire()

    desiredPoint = Point.Point(param.AWAY_GOAL.x + 0.5 , ball.y)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, goal)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega , team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    velchange.goXYOmega(0,0,0)


def score_goal():
    print "score goal"
    mutex.acquire()

    go_to_point_behind_ball()
    rush_goal()
    go_to_center()

def one_on_one():
    mutex.acquire()

    state = "defend"
    start = default_timer()
    ball_prev_x = ball.x
    ball_prev_y = ball.y

    while True:
        if state == "defend":
            print "state: defend"
            if ball.x > 0: # < 0
                # transition
                state = "score"
            else:
                # save state
                ball_prev_x = ball.x
                ball_prev_y = ball.y

                # restart timer
                start = default_timer()

                # transition
                state = "defend_goal"

        elif state == "defend_goal":
            print "state: defend_goal"

            if ball.x > 0: # < 0
                # transition
                state = "score"
                continue

            if abs(ball.x - ball_prev_x) < 0.04 and abs(ball.y - ball_prev_y) < 0.04:
                if default_timer() - start > 4:
                    state = "score"
                else:
                    defend_goal()
            else:
                start = default_timer()
                ball_prev_x = ball.x
                ball_prev_y = ball.y
                defend_goal()

        elif state == "score":
            print "state: score"

            go_to_point_behind_ball()
            rush_goal()

            go_to_home()

            # transition
            state = "defend"

# face away from goal as robot goes to defend
# if the ball starts moving when the robot goes to attack, will it go back to defend?

def main():
    """ main method """

    if len(sys.argv) != 2:
        print "Usage: <direction>"
        return

    print "Calibrating Roboclaws"
    roboclaw.calibrateRoboclaws()

    global goal
    direction = sys.argv[1]
    if direction.lower() == "home":
        print "Playing home team"
        goal = param.HOME_GOAL
    elif direction.lower() == "away":
        print "Playing away team"
        goal = param.AWAY_GOAL
    else:
        print "ERROR: invalid direction argument"
        return

    try:
        thread.start_new_thread(receive, ("ReceiverThread", 1))
    except:
        print "Error: unable to start thread"

    mutex.acquire()

    #follow_behind_ball()
    #rush_goal()
    # score_goal()
    # go_to_point_behind_ball()
    one_on_one()


if __name__ == "__main__":
    main()
