from utils import getTextWidth, getTextHeight, center, wrap_text
from sensors import getTemp
from config import TEMP_COLD, TEMP_GOOD, TEMP_HIGH


def draw_coolant_icon(LCD, x, y, color):
    """
    Draws a simple coolant temperature icon (thermometer with waves) at (x, y).
    """
    # Thermometer bulb
    LCD.ellipse(x, y + 16, 6, 6, color, True)
    # Thermometer stem
    LCD.fill_rect(x - 2, y - 12, 4, 28, color)
    # Thermometer top
    LCD.ellipse(x, y - 12, 4, 4, color, True)
    # Waves (coolant)
    LCD.line(x - 10, y + 24, x + 10, y + 24, color)
    LCD.line(x - 8, y + 28, x + 8, y + 28, color)
    LCD.line(x - 6, y + 32, x + 6, y + 32, color)


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

    # Use wrap_text for header
    header_lines = wrap_text("Coolant Temp", size=2, max_width=200)
    y = 60
    for line in header_lines:
        LCD.write_text(
            line,
            center - getTextWidth(line, 2) // 2,
            y,
            size=2,
            color=LCD.white,
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
