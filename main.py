from lib.LCD_1inch28 import LCD_1inch28
from lib.Touch_CST816T import Touch_CST816T, Gesture_CST816T
import time
from utils import getTextWidth, getTextHeight, size, center
from sensors import getTemp, getBattery
from config import DEBOUNCE_MS, PAGE_UPDATE_INTERVAL_MS, PAGE_FULL_UPDATE_INTERVAL_MS
from lib.colours import Colour
from pages.combined_page import combined_page, combined_partial_update
from pages.temp_page import temp_page, temp_partial_update
from pages.battery_page import battery_page, battery_partial_update
from pages.info_page import info_page


class SubieOBD(object):
    def __init__(self):
        self.version = "0.7.1"
        self.LCD = LCD_1inch28()
        self.LCD.set_bl_pwm(65535)
        self.Touch = Touch_CST816T(mode=0, LCD=self.LCD)
        self.pages = [
            lambda: temp_page(self.LCD),
            lambda: battery_page(self.LCD, self.write_centered_text),
            lambda: info_page(self.LCD, self.version),
            lambda: combined_page(self.LCD, self.write_centered_text),
        ]
        self.page_index = 0
        self.last_full_update = 0

    def run(self):
        self.startUp()
        time.sleep(1)
        self.Touch.Set_Mode(0)
        self.show_page()
        last_gesture = None
        last_time = time.ticks_ms()
        debounce_ms = DEBOUNCE_MS

        while True:
            gesture = self.Touch.getGesture()
            now = time.ticks_ms()
            if gesture in (Gesture_CST816T.UP, Gesture_CST816T.DOWN):
                if (
                    gesture != last_gesture
                    or time.ticks_diff(now, last_time) > debounce_ms
                ):
                    if gesture == Gesture_CST816T.UP:
                        self.page_index = (self.page_index + 1) % len(self.pages)
                        self.show_page()
                    elif gesture == Gesture_CST816T.DOWN:
                        self.page_index = (self.page_index - 1) % len(self.pages)
                        self.show_page()
                    last_gesture = gesture
                    last_time = now
            else:
                last_gesture = None
                self.show_page()
            time.sleep_ms(PAGE_UPDATE_INTERVAL_MS)

    def startUp(self):
        self.clear()
        text = "Subie OBD"
        width = getTextWidth(text, size=2)
        h = getTextHeight(size=2)
        self.LCD.write_text(
            text,
            center - width // 2,
            center - h // 2,
            size=2,
            color=Colour.red,
        )
        self.LCD.write_text(
            "V" + self.version,
            center - getTextWidth("V" + self.version, size=1) // 2,
            center + getTextHeight(size=1) // 2 + h,
            size=1,
            color=Colour.white,
        )
        self.LCD.show()

    def get_battery_value_y(self):
        y = 60
        y = self.write_centered_text(
            "Battery Voltage",
            y,
            size=2,
            color=Colour.white,
            max_width=200,
            dry_run=True,
        )
        return y

    def write_centered_text(
        self, text, y, size=1, color=None, max_width=30, dry_run=False
    ):
        if color is None:
            color = Colour.white
        text_width = getTextWidth(text, size)
        if text_width <= max_width:
            if not dry_run:
                self.LCD.write_text(
                    text,
                    center - text_width // 2,
                    y,
                    size=size,
                    color=color,
                )
            return y + getTextHeight(size) + 4
        else:
            mid = len(text) // 2
            split_idx = text.rfind(" ", 0, mid)
            if split_idx == -1:
                split_idx = mid
            line1 = text[:split_idx].strip()
            line2 = text[split_idx:].strip()
            y = self.write_centered_text(line1, y, size, color, max_width, dry_run)
            y = self.write_centered_text(line2, y, size, color, max_width, dry_run)
            return y

    def show_page(self):
        if not hasattr(self, "_last_page_index"):
            self._last_page_index = -1

        if self.page_index != self._last_page_index:
            self.clear()
            self.pages[self.page_index]()
            self._last_page_index = self.page_index
            self.last_full_update = time.ticks_ms()
        current_time = time.ticks_ms()
        if (current_time - self.last_full_update) > PAGE_FULL_UPDATE_INTERVAL_MS:
            self.clear()
            self.pages[self.page_index]()
            self.last_full_update = current_time
        else:
            if self.page_index == 0:
                temp_partial_update(self.LCD)
            elif self.page_index == 1:
                battery_partial_update(self.LCD, self.write_centered_text)
            elif self.page_index == 3:
                combined_partial_update(self.LCD, self.write_centered_text)

    def clear(self):
        self.LCD.fill(Colour.black)
        self.LCD.show()


if __name__ == "__main__":
    main = SubieOBD()
    main.run()
