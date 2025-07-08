from config import DISPLAY_SIZE, DISPLAY_CENTER

size = DISPLAY_SIZE
center = DISPLAY_CENTER


def getTextWidth(text, size=1):
    return len(text) * 8 * size


def getTextHeight(size=1):
    return 8 * size
