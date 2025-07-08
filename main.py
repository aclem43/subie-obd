from lib.LCD_1inch28 import LCD_1inch28
from lib.Touch_CST816T import Touch_CST816T, Gesture_CST816T
import time
from utils import getTextWidth, getTextHeight, size, center
from sensors import getTemp, getBattery
from config import DEBOUNCE_MS, PAGE_UPDATE_INTERVAL_MS, ARC_UPDATE_RATE

# Import page functions
from pages.temp_page import temp_page, temp_partial_update
from pages.battery_page import battery_page, battery_partial_update
from pages.info_page import info_page


class SubieOBD(object):
    def __init__(self):
        self.version = "0.5"
        self.LCD = LCD_1inch28()
        self.LCD.set_bl_pwm(65535)
        self.Touch = Touch_CST816T(mode=0, LCD=self.LCD)
        self.pages = [
            lambda: temp_page(self.LCD),
            lambda: battery_page(self.LCD, self.write_centered_text),
            lambda: info_page(self.LCD, self.version),  # Add info page as last page
        ]
        self.page_index = 0
        self.arc_update_counter = 0
        self.arc_update_rate = ARC_UPDATE_RATE

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
                last_gesture = None  # Reset if no gesture
                self.show_page()
            time.sleep_ms(PAGE_UPDATE_INTERVAL_MS)  # reduce flicker

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

    def get_battery_value_y(self):
        # Calculates the y position for the voltage value, matching both initial and update draws
        y = 60
        y = self.write_centered_text(
            "Battery Voltage",
            y,
            size=2,
            color=self.LCD.white,
            max_width=200,
            dry_run=True,
        )
        return y

    def write_centered_text(
        self, text, y, size=1, color=None, max_width=30, dry_run=False
    ):
        """
        Writes text centered at y. If it doesn't fit, splits into two lines.
        If dry_run is True, only calculates and returns the next y without drawing.
        """
        if color is None:
            color = self.LCD.white
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
            return y + getTextHeight(size) + 4  # 4px padding
        else:
            # Split text in half (at nearest space)
            mid = len(text) // 2
            split_idx = text.rfind(" ", 0, mid)
            if split_idx == -1:
                split_idx = mid
            line1 = text[:split_idx].strip()
            line2 = text[split_idx:].strip()
            y = self.write_centered_text(line1, y, size, color, max_width, dry_run)
            y = self.write_centered_text(line2, y, size, color, max_width, dry_run)
            return y

    def page_battery(self):
        voltage = getBattery()
        color = self.LCD.green if voltage > 12.0 else self.LCD.red
        y = 60
        y = self.write_centered_text(
            "Battery Voltage", y, size=2, color=self.LCD.white, max_width=200
        )
        self.LCD.write_text(
            "{:.2f} V".format(voltage),
            center - getTextWidth("{:.2f} V".format(voltage), 3) // 2,
            y,
            size=3,
            color=color,
        )
        self.LCD.write_text(
            "Swipe Up/Down",
            center - getTextWidth("Swipe Up/Down", 1) // 2,
            200,
            size=1,
            color=self.LCD.white,
        )
        self.LCD.show()

    def show_page(self):
        # Only redraw the page if the index has changed
        if not hasattr(self, "_last_page_index"):
            self._last_page_index = -1  # Initialize on first call

        if self.page_index != self._last_page_index:
            self.clear()
            self.pages[self.page_index]()
            self._last_page_index = self.page_index
        else:
            # Only update the dynamic value, not the whole page
            if self.page_index == 0:
                # Update only the temperature value
                temp_partial_update(self.LCD)
            elif self.page_index == 1:
                # Update only the battery value
                battery_partial_update(self.LCD, self.write_centered_text)

    def page_temp(self):
        temp = getTemp()
        # Set color based on temperature thresholds
        if temp < 60:
            temp_color = self.LCD.blue  # Cold
        elif temp < 90:
            temp_color = self.LCD.green  # Normal/Good
        elif temp < 105:
            temp_color = self.LCD.yellow  # High (use yellow or brown)
        else:
            temp_color = self.LCD.red  # Danger

        self.LCD.write_text(
            "Coolant Temp",
            center - getTextWidth("Coolant Temp", 2) // 2,
            60,
            size=2,
            color=self.LCD.white,
        )
        self.LCD.write_text(
            "{:.1f} C".format(temp),
            center - getTextWidth("{:.1f} C".format(temp), 3) // 2,
            100,
            size=3,
            color=temp_color,
        )
        self.LCD.write_text(
            "Swipe Up/Down",
            center - getTextWidth("Swipe Up/Down", 1) // 2,
            200,
            size=1,
            color=self.LCD.white,
        )
        self.LCD.show()

    def clear(self):
        self.LCD.fill(self.LCD.black)
        self.LCD.show()


if __name__ == "__main__":
    main = SubieOBD()
    main.run()
