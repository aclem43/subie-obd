from lib.colours import Colour

# Display settings
DISPLAY_SIZE = 240
DISPLAY_CENTER = DISPLAY_SIZE // 2
BACKGROUND_COLOR = Colour.black
TEXT_COLOR = Colour.white

# Debounce and timing
DEBOUNCE_MS = 500
PAGE_UPDATE_INTERVAL_MS = 150
PAGE_FULL_UPDATE_INTERVAL_MS = 5000

# Sensor simulation/dev mode
DEV_MODE = False

# Temperature thresholds (Celsius)
TEMP_COLD = 60
TEMP_GOOD = 90
TEMP_HIGH = 105

# Battery voltage thresholds (Volts)
BATTERY_GOOD = 12.0
BATTERY_MIN = 11.0
BATTERY_MAX = 15.0
