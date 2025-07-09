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
