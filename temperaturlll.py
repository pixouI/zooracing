from machine import Pin, ADC, PWM
import time

class Sensor:
    def __init__(self, pin, led_navn):
        self.adc = ADC(Pin(28))
        self.led = PWM(Pin("GP16", Pin.OUT), freq = 1000)
    def opdater(self):        
        adc_value = self.adc.read_u16()
        print(adc_value)