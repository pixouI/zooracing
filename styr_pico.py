import pygame
import serial
import time

# Forbinder til din Pico W via USB-porten fra dit skærmbillede
pico = serial.Serial('/dev/cu.usbmodem1101', 115200)
time.sleep(2)

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Ingen controller fundet! Tjek Bluetooth på din Mac.")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()
print("Forbundet til:", controller.get_name())

sidste_kommando = ""

while True:
    pygame.event.pump()
    

    
    # Aflæs venstre joystick (vandret akse: -1.0 er helt til venstre, +1.0 er helt til højre)
    # Aflæs højre joystick (vandret akse: -1.0 er helt til venstre, +1.0 er helt til højre)
    

    x_akse = controller.get_axis(0)
    y_akse = controller.get_axis(2)
    
    if x_akse < -0.5:
        kommando = "V"
    elif x_akse > 0.5:
        kommando = "H"
    elif y_akse < -0.5:
        kommando = "O"
    elif y_akse > 0.5:
        kommando = "N"
    else:
        kommando = "S"
        
    # Send kun besked når retningen ændrer sig
    if kommando != sidste_kommando:
        pico.write(kommando.encode())
        print("Sendte til Pico W:", kommando)
        sidste_kommando = kommando
        
    time.sleep(0.05)