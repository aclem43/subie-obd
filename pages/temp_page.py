from utils import getTextWidth, getTextHeight, center, wrap_text
from sensors import getTemp
from config import TEMP_COLD, TEMP_GOOD, TEMP_HIGH
from lib.colours import Colour
from icons.coolantTemp import draw_coolant_icon


def temp_page(LCD):
    temp = getTemp()
    # Set color based on temperature thresholds
    if temp < TEMP_COLD:
        temp_color = Colour.blue  # Cold
    elif temp < TEMP_GOOD:
        temp_color = Colour.green  # Normal/Good
    elif temp < TEMP_HIGH:
        temp_color = Colour.yellow
    else:
        temp_color = Colour.red  # Danger

    # Use wrap_text for header
    header_lines = wrap_text("Coolant Temp", size=2, max_width=200)
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
        "{:.1f} C".format(temp),
        center - getTextWidth("{:.1f} C".format(temp), 3) // 2,
        100,
        size=3,
        color=temp_color,
    )

    # Draw coolant icon below the value
    icon_x = center
    icon_y = 140
    draw_coolant_icon(LCD, icon_x, icon_y, temp_color)

    LCD.write_text(
        "Swipe Up/Down",
        center - getTextWidth("Swipe Up/Down", 1) // 2,
        200,
        size=1,
        color=Colour.white,
    )
    LCD.show()


def temp_partial_update(LCD):
    temp = getTemp()
    if temp < TEMP_COLD:
        temp_color = Colour.blue
    elif temp < TEMP_GOOD:
        temp_color = Colour.green
    elif temp < TEMP_HIGH:
        temp_color = Colour.yellow
    else:
        temp_color = Colour.red

    LCD.fill_rect(
        0,
        100,
        240,  # or use size if imported
        getTextHeight(size=3),
        Colour.black,
    )
    LCD.write_text(
        "{:.1f} C".format(temp),
        center - getTextWidth("{:.1f} C".format(temp), 3) // 2,
        100,
        size=3,
        color=temp_color,
    )
    LCD.show()
