import roboclaw as rc
import serial

starting = "Starting Circle Skill"
num_circles = 10
speed = 10
circle_ticks = 19822
splipage = speed * 11
stop_ticks = circle_ticks * num_circles - splipage

# addresses
r1_address = 0x80 # M2
r2_address = 0x81 # M1
r3_address = 0x80 # M1

# radiuses in meters
r1_radius = 0.079
r2_radius = 0.081
r3_radius = 0.063
rw_radius = 0.029

print starting

# stop all motors
rc.M2Forward(r1_address,0)
rc.M1Forward(r2_address,0)
rc.M1Forward(r3_address,0)
rc.ResetEncoderCnts(0x80)
rc.ResetEncoderCnts(0x81)

# start all motors
rc.M2Forward(r1_address,speed)
rc.M1Forward(r2_address,speed)
rc.M1Forward(r3_address,speed)

while rc.readM1encoder(r2_address)[0] <= stop_ticks:
    continue

# stop all motors
rc.M2Forward(r1_address,0)
rc.M1Forward(r2_address,0)
rc.M1Forward(r3_address,0)
rc.ResetEncoderCnts(0x80)
rc.ResetEncoderCnts(0x81)

print rc.readM1encoder(0x81)[0] - circle_ticks * num_circles

# speed     splipage
# 15        179, 187, 129       11
# 50        648, 616, 524       11.92
# 100       1067, 955, 885      9.69
#                               10.87