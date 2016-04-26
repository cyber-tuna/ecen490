def follow_ball():
    while True:
        # elif contentArray[0] == "ball":
        # ball_x = contentArray[1]
        # ball_y = contentArray[2]

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
        # state.pos_x_est = param.pixelToMeter(float(robot_x))
        # state.pos_y_est = param.pixelToMeter(float(robot_y))
        # state.pos_theta_est = param.degreeToRadian(float(robot_angle));
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


#Old score goal function
def score_goal():
    print "Scoring Goal"

    mutex.acquire()

    #Update the robot state
    #updateState()

    ball = Point.Point(param.pixelToMeter(float(ball_x)), param.pixelToMeter(float(ball_y)))

    desiredPoint = MotionSkills.getPointBehindBall(ball)

    command = MotionSkills.go_to_point(home_robot_state, desiredPoint)
    velchange.goXYOmega(command.vel_x, command.vel_y, 0)
    time.sleep(command.runTime)
    velchange.goXYOmega(0,0,0)

    #Update the robot state
    #updateState()

    command = MotionSkills.go_to_angle(home_robot_state, param.HOME_GOAL)
    velchange.goXYOmega(0, 0, command.omega)
    time.sleep(command.runTime)
    velchange.goXYOmega(0,0,0)

    #Update the robot state
    #updateState()

    currentPoint = Point.Point(home_robot_state.pos_x_est, home_robot_state.pos_y_est)
    distance = MotionSkills.disBetweenPoints(currentPoint, param.HOME_GOAL)
    length = math.sqrt((param.HOME_GOAL.x-home_robot_state.pos_x_est)**2+(param.HOME_GOAL.y-home_robot_state.pos_y_est)**2)
    runTime = length/0.5
    vel_x = 0.5
    velchange.goXYOmega(vel_x,0,0)
    time.sleep(runTime)
    velchange.goXYOmega(0,0,0)

    print "Finished score_goal"


######################
# LOW-PASS FILTER
######################

team1_robot_state = robot.State()
# team2_robot_state = robot.State()
ball = Point.Point()

# Low pass filter: y[n] = ((1-a) * input[n]) + (a * y[n])
alpha = 0.85

# Define a function for the thread
def receive(threadName, *args):
    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s" % (ip, port))
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")


    first = True

    while True:
        address, contents = subscriber.recv_multipart()

        contentArray = contents.split()

        if first:
            first = False

            # home robot
            home_robot_angle = contentArray[0]
            home_robot_x = contentArray[1]
            home_robot_y = contentArray[2]

            # ball
            ball_x = contentArray[6]
            ball_y = contentArray[7]

        else:
            # home robot
            home_robot_angle = contentArray[0]
            home_robot_x = ((1-alpha) * float(contentArray[1])) + (alpha * float(home_robot_x))
            home_robot_y = ((1-alpha) * float(contentArray[2])) + (alpha * float(home_robot_y))

            # away robot
            # away_robot_angle = contentArray[3]
            # away_robot_x = contentArray[4]
            # away_robot_y = contentArray[5]

            # ball
            ball_x = ((1-alpha) * param.pixelToMeter(float(contentArray[6]))) + (alpha * float(ball_x))
            ball_y = ((1-alpha) * param.pixelToMeter(float(contentArray[7]))) + (alpha * float(ball_y))

        # set state
        team1_robot_state.pos_theta_est = param.degreeToRadian(float(home_robot_angle))
        team1_robot_state.pos_x_est = param.pixelToMeter(float(home_robot_x))
        team1_robot_state.pos_y_est = param.pixelToMeter(float(home_robot_y))
        # team2_robot_state.pos_theta_est = param.degreeToRadian(float(away_robot_angle))
        # team2_robot_state.pos_x_est = param.pixelToMeter(float(away_robot_x))
        # team2_robot_state.pos_y_est = param.pixelToMeter(float(away_robot_y))
        ball.x = float(ball_x)
        ball.y = float(ball_y)

        try:
            mutex.release()
        except:
            pass

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()

######################
# ALTERNATIVE GO TO POINT
######################

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