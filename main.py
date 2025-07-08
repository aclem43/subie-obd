from lib.LCD_1inch28 import LCD_1inch28
from lib.Touch_CST816T import Touch_CST816T, Gesture_CST816T
from machine import ADC
import time

size = 240  # Size of the LCD in pixels (240x240 for 1.28 inch display)
center = size // 2  # Center point of the LCD


def getTextWidth(text, size=1):
    return len(text) * 8 * size


def getTextHeight(size=1):
    return 8 * size


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

        self.Touch = Touch_CST816T(mode=0, LCD=self.LCD)  # Initialize touch with mode 1

    def run(self):
        self.startUp()
        time.sleep(1)
        self.Touch.Set_Mode(0)  # Set touch to gesture mode
        self.pageDisplay("{:.2f}C".format(getTemp()), "12v", "Touch to start")
        while True:
            if self.Touch.getGesture() == Gesture_CST816T.UP:
                time.sleep(0.1)
                self.pageDisplay(
                    "{:.2f}C".format(getTemp()), "12v", "Touch to start", rst=True
                )

    def startUp(self):
        self.clear()
        text = "Subie OBD"
        width = getTextWidth(text, size=2)
        h = getTextHeight(size=2)
        self.LCD.write_text(
            text, center - width // 2, center - h // 2, size=2, color=self.LCD.red
        )
        self.LCD.write_text(
            "V" + self.version,
            center - getTextWidth("V" + self.version, size=1) // 2,
            center + getTextHeight(size=1) // 2 + h,
            size=1,
            color=self.LCD.white,
        )
        self.LCD.show()

    def pageDisplay(self, data1, data2, data3, rst=False):

        if rst:
            # only clear the old text not the whole screen
            self.LCD.fill_rect(
                0,
                center - getTextHeight(size=3) // 2,
                size,
                getTextHeight(size=3),
                self.LCD.black,
            )
            self.LCD.fill_rect(
                0,
                center - getTextHeight(size=2) // 2 + 8,
                size,
                getTextHeight(size=2),
                self.LCD.black,
            )
            self.LCD.fill_rect(
                0,
                center - getTextHeight(size=1) // 2 + 16,
                size,
                getTextHeight(size=1),
                self.LCD.black,
            )
            self.LCD.show()
        else:
            self.clear()

        y1 = center - getTextHeight(size=3)
        y2 = y1 + getTextHeight(size=3) + 8  # 8 pixels padding
        y3 = y2 + getTextHeight(size=2) + 8  # 8 pixels padding

        self.LCD.write_text(
            data1,
            center - getTextWidth(data1, size=3) // 2,
            y1,
            size=3,
            color=self.LCD.white,
        )
        self.LCD.write_text(
            data2,
            center - getTextWidth(data2, size=2) // 2,
            y2,
            size=2,
            color=self.LCD.white,
        )
        self.LCD.write_text(
            data3,
            center - getTextWidth(data3, size=1) // 2,
            y3,
            size=1,
            color=self.LCD.white,
        )

        self.LCD.show()

    def clear(self):
        self.LCD.fill(self.LCD.black)
        self.LCD.show()


if __name__ == "__main__":
    main = SubieOBD()
    main.run()  # Run the main applicatio
