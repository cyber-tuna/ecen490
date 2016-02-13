import velchange
import roboclaw as rc
import time

rc.calibrateRoboclaws()

velchange.goXYOmega(0.5,0,0)
time.sleep(1)
velchange.goXYOmega(0,0,0)
