from utils import getTextWidth, getTextHeight, wrap_text, center
from sensors import getBattery, getTemp
from config import (
    BATTERY_MIN,
    BATTERY_MAX,
    TEMP_COLD,
    TEMP_GOOD,
    TEMP_HIGH,
    BACKGROUND_COLOR,
)
from lib.colours import Colour
from icons.coolantTemp import draw_coolant_icon
from lib.LCD_1inch28 import LCD_1inch28


def combined_page(LCD, write_centered_text):
    """
    Draws a combined page with battery and coolant temperature information.
    """
    voltage = getBattery()
    if voltage < BATTERY_MIN:
        color = Colour.red
    elif voltage > BATTERY_MAX:
        color = Colour.yellow
    else:
        color = Colour.green

    # Write centered text for header/status
    y = 60
    y = write_centered_text(
        "Battery Voltage", y, size=2, color=Colour.white, max_width=200
    )
    y = write_centered_text(
        "{:.2f} V".format(voltage), y, size=3, color=color, max_width=200
    )

    temp = getTemp()
    if temp < TEMP_COLD:
        temp_color = Colour.blue
    elif temp < TEMP_GOOD:
        temp_color = Colour.green
    elif temp < TEMP_HIGH:
        temp_color = Colour.yellow
    else:
        temp_color = Colour.red

    # Write centered text for coolant temperature
    y = write_centered_text(
        "Coolant Temp", y + 20, size=2, color=Colour.white, max_width=200
    )
    y = write_centered_text(
        "{:.1f} C".format(temp), y, size=3, color=temp_color, max_width=200
    )

    LCD.write_text(
        "Swipe Up/Down",
        center - getTextWidth("Swipe Up/Down", 1) // 2,
        200,
        size=1,
        color=Colour.white,
    )
    # Show the changes on the LCD
    LCD.show()


def combined_partial_update(LCD: LCD_1inch28, write_centered_text):
    voltage = getBattery()
    if voltage < BATTERY_MIN:
        color = Colour.red
    elif voltage > BATTERY_MAX:
        color = Colour.yellow
    else:
        color = Colour.green

    y = 60

    y += getTextHeight(2) + getTextHeight(2) + 8
    LCD.rect(0, y, 240, getTextHeight(3), BACKGROUND_COLOR, True)
    y = write_centered_text(
        "{:.2f} V".format(voltage), y, size=3, color=color, max_width=200
    )
    temp = getTemp()
    if temp < TEMP_COLD:
        temp_color = Colour.blue
    elif temp < TEMP_GOOD:
        temp_color = Colour.green
    elif temp < TEMP_HIGH:
        temp_color = Colour.yellow
    else:
        temp_color = Colour.red

    y += getTextHeight(2) + 4 + 20
    LCD.rect(0, y, 240, getTextHeight(3), BACKGROUND_COLOR, True)
    y = write_centered_text(
        "{:.1f} C".format(temp), y, size=3, color=temp_color, max_width=200
    )

    LCD.show()
