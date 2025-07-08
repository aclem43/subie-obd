from utils import getTextWidth, center, wrap_text, getTextHeight
from config import DEV_MODE


def info_page(LCD, version):
    LCD.fill(LCD.black)
    # Use wrap_text for header
    header_lines = wrap_text("Subie OBD Info", size=2, max_width=200)
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
        f"Version: {version}",
        center - getTextWidth(f"Version: {version}", 1) // 2,
        100,
        size=1,
        color=LCD.green,
    )
    LCD.write_text(
        f"Dev Mode: {'ON' if DEV_MODE else 'OFF'}",
        center - getTextWidth(f"Dev Mode: {'ON' if DEV_MODE else 'OFF'}", 1) // 2,
        130,
        size=1,
        color=LCD.yellow if DEV_MODE else LCD.white,
    )
    LCD.write_text(
        "Future Data:",
        center - getTextWidth("Future Data:", 1) // 2,
        170,
        size=1,
        color=LCD.white,
    )
    LCD.write_text(
        "-------------------",
        center - getTextWidth("-------------------", 1) // 2,
        185,
        size=1,
        color=LCD.white,
    )
    LCD.show()
