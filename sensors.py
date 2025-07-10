from machine import ADC
from config import DEV_MODE
import time

lastTemp = 0.0
lastVolt = 12.0


def getTemp():
    global lastTemp
    if DEV_MODE:
        t = lastTemp + 1
        if t > 110.0:
            t = 20.0
        lastTemp = t
        return t
    adcpin = 4
    sensor = ADC(adcpin)
    adc_value = sensor.read_u16()
    volt = (3.3 / 65535) * adc_value
    temperature = 27 - (volt - 0.706) / 0.001721
    return temperature


def getBattery():
    global lastVolt
    if DEV_MODE:
        t = lastVolt + 0.1
        if t > 15.0:
            t = 11.0
        lastVolt = t
        return t
    adcpin = 3
    sensor = ADC(adcpin)
    adc_value = sensor.read_u16()
    volt = (3.3 / 65535) * adc_value * (15.0 / 3.3)  # Example scaling
    return volt


def getTimeSinceBoot():
    return time.ticks_ms() / 1000.0  # Return time in seconds since boot
