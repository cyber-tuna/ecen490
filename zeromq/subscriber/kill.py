import sys
import os

sys.path.append('/home/odroid/ecen490/')

os.system("echo 0 > /sys/class/gpio/gpio199/value;")

import MotionControl.scripts.motor_control.velchange as velchange
import MotionControl.scripts.motor_control.roboclaw as roboclaw


velchange.goXYOmega(0,0,0)
