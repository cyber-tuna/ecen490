#!/usr/bin/python
from roboclaw import *

p = int(65536 * 4) #262144
i = int(65536 * 2) #131072
d = int(65536 * 6)  #65536
q = 308419



def readWheel1pidq():
  return readM2pidq(128)

def readWheel2pidq():
  return readM1pidq(129)

def readWheel3pidq():
  return readM1pidq(128)

def SetWheel1pidq(p,i,d,speedM1):
  SetM2pidq(128,p,i,d,speedM1)

def SetWheel2pidq(p,i,d,speedM2):
  SetM1pidq(129,p,i,d,speedM2)

def SetWheel3pidq(p,i,d,speedM3):
  SetM1pidq(128,p,i,d,speedM3)

def wheel1forward(pwm):
  M2Forward(128,pwm)

def wheel1backward(pwm):
  M2Backward(128,pwm)

def wheel2forward(pwm):
  M1Forward(129,pwm)

def wheel2backward(pwm):
  M1Backward(129,pwm)

def wheel3forward(pwm):
  M1Forward(128,pwm)

def wheel3backward(pwm):
  M1Backward(128,pwm)

print readmainbattery()
p1,i1,d1,q1 = readWheel1pidq()
print "128 M3 P=%.2f" % (p1/65536.0)
print "128 M3 I=%.2f" % (i1/65536.0)
print "128 M3 D=%.2f" % (d1/65536.0)
print "128 M3 QPPS=",q1
p2,i2,d2,q2 = readWheel2pidq()
print "128 M1 P=%.2f" % (p2/65536.0)
print "128 M1 I=%.2f" % (i2/65536.0)
print "128 M1 D=%.2f" % (d2/65536.0)
print "128 M1 QPPS=",q2
p3,i3,d3,q3 = readWheel3pidq()
print "121 M2 P=%.2f" % (p3/65536.0)
print "129 M2 I=%.2f" % (i3/65536.0)
print "129 M2 D=%.2f" % (d3/65536.0)
print "129 M2 QPPS=",q3

def stop():
  wheel1forward(0)
  wheel2forward(0)
  wheel3forward(0)

def readWheel1():
  return read(128,2)

def readWheel2():
  return read(129,1)

def readWheel3():
  return read(128,1)


def read(addr,motor):
  samples = 4
  result = 0
  for i in range(0, samples):
    sample = 0
    if motor == 1:
      sample = readM1speed(addr)
    elif motor == 2:
      sample = readM2speed(addr)
    #print sample
    result = result + sample
  result = result/samples
  return result
  
speedM1Forward=0
speedM1Backward=0
speedM2Forward=0
speedM2Backward=0
speedM3Forward=0
speedM3Backward=0

speed = 54

stop();

#Forwards
wheel1backward(speed); #M1 backward sample 1
wheel2forward(speed); #M2 forward sample 1
time.sleep(2)

speedM1Backward=speedM1Backward+readWheel1()
speedM2Forward=speedM2Forward+readWheel2()

stop();
time.sleep(1);

#Backwards
wheel1forward(speed); #M1 forward sample 1
wheel2backward(speed); #M2 backward sample 1
time.sleep(2)

speedM1Forward=speedM1Forward+readWheel1()
speedM2Backward=speedM2Backward+readWheel2()

stop();
time.sleep(1);

#Left back
wheel2backward(speed); #M2 backward sample 2 
wheel3forward(speed); #M3 forward sample 1
time.sleep(2)

speedM2Backward=speedM2Backward+readWheel2()
speedM2Backward=speedM2Backward/2
speedM3Forward=speedM3Forward+readWheel3()

stop();
time.sleep(1);

#Left forward
wheel2forward(speed); #M2 forward sample 2
wheel3backward(speed); #M3 backward sample 1
time.sleep(2)

speedM2Forward=speedM2Forward+readWheel2()
speedM2Forward=speedM2Forward/2
speedM3Backward=speedM3Backward+readWheel3()

stop();
time.sleep(1);

# RightBack
wheel1forward(speed); #M1 forward sample 2
wheel3backward(speed); #M3 backward sample 2
time.sleep(2)

speedM1Forward=speedM1Forward+readWheel1()
speedM1Forward=speedM1Forward/2
speedM3Backward=speedM3Backward+readWheel3()
speedM3Backward=speedM3Backward/2

stop();
time.sleep(1);

# Right Forward
wheel1backward(speed); #M1 backward sample 2
wheel3forward(speed); #M3 forward sample 2
time.sleep(2)

speedM1Backward=speedM1Backward+readWheel1()
speedM1Backward=speedM1Backward/2
speedM3Forward=speedM3Forward+readWheel3()
speedM3Forward=speedM3Forward/2

stop();

speedM1Forward=(speedM1Forward*127)/speed
speedM1Backward=(speedM1Backward*127)/speed
speedM2Forward=(speedM2Forward*127)/speed
speedM2Backward=(speedM2Backward*127)/speed
speedM3Forward=(speedM3Forward*127)/speed
speedM3Backward=(speedM3Backward*127)/speed

#print speedM1Forward;
#print speedM1Backward;
#print speedM2Forward;
#print speedM2Backward;
#print speedM3Forward;
#print speedM3Backward;

speedM1 = (speedM1Forward - speedM1Backward)/2
speedM2 = (speedM2Forward - speedM2Backward)/2
speedM3 = (speedM3Forward - speedM3Backward)/2

print speedM1
print speedM2
print speedM3

SetWheel1pidq(p,i,d,speedM1)
SetWheel2pidq(p,i,d,speedM2)
SetWheel3pidq(p,i,d,speedM3)

p1,i1,d1,q1 = readWheel1pidq()
print "128 M1 P=%.2f" % (p1/65536.0)
print "128 M1 I=%.2f" % (i1/65536.0)
print "128 M1 D=%.2f" % (d1/65536.0)
print "128 M1 QPPS=",q1
p2,i2,d2,q2 = readWheel2pidq()
print "128 M2 P=%.2f" % (p2/65536.0)
print "128 M2 I=%.2f" % (i2/65536.0)
print "128 M2 D=%.2f" % (d2/65536.0)
print "128 M2 QPPS=",q2
p3,i3,d3,q3 = readWheel3pidq()
print "121 M1 P=%.2f" % (p3/65536.0)
print "129 M1 I=%.2f" % (i3/65536.0)
print "129 M1 D=%.2f" % (d3/65536.0)
print "129 M1 QPPS=",q3

