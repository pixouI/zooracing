# Name: Jeppe Nielsen
# Email: jepni26@student.sdu.dk

from stepper_motor import StepperMotor
from diff_drive import DiffDrive
from time import sleep_us

"""tuner"""
pwm = 0.40 # Set duty cycle of pins
delay = 1000 # Set delay between steps

# LED pins: 16, 17, 18, 19
# PWM pins: 0, 1, 2, 3, 4, 5, 6, 7

# The main function that users control the motor from by importing the StepperMotor class. 
motor1 = StepperMotor([0, 1, 2, 3], pwm_pct=pwm, frequency=25_000) # Set duty cycle and frequency of pins.     
motor2 = StepperMotor([4, 5, 6, 7], pwm_pct=pwm, frequency=25_000) 
robot = DiffDrive(motor1, motor2) # Create a differential drive object with the two motors
robot.driveInit() # Initialize the differential drive

try:
    while (True): # Loop to keep motors running
        robot.driverdriver(1, 1) # Set speeds for both motors
        sleep_us(delay)
finally:
    motor1.stop() # Stop motors when program is interrupted
    motor2.stop()
