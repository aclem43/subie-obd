from utils import getTextWidth, getTextHeight
from lib.colours import Colour
from sensors import getTimeSinceBoot


def time_page(LCD, write_centered_text):
    """
    Display the time page on the LCD.
    """

    center = LCD.width // 2

    current_time = format_time(getTimeSinceBoot())

    write_centered_text(
        "Time Since Boot",
        60,
        size=2,
        color=Colour.white,
        max_width=200,
    )
    write_centered_text(
        current_time,
        100,
        size=2,
        color=Colour.white,
        max_width=200,
    )

    LCD.show()


def time_partial_update(LCD, write_centered_text):
    current_time = format_time(getTimeSinceBoot())
    LCD.rect(0, 100, 240, getTextHeight(2) + 8, Colour.black, True)
    write_centered_text(
        current_time,
        100,
        size=2,
        color=Colour.white,
        max_width=200,
    )
    LCD.show()


def format_time(seconds):
    """
    Format the time in seconds into a human-readable string.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"
