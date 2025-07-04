
from lib.LCD_1inch28 import LCD_1inch28
from lib.Touch_CST816T import Touch_CST816T

size = 240  # Size of the LCD in pixels (240x240 for 1.28 inch display)
center = size // 2  # Center point of the LCD

class SubieOBD(object):
    def __init__(self):
        self.version = '0.4'
        self.LCD = LCD_1inch28()
        self.LCD.set_bl_pwm(65535)  # Set backlight brightness

        self.Touch = Touch_CST816T(mode=1, LCD=self.LCD)  # Initialize touch with mode 1

    def run(self):
        self.startUp()
        
    def startUp(self):
        self.clear()
        self.LCD.write_text("Subie OBD", center - self.getTextWidth("Subie OBD", size=2) // 2, center - self.getTextHeight(size=2) // 2, size=2, color=self.LCD.white)
        self.LCD.show()

    def getTextWidth(self, text, size=1):
        return len(text) * 8 * size
    
    def getTextHeight(self, size=1):
        return 8 * size


    def clear(self):
        self.LCD.fill(self.LCD.black)
        self.LCD.show()

if __name__=='__main__':
    main = SubieOBD()
    main.run()  # Run the main application
