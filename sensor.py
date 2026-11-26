from machine import ADC, Pin
import time

def measureLight():
    sensor_pin = ADC(Pin(28)) # ADC2 = GPIO28
    print("Starting light measurement")
    startTime = time.time() # time of first measurement
    while True:
        lightLvl = sensor_pin.read_u16() # read value of sensor in 16-bit
        print(lightLvl) # print values to console
        #log(str(lightLvl), startTime) # call log function
        time.sleep(0.1) # delay between measurements (here 0.1 seconds)

def log(sensorData, startTime): # Function to log data to a csv file
    currentTime = time.ticks_ms() # Time of individual measurement
    with open(f"log{startTime}.csv", "a") as log_file: # append line to file 
        log_file.write(f"{currentTime}, {sensorData} \n") # ^ write time and value of measurement, then newline
                       
measureLight() # call the measurement function