from st7735 import TFT
from st7735 import sysfont
from machine import SPI,Pin,ADC, 
import network
import time
import math

def showNetworks():
    font = sysfont.sysfont
    wlan = network.WLAN(network.STA_IF)
    nets = wlan.scan()
    tft.fill(TFT.BLACK)
    tft.text((0, 0), 'Networks', TFT.RED, font, 1, nowrap=True)
    x = font["Height"]
    for net in nets:
        x=  x + 1 + font["Height"]
        ssid = str(net[0].decode("utf-8"))
        if (ssid == ''):
            ssid = 'No SSID'
        tft.text((0, x),ssid , TFT.GREEN, font, 1, nowrap=True)


def displayTemp():
    adcpin = 4
    sensor = ADC(adcpin)
    adc_value = sensor.read_u16()
    volt = (3.3/65535)*adc_value
    temperature = 27 - (volt - 0.706)/0.001721  

    font = sysfont.sysfont
    tft.fill(TFT.BLACK)
    tft.text((0, 0), 'Temperature', TFT.RED, font, 1, nowrap=True)
    x = font["Height"]
    tft.text((0, x), 'Core: ' + str(temperature) + 'C', TFT.GREEN, font, 1, nowrap=True)


if __name__ == "__main__":
    spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(6), mosi=Pin(7), miso=None)
    tft=TFT(spi,11,10,12)
    tft.rotation(1)
    tft.initr()
    tft.rgb(True)
    while True:
        showNetworks()
        time.sleep(5)
        displayTemp()
        time.sleep(5)

