"""

   Pubsub envelope subscriber

   Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""
import zmq
import sys
sys.path.append('/home/odroid/ecen490/')
#from MotionControl.scripts.kalman_filter.Robot import Robot
import MotionControl.scripts.kalman_filter.Robot as robot
import MotionControl.scripts.motor_control.velchange as velchange
import MotionControl.scripts.motor_control.roboclaw as roboclaw
import MotionControl.scripts.Point as Point
import MotionControl.scripts.param as param
from MotionControl.scripts.MotionSkills import MotionSkills
# import MotionControl.scripts.gamepieces.Ball as Ball
import time
import thread


ip = "192.168.1.24"
port = "5563"

#ball = gamepieces.BallLocation()
state = robot.State()
ball_x = 0
ball_y = 0

# Define a function for the thread
def receive(threadName):
    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s" % (ip, port))
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")

    while True:
        address, contents = subscriber.recv_multipart()
        # print contents
        #type, robot_team, robot_angle, robot_x, robot_y = contents.split()
        contentArray = contents.split()
        # if contentArray[0] == "robot1" or "robot2":
        #     robot_number = contentArray[0]
        #     robot_team = contentArray[1]
        #     robot_angle = contentArray[2]
        #     robot_x = contentArray[3]
        #     robot_y = contentArray[4]
        #     print("Robot angle: %s" % robot_angle)
        #     print("Robot x: %s" % robot_x)
        #     print("Robot y: %s" % robot_y)

        global ball_x
        ball_x = contentArray[1]
        global ball_y
        ball_y = contentArray[2]

        robot_angle = contentArray[5]

        robot_x = contentArray[6]
        robot_y = contentArray[7]

        #Update the robot state
        state.pos_x_est = robot_x;
        state.pos_y_est = robot_y;
        state.pos_theta_est = robot_angle;

        # elif contentArray[0] == "ball":
        # ball_x = contentArray[1]
        # ball_y = contentArray[2]

        # print("[%s] %s" % (address, contents))
        # print

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()

def main():
    """ main method """
    # try:
    #     thread.start_new_thread( receive, ("ReceiverThread", ) )
    # except:
    #     print "Error: unable to start thread"


    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s" % (ip, port))
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")

    while True:
        address, contents = subscriber.recv_multipart()
        print contents
        #type, robot_team, robot_angle, robot_x, robot_y = contents.split()
        contentArray = contents.split()
        # if contentArray[0] == "robot1" or "robot2":
        #     robot_number = contentArray[0]
        #     robot_team = contentArray[1]
        #     robot_angle = contentArray[2]
        #     robot_x = contentArray[3]
        #     robot_y = contentArray[4]
        #     print("Robot angle: %s" % robot_angle)
        #     print("Robot x: %s" % robot_x)
        #     print("Robot y: %s" % robot_y)

        # global ball_x
        ball_x = contentArray[1]
        # global ball_y
        ball_y = contentArray[2]

        robot_angle = contentArray[5]
        robot_x = contentArray[6]
        robot_y = contentArray[7]

        #Update the robot state
        state.pos_x_est = param.pixelToMeter(float(robot_x))
        state.pos_y_est = param.pixelToMeter(float(robot_y))
        state.pos_theta_est = param.degreeToRadian(float(robot_angle));

        # elif contentArray[0] == "ball":
        # ball_x = contentArray[1]
        # ball_y = contentArray[2]

        # print("[%s] %s" % (address, contents))
        # print

        # desiredPoint = Point.Point(param.pixelToMeter(float(ball_x)), param.pixelToMeter(float(ball_y)))
        #
        # print("Desired x: %s" % desiredPoint.x)
        # print("Desired y: %s" % desiredPoint.y)
        #
        # print("Robot x: %s" % state.pos_x_est)
        # print("Robot y: %s" % state.pos_y_est)

        # command = MotionSkills.go_to_point(state, desiredPoint)
        # velchange.goXYOmega(command.vel_x, command.vel_y, 0)
        # print("Run Time: %s" % command.runTime)
        # time.sleep(command.runTime)
        # velchange.goXYOmega(0,0,0)

        ball =  Point.Point(param.pixelToMeter(float(ball_x)), param.pixelToMeter(float(ball_y)))

        command = MotionSkills.go_to_angle(state, ball)
        velchange.goXYOmega(0, 0, command.omega)
        time.sleep(command.runTime)
        velchange.goXYOmega(0,0,0)

        return

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()

    # #while 1:
    #     # print("Ball x: %s" % ball_x)
    #     # print("Ball y: %s" % ball_y)
    #     # print("Robot angle: %s" % robot_angle)
    #     print("Robot x: %s" % state.pos_x_est)
    #     print("Robot y: %s" % state.pos_y_est)
    #
    #     desiredPoint = Point.Point(param.pixelToMeter(int(ball_x)), param.pixelToMeter(int(ball_y)))
    #     command = MotionSkills.go_to_point(state, desiredPoint)
    #     velchange.goXYOmega(command.vel_x, command.vel_y, 0)
    #     time.sleep(command.runTime)
    #     velchange.goXYOmega(0,0,0)
    #
    #     print

if __name__ == "__main__":
    print "Calibrating Roboclaws"
    roboclaw.calibrateRoboclaws()
    main()
