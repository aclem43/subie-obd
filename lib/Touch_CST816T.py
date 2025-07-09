from machine import Pin, I2C, Timer
import framebuf
import time
from lib.LCD_1inch28 import LCD_1inch28
from lib.pins import LCDPin
from lib.colours import Colour


# Touch drive  触摸驱动
class Touch_CST816T(object):
    def __init__(self, LCD: LCD_1inch28, address=0x15, mode=0, i2c_num=1):
        self.LCD = LCD
        if self.LCD is None:
            raise ValueError("LCD cannot be None")
        self._bus = I2C(
            i2c_num, scl=Pin(LCDPin.I2C_SCL), sda=Pin(LCDPin.I2C_SDA), freq=400_000
        )  # Initialize I2C 初始化I2C
        self._address = address  # Set slave address  设置从机地址
        self.int = Pin(LCDPin.I2C_INT, Pin.IN, Pin.PULL_UP)
        self.tim = Timer()
        self.rst = Pin(LCDPin.I2C_RST, Pin.OUT)
        self.Reset()
        bRet = self.WhoAmI()
        if bRet:
            print("Success:Detected CST816T.")
            Rev = self.Read_Revision()
            print("CST816T Revision = {}".format(Rev))
            self.Stop_Sleep()
        else:
            print("Error: Not Detected CST816T.")
            return None
        self.Mode = mode
        self.Gestures = "None"
        self.Flag = self.Flgh = self.l = 0
        self.X_point = self.Y_point = 0
        self.int.irq(handler=self.Int_Callback, trigger=Pin.IRQ_FALLING)

    def _read_byte(self, cmd):
        rec = self._bus.readfrom_mem(int(self._address), int(cmd), 1)
        return rec[0]

    def _read_block(self, reg, length=1):
        rec = self._bus.readfrom_mem(int(self._address), int(reg), length)
        return rec

    def _write_byte(self, cmd, val):
        self._bus.writeto_mem(int(self._address), int(cmd), bytes([int(val)]))

    def WhoAmI(self):
        if (0xB5) != self._read_byte(0xA7):
            return False
        return True

    def Read_Revision(self):
        return self._read_byte(0xA9)

    # Stop sleeping  停止睡眠
    def Stop_Sleep(self):
        self._write_byte(0xFE, 0x01)

    # Reset  复位
    def Reset(self):
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)

    # Set mode  设置模式

    def Set_Mode(self, mode, callback_time=10, rest_time=5):
        """
        Sets the operating mode of the CST816T touch controller.
        Args:
            mode (int): The desired mode to set.
                - 0: Gestures mode
                - 1: Point mode
                - 2: Mixed mode
            callback_time (int, optional): Time in milliseconds for callback interval. Default is 10.
            rest_time (int, optional): Time in milliseconds for rest interval. Default is 5.
        """
        # mode = 0 gestures mode
        # mode = 1 point mode
        # mode = 2 mixed mode
        if mode == 1:
            self._write_byte(0xFA, 0x41)

        elif mode == 2:
            self._write_byte(0xFA, 0x71)

        else:
            self._write_byte(0xFA, 0x11)
            self._write_byte(0xEC, 0x01)

    # Get the coordinates of the touch  获取触摸的坐标
    def get_point(self):
        xy_point = self._read_block(0x03, 4)

        x_point = ((xy_point[0] & 0x0F) << 8) + xy_point[1]
        y_point = ((xy_point[2] & 0x0F) << 8) + xy_point[3]

        self.X_point = x_point
        self.Y_point = y_point

    def getGesture(self):
        g = None
        if self.Gestures != None:
            g = self.Gestures
            self.Gestures = None
        return g

    # Gesture  手势
    def Touch_Gesture(self):
        self.Mode = 0
        self.Set_Mode(self.Mode)
        self.LCD.write_text("Gesture test", 70, 90, 1, Colour.black)
        self.LCD.write_text("Complete as prompted", 35, 120, 1, Colour.black)
        self.LCD.show()
        time.sleep(1)
        self.LCD.fill(Colour.white)
        while self.Gestures != 0x01:
            self.LCD.fill(Colour.white)
            self.LCD.write_text("UP", 100, 110, 3, Colour.black)
            self.LCD.show()

        while self.Gestures != 0x02:
            self.LCD.fill(Colour.white)
            self.LCD.write_text("DOWN", 70, 110, 3, Colour.black)
            self.LCD.show()

        while self.Gestures != 0x03:
            self.LCD.fill(Colour.white)
            self.LCD.write_text("LEFT", 70, 110, 3, Colour.black)
            self.LCD.show()

        while self.Gestures != 0x04:
            self.LCD.fill(Colour.white)
            self.LCD.write_text("RIGHT", 60, 110, 3, Colour.black)
            self.LCD.show()

        while self.Gestures != 0x0C:
            self.LCD.fill(Colour.white)
            self.LCD.write_text("Long Press", 40, 110, 2, Colour.black)
            self.LCD.show()

        while self.Gestures != 0x0B:
            self.LCD.fill(Colour.white)
            self.LCD.write_text("Double Click", 25, 110, 2, Colour.black)
            self.LCD.show()

    def Int_Callback(self, pin):
        if self.Mode == 0:
            self.Gestures = self._read_byte(0x01)

        elif self.Mode == 1:
            self.Flag = 1
            self.get_point()

    def Timer_callback(self, t):
        self.l += 1
        if self.l > 100:
            self.l = 50


class Gesture_CST816T:
    UP = 0x01
    DOWN = 0x02
    LEFT = 0x03
    RIGHT = 0x04
    LONG_PRESS = 0x0C
    DOUBLE_CLICK = 0x0B
