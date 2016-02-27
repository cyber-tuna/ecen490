import sys
sys.path.append('/home/odroid/ecen490/')

import MotionControl.scripts.motor_control.velchange as velchange
import MotionControl.scripts.motor_control.roboclaw as roboclaw


velchange.goXYOmega(0,0,0)
