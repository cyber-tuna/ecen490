import roboclaw as rc
import velchange as vel
import time

rc.calibrateRoboclaws()

vel.goXYOmega(0.2,0,0)
time.sleep(2)
vel.goXYOmega(0,0.2,0)
time.sleep(2)
vel.goXYOmega(-0.2,0,0)
time.sleep(2)
vel.goXYOmega(0,-0.2,0)
time.sleep(2);
vel.goXYOmega(0,0,0)
