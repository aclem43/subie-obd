from utils import getTextWidth, getTextHeight, center, wrap_text
from sensors import getBattery
from config import BATTERY_GOOD, BATTERY_MIN, BATTERY_MAX
from lib.colours import Colour


def battery_page(LCD, write_centered_text):
    voltage = getBattery()
    if voltage < BATTERY_MIN:
        status = "Battery Low"
        color = Colour.red
    elif voltage > BATTERY_MAX:
        status = "Battery High"
        color = Colour.yellow
    else:
        status = "Battery Safe"
        color = Colour.green

    # Use wrap_text for header/status
    header_lines = wrap_text(status, size=2, max_width=200)
    y = 60
    for line in header_lines:
        LCD.write_text(
            line,
            center - getTextWidth(line, 2) // 2,
            y,
            size=2,
            color=Colour.white,
        )
        y += getTextHeight(2) + 4

    LCD.write_text(
        "{:.2f} V".format(voltage),
        center - getTextWidth("{:.2f} V".format(voltage), 3) // 2,
        y,
        size=3,
        color=color,
    )
    LCD.write_text(
        "Swipe Up/Down",
        center - getTextWidth("Swipe Up/Down", 1) // 2,
        200,
        size=1,
        color=Colour.white,
    )
    LCD.show()


def battery_partial_update(LCD, write_centered_text):
    voltage = getBattery()
    # Determine status and color
    if voltage < BATTERY_MIN:
        color = Colour.red
    elif voltage > BATTERY_MAX:
        color = Colour.yellow
    else:
        color = Colour.green

    y = 60
    y = write_centered_text(
        "Battery Safe", y, size=2, color=Colour.white, max_width=200, dry_run=True
    )
    # Clear only the area where the voltage value is drawn
    LCD.fill_rect(
        center - getTextWidth("{:.2f} V".format(voltage), 3) // 2 - 4,
        y,
        getTextWidth("{:.2f} V".format(voltage), 3) + 8,
        getTextHeight(size=3),
        Colour.black,
    )
    LCD.write_text(
        "{:.2f} V".format(voltage),
        center - getTextWidth("{:.2f} V".format(voltage), 3) // 2,
        y,
        size=3,
        color=color,
    )
    LCD.show()
