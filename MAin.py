from stepper_motor import StepperMotor
from differential_drive import DifferentialDrive
from machine import Pin
import math
import time
import sensor




# Vi prøver GP14 som input til knappen på PCB-boardet.
# PULL_UP betyder, at pinnen normalt læser 1.
# Hvis knappen forbinder pinnen til GND, læser den 0.
button = Pin(27, Pin.IN, Pin.PULL_UP)


# --------------------------------------------------
# MOTORER
# --------------------------------------------------

# Her opretter vi vores to motorer.
left_motor = StepperMotor(
    [0, 1, 2, 3],
    pwm_pct=0.15,
    frequency=18_000
)

right_motor = StepperMotor(
    [4, 5, 6, 7],
    pwm_pct=0.15,
    frequency=18_000
)

# Vi vælger half-step på begge motorer.
left_motor.set_step_mode("half")
right_motor.set_step_mode("half")

# Her samler vi begge motorer i DifferentialDrive.
robot = DifferentialDrive(left_motor, right_motor)



# --------------------------------------------------
# KØR EN FIRKANT

print("Start")
robot.start_rotate(90, delay=0.02)

while robot.update_rotation():
    time.sleep_ms(1)

print("Færdig")