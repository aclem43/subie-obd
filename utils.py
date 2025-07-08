size = 240  # LCD size
center = size // 2


def getTextWidth(text, size=1):
    return len(text) * 8 * size


def getTextHeight(size=1):
    return 8 * size
