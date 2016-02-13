import roboclaw as rc
import velchange as vel
import time

rc.calibrateRoboclaws()

pixel_x = 132
pixel_y = 99

x = pixel_x / 40
y = pixel_y / 40

vel.goXYOmega(-0.2,0,0)
time.sleep(x)
vel.goXYOmega(0,-0.2,0)
time.sleep(y)
vel.goXYOmega(0,0,0)
