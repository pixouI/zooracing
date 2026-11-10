from stepper_moterll import StepperMotor
from differential_drivelll import DifferentialDrive
from machine import Pin, ADC
from temperaturlll import Sensor
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


linje_sensor = Sensor(28, "GP28")
def tjek_sensor():
    raa_data = linje_sensor.opdater()


# --------------------------------------------------
# BEREGNINGER
# --------------------------------------------------

# Robotens mål i centimeter.
wheel_diameter = 8.5
wheel_distance = 24.5
distance = 100

# Antal full-steps pr. hjulomdrejning.
steps_per_rotation = 200

# Beregner hjulets omkreds.
wheel_circumference = math.pi * wheel_diameter

# Beregner antal steps for at køre 100 cm.
forward_steps = round(
    distance / wheel_circumference * steps_per_rotation
)

# Beregner hvor langt hvert hjul skal køre ved 90 graders drejning.
turn_distance = math.pi * wheel_distance / 4

# Omregner drejningens distance til steps.
turn_steps = round(
    turn_distance / wheel_circumference * steps_per_rotation
)


# --------------------------------------------------
# START-NEDTÆLLING (KNAP SLETTET)
# --------------------------------------------------

print("Robotten starter om 2 sekunder...")
time.sleep(2)

# --------------------------------------------------
# KØR EN FIRKANT
# --------------------------------------------------

try:
    for i in range(4):
    # Vi gentager bevægelsen fire gange. 
        print("Kører side", i + 1)

        # Begge motorer kører fremad i 100 cm.
        for _ in range(forward_steps):
            tjek_sensor()
            robot.move(
                1,
                1,
                1,
            )

        # Holder en kort pause.
        time.sleep(0.5)

        print("Drejer 90 grader")

        # Hjulene kører i hver sin retning.
        for _ in range(forward_steps):
            tjek_sensor()
            robot.move(
                1,
                1,
                -1,
            )

        # Holder en kort pause.
        time.sleep(0.5)

finally:

    # Sikrer, at begge motorer stoppes.
    robot.stop()

print("Firkanten er færdig!")
 
