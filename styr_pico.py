# Importer de nødvendige biblioteker
# pygame aflæser PS4-controlleren, serial sender data via USB, og time styrer pauser.
# Importerer biblioteker til controller (pygame), USB-kommunikation (serial) og pauser (time)
import pygame
import serial
import time

# Forbinder til din Pico W via USB-porten
# '/dev/cu.usbmodem1101' er portnavnet på Mac, og 115200 er overførselshastigheden (baudrate)
pico = serial.Serial('/dev/cu.usbmodem1101', 115200)
time.sleep(2) # Venter 2 sekunder, så Pico W er helt klar efter forbindelsen åbnes


# Start pygame og tjek om PS4-controlleren er forbundet til MacBook via Bluetooth
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Ingen controller fundet! Tjek Bluetooth på din Mac.")
    exit()  # Stopper programmet, hvis ingen controller er tændt


# Vælg den første tilsluttede controller (indeks 0) og gør den klar
controller = pygame.joystick.Joystick(0)
controller.init()
print("Forbundet til:", controller.get_name())


# Husker den seneste kommando, så vi ikke sender det samme bogstav igen og igen, når vi begynder at skrive bogstaver
sidste_kommando = ""

#hovedløkken der kører uendeligt
try:
    while True:
        pygame.event.pump()
        

         #  Aflæs værdierne fra de to joysticks (tal mellem -1.0 og +1.0)
        # Aflæs venstre joystick (vandret akse: -1.0 er helt til venstre, +1.0 er helt til højre)
        # Aflæs højre joystick (vandret akse: -1.0 er helt til venstre, +1.0 er helt til højre)
        

        x_akse = controller.get_axis(0)
        y_akse = controller.get_axis(3)

        # Oversæt joystick-udslag til et enkelt kommandobogstav
        # Vi bruger grænsen +/- 0.5 som "deadzone", så små rystelser ikke starter motoren
        if abs(x_akse) > abs(y_akse):
            if x_akse < -0.6:
                kommando = "H1" # Hurtig venstre
            elif x_akse < -0.45:
                kommando = "H2" # middel venstre
            elif x_akse < -0.15:
                kommando = "H3" # langsom venstre
            elif x_akse > 0.6:
                kommando = "V1" # Hurtig højre
            elif x_akse > 0.45:
                kommando = "V2" # middel højre
            elif x_akse > 0.15:
                kommando = "V3" # Langsom højre
            else:
                kommando = "S"
            
        else:
            if y_akse < -0.6:
                kommando = "O1" # Hurtig frem (op)
            elif x_akse < -0.45:
                kommando = "O2" # middel frem (op)
            elif y_akse < -0.15:
                kommando = "O3" # Langsom frem (op)
            elif y_akse > 0.6:
                kommando = "N1" # Hurtig tilbage (Ned)
            elif x_akse > 0.45:
                kommando = "N2" # middel tilbage (Ned)
            elif y_akse > 0.15:
                kommando = "N3" # Langsom tilbage (Ned)
            else:
                kommando = "S" # Stop
                
        # Send kun besked når retningen ændrer sig
        if kommando != sidste_kommando:
            pico.write((kommando + "\n").encode()) # Omregner bogstavet til bytes og sender til Pico W
            print("Sendte til Pico W:", kommando)
            sidste_kommando = kommando # Gemmer den nye retning som den seneste
            
        # Holder en kort pause på 0,05 sekunder (50 ms), så computeren ikke overbelastes 
        time.sleep(0.05)
finally:
    # Sender altid STOP til Pico W og slukker LED'er, når du lukker programmet på Mac
    pico.write(b"S\n")
    pico.close()
    print("Stoppede robotten sikkert.")