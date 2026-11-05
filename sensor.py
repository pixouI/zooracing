from machine import ADC, Pin
import time

def measureLight():
    sensor_pin = ADC(Pin(28)) # ADC2 = GPIO28

    print("Starting light measurement")
    current_time = time.time()
    while True:
        lightLvl = sensor_pin.read_u16() # read value of sensor in 16-bit
        if lightLvl > 1000:
            print(f"{lightLvl} = sort")
        else:
            print(f"{lightLvl} = hvid")
        log(str(lightLvl), current_time)
        time.sleep(0.1)

def log(sensorData, time):
    with open(f"log{time}.csv", "a") as log_file:
        log_file.write(sensorData + "\n")

measureLight()

