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

def is_robot_behind_ball():
    desiredPoint = MotionSkills.getPointBehindBall(ball, param.AWAY_GOAL)

    if (team1_robot_state.pos_x_est > (desiredPoint.x + 0.13) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.13)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.13) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.13)):
        print "robot not behind ball"
        return False
    else:
        print "Robot behind ball"
        return True

def rush_goal():
    print "rush goal"

    mutex.acquire()

    desiredPoint = param.AWAY_GOAL

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.4)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.3) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.3)):

        if team1_robot_state.pos_x_est < ball.x:
            print "break"
            break

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), desiredPoint)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(5)
        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

        # kick.kick()

    velchange.goXYOmega(0,0,0)

def follow_behind_ball():
    mutex.acquire()

    while True:
        desiredPoint = MotionSkills.getPointBehindBall(ball)

        if (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):
            go_to_point_behind_ball()

def go_to_point_behind_ball():

    desiredPoint = MotionSkills.getPointBehindBall(ball, param.AWAY_GOAL)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.13) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.13)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.13) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.13)):

        robot_point = Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est)
        desiredPoint = MotionSkills.getPointBehindBall(ball, param.AWAY_GOAL)

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), param.AWAY_GOAL)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(5)
        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
    velchange.goXYOmega(0,0,angular_command.omega)
    time.sleep(angular_command.runTime)

    velchange.goXYOmega(0,0,0)

def go_to_center():
    mutex.acquire()

    desiredPoint = param.CENTER

    # anglediff = (facingAngle - angleOfTarget + 180) % 360 - 180
    #
    # if (anglediff <= 45 && anglediff>=-45) ....

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.05) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.05)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.05) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.05)):

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), desiredPoint)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(7)
        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega , team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    velchange.goXYOmega(0,0,0)

def defend_goal():

    # vel_x = 0

    # if float(ball_y) < 85 and float(ball_y) > -75:
    #     if state.pos_y_est > param.pixelToMeter(float(ball_y)):
    #         vel_x = -0.7
    #     else:
    #         vel_x = 0.7
    #     velchange.goXYOmega(0,vel_x,0)
    # else:
    #     velchange.goXYOmega(0,0,0)


    desiredPoint = Point.Point(param.HOME_GOAL.x - 0.38 , ball.y)

    # keep robot within the bounds of the goal
    if desiredPoint.y > param.HOME_GOAL.y + 0.25:
        desiredPoint.y = param.HOME_GOAL.y + 0.25
    elif desiredPoint.y < param.HOME_GOAL.y - 0.25:
        desiredPoint.y = param.HOME_GOAL.y - 0.25

    # move to the desiredPoint
    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.13) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.13)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.13) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.13)):

        desiredPoint = Point.Point(param.HOME_GOAL.x - 0.38 , ball.y)
        # keep robot within the bounds of the goal
        if desiredPoint.y > param.HOME_GOAL.y + 0.25:
            desiredPoint.y = param.HOME_GOAL.y + 0.25
        elif desiredPoint.y < param.HOME_GOAL.y - 0.25:
            desiredPoint.y = param.HOME_GOAL.y - 0.25

        targetAngle = MotionSkills.angleBetweenPoints(Point.Point(team1_robot_state.pos_x_est, team1_robot_state.pos_y_est), param.AWAY_GOAL)
        radian180 = param.degreeToRadian(180)
        radian360 = param.degreeToRadian(360)
        radian5 = param.degreeToRadian(7)

        anglediff = (team1_robot_state.pos_theta_est - targetAngle + radian180) % radian360 - radian180

        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        if(anglediff <= radian5 and anglediff >= -radian5):
            omega = 0

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(goalie_update_delay)

    velchange.goXYOmega(0,0,0)

def go_to_home():
    mutex.acquire()

    desiredPoint = Point.Point(param.HOME_GOAL.x - 0.5, 0)

    while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.1) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.1)) or \
            (team1_robot_state.pos_y_est > (desiredPoint.y + 0.1) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.1)):

        command = MotionSkills.go_to_point(team1_robot_state, desiredPoint)
        angular_command = MotionSkills.go_to_angle(team1_robot_state, param.AWAY_GOAL)
        omega = angular_command.omega

        velchange.goXYOmegaTheta(command.vel_x, command.vel_y, omega, team1_robot_state.pos_theta_est)
        time.sleep(robot_update_delay)

    velchange.goXYOmega(0,0,0)

