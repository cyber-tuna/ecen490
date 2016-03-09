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


