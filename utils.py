from config import DISPLAY_SIZE, DISPLAY_CENTER

size = DISPLAY_SIZE
center = DISPLAY_CENTER


def getTextWidth(text, size=1):
    return len(text) * 8 * size


def getTextHeight(size=1):
    return 8 * size


def wrap_text(text, size=1, max_width=120):
    """
    Splits text into a list of lines so each line fits within max_width.
    Returns a list of lines.
    """
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = (current_line + " " + word).strip()
        if getTextWidth(test_line, size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines
