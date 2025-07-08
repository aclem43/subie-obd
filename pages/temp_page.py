from utils import getTextWidth, getTextHeight, center
from sensors import getTemp
from config import TEMP_COLD, TEMP_GOOD, TEMP_HIGH


def temp_page(LCD):
    temp = getTemp()
    # Set color based on temperature thresholds
    if temp < TEMP_COLD:
        temp_color = LCD.blue  # Cold
    elif temp < TEMP_GOOD:
        temp_color = LCD.green  # Normal/Good
    elif temp < TEMP_HIGH:
        temp_color = LCD.yellow if hasattr(LCD, "yellow") else LCD.white  # High
    else:
        temp_color = LCD.red  # Danger

    LCD.write_text(
        "Coolant Temp",
        center - getTextWidth("Coolant Temp", 2) // 2,
        60,
        size=2,
        color=LCD.white,
    )
    LCD.write_text(
        "{:.1f} C".format(temp),
        center - getTextWidth("{:.1f} C".format(temp), 3) // 2,
        100,
        size=3,
        color=temp_color,
    )
    LCD.write_text(
        "Swipe Up/Down",
        center - getTextWidth("Swipe Up/Down", 1) // 2,
        200,
        size=1,
        color=LCD.white,
    )
    LCD.show()


def temp_partial_update(LCD):
    temp = getTemp()
    if temp < TEMP_COLD:
        temp_color = LCD.blue
    elif temp < TEMP_GOOD:
        temp_color = LCD.green
    elif temp < TEMP_HIGH:
        temp_color = LCD.yellow if hasattr(LCD, "yellow") else LCD.white
    else:
        temp_color = LCD.red

    LCD.fill_rect(
        0,
        100,
        240,  # or use size if imported
        getTextHeight(size=3),
        LCD.black,
    )
    LCD.write_text(
        "{:.1f} C".format(temp),
        center - getTextWidth("{:.1f} C".format(temp), 3) // 2,
        100,
        size=3,
        color=temp_color,
    )
    LCD.show()
