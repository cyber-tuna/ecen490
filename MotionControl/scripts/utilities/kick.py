#!/usr/bin/env python
import os
def kick():
  os.system("echo 1 > /sys/class/gpio/gpio199/value; sleep .1; echo 0 > /sys/class/gpio/gpio199/value")

if __name__ == '__main__':
  kick()
