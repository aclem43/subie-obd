from st7735 import TFT
from st7735 import sysfont
from machine import SPI,Pin
import time
import math

def tftprinttest(font):
    tft.fill(TFT.BLACK);
    v = 30
    tft.text((0, v), "Huon", TFT.RED, font, 1, nowrap=True)
    v += font["Height"]
    tft.text((0, v), "is", TFT.YELLOW, font, 2, nowrap=True)
    v += font["Height"] * 2
    tft.text((0, v), "Gay!", TFT.GREEN, font, 5, nowrap=True)
    v += font["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, font, 5, nowrap=True)
    time.sleep_ms(1500)

def test_main():
    tftprinttest(sysfont.sysfont)
    time.sleep_ms(100)

if __name__ == "__main__":
    spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(6), mosi=Pin(7), miso=None)
    tft=TFT(spi,11,10,12)
    tft.initr()
    tft.rgb(True)
    test_main()
