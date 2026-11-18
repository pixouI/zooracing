# Importerer biblioteker til USB-læsning (sys, select), hardware-pins (Pin, ADC), matematik og tid
import sys
import select
from machine import Pin
from stepper_moterll import StepperMotor
from differential_drivelll import DifferentialDrive
from machine import Pin, ADC
import math
import time

# Gør den indbyggede grønne LED-lampe på Pico W klar som visuel indikator
led = Pin("LED", Pin.OUT)

# Lytter efter beskeder fra din Mac via USB
# Opsætter en "poll"-lytter, der tjekker om der er kommet nye bogstaver via USB-kablet uden at låse koden
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

# Opretter venstre stepmotor på pin 0, 1, 2, 3 med 15 % motorkraft (PWM) og 18.000 Hz frekvens
left_motor = StepperMotor(
    [0, 1, 2, 3],
    pwm_pct=0.15,
    frequency=18_000
)

# Opretter højre stepmotor på pin 4, 5, 6, 7 med samme motorkraft og frekvens
right_motor = StepperMotor(
    [4, 5, 6, 7],
    pwm_pct=0.15,
    frequency=18_000
    )

# Sætter begge motorer til "full"-step for større skridt og højere hastighed
# Vi vælger full-step på begge motorer.
left_motor.set_step_mode("full")
right_motor.set_step_mode("full")

# Her samler vi begge motorer i DifferentialDrive.
robot = DifferentialDrive(left_motor, right_motor)

# Starter med at sætte den aktive kommando til "S" (Stop), så robotten står stille ved opstart
aktiv_kommando = "S"

# try/finally sikrer, at motorer og LED altid slukkes sikkert, hvis programmet afbrydes
try:
    while True:
            # Tjekker i op til 10 ms, om din Mac har sendt et nyt kommandobogstav via USB
        if poll.poll(10):
            aktiv_kommando = sys.stdin.read(1)
        
        # Udfører bevægelsen ud fra den senest modtagne kommando (1 step ad gangen med 0,005 s delay)
        if aktiv_kommando == "V":
            robot.move(1,1,-1,0.005)  # Drejer til venstre (venstre hjul frem, højre tilbage)

            
        elif aktiv_kommando == "H":
            led.on()
            robot.move(1, -1, 1,0.005) # Drejer til højre (venstre hjul tilbage, højre frem)
            
        elif aktiv_kommando == "O":
            led.on()
            robot.move(1, 1, 1,0.005) # Kører lige fremad (begge hjul fremad)
            
        elif aktiv_kommando == "N":
            led.on()
            robot.move(1, -1, -1,0.005) # Kører lige baglæns (begge hjul baglæns)
            
        else:
            led.off()
            robot.stop()   # Slukker strømmen til begge motorer, når kommandoen er "S"         
            
        
finally:
    # Sikrer at lampe og motorer slukkes helt, hvis koden stoppes
    led.off()
    robot.stop()


