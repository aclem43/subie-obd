from utils import getTextWidth, getTextHeight, center
from sensors import getBattery
from config import BATTERY_GOOD, BATTERY_MIN, BATTERY_MAX


def battery_page(LCD, write_centered_text):
    voltage = getBattery()
    # Determine status and color
    if voltage < BATTERY_MIN:
        status = "Battery Low"
        color = LCD.red
    elif voltage > BATTERY_MAX:
        status = "Battery High"
        color = LCD.yellow if hasattr(LCD, "yellow") else LCD.white
    else:
        status = "Battery Safe"
        color = LCD.green

    y = 60
    y = write_centered_text(status, y, size=2, color=LCD.white, max_width=200)
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
        color=LCD.white,
    )
    LCD.show()


def battery_partial_update(LCD, write_centered_text):
    voltage = getBattery()
    # Determine status and color
    if voltage < BATTERY_MIN:
        color = LCD.red
    elif voltage > BATTERY_MAX:
        color = LCD.yellow if hasattr(LCD, "yellow") else LCD.white
    else:
        color = LCD.green

    y = 60
    y = write_centered_text(
        "Battery Safe", y, size=2, color=LCD.white, max_width=200, dry_run=True
    )
    # Clear only the area where the voltage value is drawn
    LCD.fill_rect(
        center - getTextWidth("{:.2f} V".format(voltage), 3) // 2 - 4,
        y,
        getTextWidth("{:.2f} V".format(voltage), 3) + 8,
        getTextHeight(size=3),
        LCD.black,
    )
    LCD.write_text(
        "{:.2f} V".format(voltage),
        center - getTextWidth("{:.2f} V".format(voltage), 3) // 2,
        y,
        size=3,
        color=color,
    )
    LCD.show()
