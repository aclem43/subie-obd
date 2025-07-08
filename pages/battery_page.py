from utils import getTextWidth, getTextHeight, center
from sensors import getBattery


def battery_page(LCD, write_centered_text):
    voltage = getBattery()
    color = LCD.green if voltage > 12.0 else LCD.red
    y = 60
    y = write_centered_text(
        "Battery Voltage", y, size=2, color=LCD.white, max_width=200
    )
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
