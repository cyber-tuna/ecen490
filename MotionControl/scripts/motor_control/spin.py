import roboclaw as rc
import velchange as vel
import time

rc.calibrateRoboclaws()

vel.goXYOmega(0,0,4)
time.sleep(5)
vel.goXYOmega(0,0,0)
