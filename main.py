from lib.LCD_1inch28 import LCD_1inch28
from lib.Touch_CST816T import Touch_CST816T
from machine import ADC
import time

size = 240  # Size of the LCD in pixels (240x240 for 1.28 inch display)
center = size // 2  # Center point of the LCD


def getTemp():
    adcpin = 4
    sensor = ADC(adcpin)
    adc_value = sensor.read_u16()
    volt = (3.3 / 65535) * adc_value
    temperature = 27 - (volt - 0.706) / 0.001721

    return temperature


class SubieOBD(object):
    def __init__(self):
        self.version = "0.4"
        self.LCD = LCD_1inch28()
        self.LCD.set_bl_pwm(65535)  # Set backlight brightness

        self.Touch = Touch_CST816T(mode=1, LCD=self.LCD)  # Initialize touch with mode 1

    def run(self):
        self.startUp()

    def startUp(self):
        self.clear()
        text = "Subie OBD"
        width = self.getTextWidth(text, size=2)
        h = self.getTextHeight(size=2)
        self.LCD.write_text(
            text, center - width // 2, center - h // 2, size=2, color=self.LCD.red
        )
        self.LCD.write_text(
            "V" + self.version,
            center - self.getTextWidth("V" + self.version, size=1) // 2,
            center + self.getTextHeight(size=1) // 2 + h,
            size=1,
            color=self.LCD.white,
        )
        self.LCD.show()

    def getTextWidth(self, text, size=1):
        return len(text) * 8 * size

    def getTextHeight(self, size=1):
        return 8 * size

    def clear(self):
        self.LCD.fill(self.LCD.black)
        self.LCD.show()


if __name__ == "__main__":
    main = SubieOBD()
    main.run()  # Run the main applicatio