def score_goal():
    print "score goal"
    mutex.acquire()

    go_to_point_behind_ball()
    rush_goal()
    go_to_center()

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

def one_on_one():
    mutex.acquire()

    print "one_on_one"
    state = "defend"
    start = default_timer()
    ball_prev_x = ball.x
    ball_prev_y = ball.y

    while True:
        if state == "defend":
            print "state: defend"
            if ball.x < 0:
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

            if ball.x < 0:
                # transition
                state = "score"
                continue

            if abs(ball.x - ball_prev_x) < 0.02 and abs(ball.y - ball_prev_y) < 0.02:
                if default_timer() - start > 0.5:
                    # transition
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

            # check if a goal was scored
            if(ball.x < -param.pixelToMeter(320)):
                print "goal scored", ball.x

                # transition
                state = "victory"
                continue

            go_to_point_behind_ball()

            # check if a goal was scored
            if(ball.x < -param.pixelToMeter(320)):
                print "goal scored", ball.x

                # transition
                state = "victory"
                continue

            rush_goal()

            # check if a goal was scored
            if(ball.x < -param.pixelToMeter(320)):
                print "goal scored", ball.x

                # transition
                state = "victory"
            else:
                #transition
                state = "defend"

        elif state == "victory":
            print "state: victory"

            go_prepare_spin()
            break

def test():
    print "in test"
    kick.kick()
    # mutex.acquire()
    # desiredPoint = Point.Point(param.pixelToMeter(0), param.pixelToMeter(0))
    #
    # # while (team1_robot_state.pos_x_est > (desiredPoint.x + 0.1) or team1_robot_state.pos_x_est < (desiredPoint.x - 0.1)) or \
    # #         (team1_robot_state.pos_y_est > (desiredPoint.y + 0.1) or team1_robot_state.pos_y_est < (desiredPoint.y - 0.1)):
    #
    # while True:
    #     desiredPoint = Point.Point(param.pixelToMeter(0), param.pixelToMeter(0))
    #     go_to_point2(desiredPoint.x, desiredPoint.y, param.HOME_GOAL)
    #     # time.sleep(0.01)
    #
    # # velchange.goXYOmega(0,0,0)
    #
    #
    #
    # # print "vel_x: %s , vel_y: %s" % (command.vel_x, command.vel_y)
    # # print "theta: ", param.radianToDegree(team1_robot_state.pos_theta_est)
    # # velchange.goXYOmegaTheta(command.vel_x, command.vel_y, 0 , team1_robot_state.pos_theta_est)
    # #
    # # time.sleep(command.runTime)
    # #
    # # velchange.goXYOmega(0,0,0)

def go_to_point2(x, y, lookAtPoint=None):
    print "go_to_point2"
    if lookAtPoint == None:
      lookAtPoint = ball
    desired_x = x
    desired_y = y

    vektor_x = (desired_x-team1_robot_state.pos_x_est) * param.SCALE_VEL
    vektor_y = (desired_y-team1_robot_state.pos_y_est) * param.SCALE_VEL

    mag = math.sqrt(vektor_x**2+vektor_y**2)
    angle = math.atan2(lookAtPoint.y-team1_robot_state.pos_y_est, lookAtPoint.x-desired_x-team1_robot_state.pos_x_est)

    delta_angle = angle-desired_x-team1_robot_state.pos_theta_est

    bestDelta = math.atan2(math.sin(delta_angle), math.cos(delta_angle)) * param.SCALE_OMEGA
    #print bestDelta
    if mag >= param.MAX_SPEED:
      vektor_x = (param.MAX_SPEED/mag)*vektor_x
      vektor_y = (param.MAX_SPEED/mag)*vektor_y
    elif mag < param.MIN_SPEED:
      vektor_x = 0
      vektor_y = 0

    if bestDelta < param.MIN_DELTA and bestDelta > -param.MIN_DELTA:
      bestDelta = 0
    # self.sendCommand(vektor_x, vektor_y, bestDelta, self.robotLocation.theta)

    velchange.goXYOmegaTheta(vektor_x, vektor_y, bestDelta , team1_robot_state.pos_theta_est)

# face away from goal as robot goes to defend
# if the ball starts moving when the robot goes to attack, will it go back to defend?

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

    # follow_behind_ball()
    # rush_goal()
    # score_goal()
    #go_to_point_behind_ball()
    one_on_one()
    #test()

if __name__ == "__main__":
    main()
