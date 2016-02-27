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
import MotionControl.scripts.MotionSkills as MotionSkills
import time
import thread


ip = "192.168.1.24"
port = "5563"

print "Calibrating Roboclaws"
#roboclaw.calibrateRoboclaws()

state = robot.State()

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

        ball_x = contentArray[1]
        ball_y = contentArray[2]

        robot_angle = contentArray[5]
        robot_x = contentArray[6]
        robot_y = contentArray[7]

        #Update the robot state
        state.pos_x_est = robot_x;
        state.pos_y_est = robot_y;

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
    try:
        thread.start_new_thread( receive, ("ReceiverThread", ) )
    except:
        print "Error: unable to start thread"

    while 1:
        # print("Ball x: %s" % ball_x)
        # print("Ball y: %s" % ball_y)
        # print("Robot angle: %s" % robot_angle)
        print("Robot x: %s" % state.pos_x_est)
        print("Robot y: %s" % state.pos_y_est)
        print

if __name__ == "__main__":
    main()
