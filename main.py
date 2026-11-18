import sys
import select
from machine import Pin
from stepper_moterll import StepperMotor
from differential_drivelll import DifferentialDrive
from machine import Pin, ADC
import math
import time

led = Pin("LED", Pin.OUT)

# Lytter efter beskeder fra din Mac via USB
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

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

while True:
    if poll.poll(10):
        kommando = sys.stdin.read(1)
        
        if kommando == "V":
            robot.move(1,1,-1)
            
        elif kommando == "H":
            robot.move(1,-1,1)
            
        elif kommando == "S":
            robot.stop()          
            
            
        
        
