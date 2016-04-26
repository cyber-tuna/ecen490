import bresenham as br
import MotionControl.scripts.param as param

def obstruction(start, end, team2_robot_state):
    team2_x = param.meterToPixel(team2_robot_state.pos_x_est)
    team2_y = param.meterToPixel(team2_robot_state.pos_y_est)

    ray = br.bresenham([param.meterToPixel(start.x), param.meterToPixel(start.y)], [param.meterToPixel(end.x), param.meterToPixel(end.y)])

    for point in ray.path:
        print point[0], "," , point[1]
        if point[0] < (team2_x + 30) and point[0] > (team2_x - 30) and \
           point[1] < (team2_y + 30) and point[1] > (team2_y - 30):
           return True

    return False

# if __name__ == '__main__':
#     obstruction([0,0],[649,449])
