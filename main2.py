from stepper_moterll import StepperMotor
from differential_drivelll import DifferentialDrive
from machine import Pin, ADC
import math
import time



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

# Vi vælger full-step på begge motorer.
left_motor.set_step_mode("half")
right_motor.set_step_mode("half")

# Her samler vi begge motorer i DifferentialDrive.
robot = DifferentialDrive(left_motor, right_motor)



# --------------------------------------------------
# START-NEDTÆLLING (KNAP SLETTET)
# --------------------------------------------------

print("Robotten starter om 2 sekunder...")
time.sleep(1)

step_delay = 2
# --------------------------------------------------
# KØR EN FIRKANT
# --------------------------------------------------

try:
    #hvor mange gange den skal gøre det i løkken range
    for i in range(1):
    
        # hjulene drejer 180 grader. i steps
        for _ in range(600):
            robot.move(1,-1,-1)

        # Holder en kort pause på 2 sekunder i step_delay.
        time.sleep(0.1)
        time.sleep(step_delay)

        print("Drejer 180 grader")

        # Hjulene drejer 180 grader den samme vej balæns
        for _ in range(625):
            robot.move(1,1,1)

        # Holder en kort pause.
        time.sleep(2)

finally:

    # Sikrer, at begge motorer stoppes.
    robot.stop()

print("cirklen er færdig!")
 


