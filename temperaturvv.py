from machine import Pin, ADC, PWM
import time

class Sensor:
    def __init__(self, pin, led_navn):
        self.adc = ADC(Pin(28))
        self.led = PWM(Pin("GP16", Pin.OUT), freq = 1000)
    def opdater(self):        
        adc_value = self.adc.read_u16()
        self.led.duty_u16(adc_value)
        time.sleep(0.1)
        if adc_value < 800:
            print("sort")
        else:
            print("hvid")

linje_sensor = Sensor(28, "GP28")
def tjek_sensor():
    if linje_sensor.opdater() == "sort":
        print("sort")
    else:
        print("hvid")