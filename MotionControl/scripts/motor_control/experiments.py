import roboclaw as rc
import serial
import time

seconds = 5
speeds = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65,
          70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125)

circle_ticks = 19822

# addresses
r1_address = 0x80 # M2
r2_address = 0x81 # M1
r3_address = 0x80 # M1

# radiuses in meters
r1_radius = 0.079
r2_radius = 0.081
r3_radius = 0.063
rw_radius = 0.029

for speed in speeds:
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

    time.sleep(seconds)

    # stop all motors
    rc.M2Forward(r1_address,0)
    rc.M1Forward(r2_address,0)
    rc.M1Forward(r3_address,0)

    r1_ticks_per_second = rc.readM2encoder(r1_address)[0]/seconds
    r2_ticks_per_second = rc.readM1encoder(r2_address)[0]/seconds
    r3_ticks_per_second = rc.readM1encoder(r3_address)[0]/seconds

    print speed, r1_ticks_per_second, r2_ticks_per_second, r3_ticks_per_second

# speed     ticks/second (r1, r2, r3)
# 5         6565 7316 7206
# 10        14103 15410 15189
# 15        21744 23391 23160
# 20        29412 31361 31187
# 25        37284 38919 39325
# 30        45164 46916 47410
# 35        53177 55065 55714
# 40        61693 63290 64199
# 45        70002 71671 72669
# 50        78266 80219 81127
# 55        87225 88925 90211
# 60        96173 97800 99225
# 65        104847 106588 108231
# 70        113851 115615 117111
# 75        123363 125192 126648
# 80        132922 134561 136575
# 85        140428 143517 143866
# 90        151019 153696 154651
# 95        161729 164575 165887
# 100       173328 175953 177346
# 105       183519 186532 187681
# 110       194477 196839 198408
# 115       205459 207092 209503
# 120       216418 217502 220354
# 125       227483 228021 231491