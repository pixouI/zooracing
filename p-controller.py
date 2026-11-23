import math
import time
from machine import Pin, PWM, ADC

error = 0
targetVal = 0
kp = 10
leftmotorspeed = 0
rightmotorspeed = 0
sensor1 = 1
sensor2 = 2
sensor3 = 3
sensor4 = 4
sensor5 = 5

# difference between target value and current value (error)
if adc.read_16(sensor1) == "black": # leftmost sensor
    error += -2
elif adc.read_16(sensor2) == "black": # left sensor
    error += -1
elif adc.read_16(sensor3) == "black": # center sensor
    error += 0
elif adc.read_16(sensor4) == "black": # right sensor
    error += 1
elif adc.read_16(sensor5) == "black": # rightmost sensor
    error += 2

errorAvg = error / 5 # average error from all sensors

# negative => too far right (1 or 2), positive => too far left (4 or 5), 0 => on track (3)
p = errorAvg * kp 

leftmotorspeed += p # slows down if negative (too far right), speeds up if positive (too far left)
rightmotorspeed -= p # slows down if positive (too far left), speeds up if negative (too far right)


#if p < 0: # if too far to the right (negative error), slow down left motor and speed up right motor
#    rightmotorspeed = rightmotorspeed - p
#    leftmotorspeed = leftmotorspeed + p
#elif p > 0: # if too far to the left (positive error), slow down right motor and speed up left motor
#    leftmotorspeed = leftmotorspeed + p
#    rightmotorspeed = rightmotorspeed - p
