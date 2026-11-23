import sys
import select
from machine import Pin, PWM
from stepper_moterll import StepperMotor
from differential_drivelll import DifferentialDrive
from machine import Pin, ADC
import math
import time

led = Pin("LED", Pin.OUT)

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

left_motor = StepperMotor([0, 1, 2, 3], pwm_pct=0.15, frequency=18_000)
right_motor = StepperMotor([4, 5, 6, 7], pwm_pct=0.15, frequency=18_000)

left_motor.set_step_mode("full")
right_motor.set_step_mode("full")

robot = DifferentialDrive(left_motor, right_motor)

# Opret knappen
button = Pin(22, Pin.IN, Pin.PULL_UP)

aktiv_kommando = "S"

button_previous = 1
running = True 
i = 0
last_press = time.ticks_ms()



led1 = PWM(Pin("GP28"))
led2 = PWM(Pin("GP27"))
led3 = PWM(Pin("GP26"))
led1.freq(1000)
led2.freq(1000)
led3.freq(1000)

led1.duty_u16(0)
led2.duty_u16(0)
led3.duty_u16(0)

def opdater_leds(kommando):
    if kommando in ("H1", "V1", "O1", "N1"):
        led1.duty_u16(65535)
        led2.duty_u16(0)
        led3.duty_u16(0)
    elif kommando in ("H2", "V2", "O2", "N2"):
        led1.duty_u16(65535)
        led2.duty_u16(65535)
        led3.duty_u16(0)
    elif kommando in ("H3", "V3", "O3", "N3"):
        led1.duty_u16(65535)
        led2.duty_u16(65535)
        led3.duty_u16(65535)
    else:
        led1.duty_u16(0)
        led2.duty_u16(0)
        led3.duty_u16(0)

try:
    while True:
        if poll.poll(0):
            ny_linje = sys.stdin.readline().strip()
            if ny_linje != "":
                aktiv_kommando = ny_linje
                
                
        button_now = button.value()
        # Registrer et nyt knaptryk
        if button_now == 0 and button_previous == 1:
            now = time.ticks_ms()

            if time.ticks_diff(now, last_press) >= 200:
                running = not running
                last_press = now

        button_previous = button_now
        
        if not running:
            led.off()
            led1.duty_u16(0)
            led2.duty_u16(0)
            led3.duty_u16(0)
            robot.stop()
            continue
        
        opdater_leds(aktiv_kommando)
        
        if aktiv_kommando == "V1":
            led.on()
            robot.move(1, 1, -1, 0.004)
        elif aktiv_kommando == "H1":
            led.on()
            robot.move(1, -1, 1, 0.004)
        elif aktiv_kommando == "O1":
            led.on()
            robot.move(1, 1, 1, 0.004)
        elif aktiv_kommando == "N1":
            led.on()
            robot.move(1, -1, -1, 0.004)
            
        elif aktiv_kommando == "V2":
            led.on()
            robot.move(1, 1, -1, 0.0095)
        elif aktiv_kommando == "H2":
            led.on()
            robot.move(1, -1, 1, 0.0095)
        elif aktiv_kommando == "O2":
            led.on()
            robot.move(1, 1, 1, 0.0095)
        elif aktiv_kommando == "N2":
            led.on()
            robot.move(1, -1, -1, 0.0095)   
            
        elif aktiv_kommando == "V3":
            led.on()
            robot.move(1, 1, -1, 0.015)
        elif aktiv_kommando == "H3":
            led.on()
            robot.move(1, -1, 1, 0.015)
        elif aktiv_kommando == "O3":
            led.on()
            robot.move(1, 1, 1, 0.015)
        elif aktiv_kommando == "N3":
            led.on()
            robot.move(1, -1, -1, 0.015)
        else:
            led.off()
            robot.stop()

finally:
    led.off()
    led1.duty_u16(0)
    led2.duty_u16(0)
    led3.duty_u16(0)
    robot.stop()  
        
        
