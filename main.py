from st7735 import TFT
from st7735 import sysfont
from machine import SPI,Pin,ADC
import network
import time
import _thread
import random

def showNetworks():
    font = sysfont.sysfont
    wlan = network.WLAN(network.STA_IF)
    nets = wlan.scan()
    tft.fill(TFT.BLACK)
    tft.text((0, 0), 'Networks', TFT.RED, font, 1, nowrap=True)
    x = font["Height"]
    for net in nets:
        x=  x + 1 + font["Height"]
        ssid = str(net[0].decode("utf-8"))
        if (ssid == ''):
            ssid = 'No SSID'
        tft.text((0, x),ssid , TFT.GREEN, font, 1, nowrap=True)


def displayTemp():
    adcpin = 4
    sensor = ADC(adcpin)
    adc_value = sensor.read_u16()
    volt = (3.3/65535)*adc_value
    temperature = 27 - (volt - 0.706)/0.001721  

    font = sysfont.sysfont
    tft.fill(TFT.BLACK)
    tft.text((0, 0), 'Temperature', TFT.RED, font, 1, nowrap=True)
    x = font["Height"]
    tft.text((0, x), 'Core: ' + str(temperature) + 'C', TFT.GREEN, font, 1, nowrap=True)


class SubieObd:
    def __init__(self,tft:TFT, widgets = False) -> None: 
        self.version = '0.2'

        self.tft = tft
        self.starting = False
        self.mainpage = False

        self.widgets = []
        if widgets == False:
            self.defaultWidgets()
        
        self.data = {}
        self.updatedData = False

        self.font = sysfont.sysfont
        self.fontHeight = self.font["Height"]
        self.fontHeight2 = self.fontHeight * 2
        self.fontHeight3 = self.fontHeight * 3
        self.fontHeight4 = self.fontHeight * 4
        self.fontHeight5 = self.fontHeight * 5

        self.connected = False
        self.sLock = _thread.allocate_lock()


    def clearScreen(self):
        tft.fill(TFT.BLACK)

    def startUpScreen(self):
        self.clearScreen()
        self.tft.text((0, 0), 'Subie OBD', TFT.RED, self.font, 3, nowrap=True)
        self.tft.text((0, self.fontHeight3), 'Starting up', TFT.GREEN, self.font, 2, nowrap=True)
        self.tft.text((0, 128 - self.fontHeight), 'Version: ' + self.version, TFT.GREEN, self.font, 1, nowrap=True)


    def startUpAnimation(self):
        while self.isStarting():
            self.tft.fillrect((0, self.fontHeight3*2), ( 160,  self.fontHeight3), TFT.BLACK)
            self.tft.text((0, self.fontHeight3*2), '...', TFT.GREEN, self.font, 2, nowrap=True)
            time.sleep(0.5)
            self.tft.fillrect((0, self.fontHeight3*2), ( 160,  self.fontHeight3), TFT.BLACK)
            self.tft.text((0, self.fontHeight3*2), '..', TFT.GREEN, self.font, 2, nowrap=True)
            time.sleep(0.5)
        _thread.exit()

    def start(self):
       self.startUpScreen()
       self.starting = True
       _thread.start_new_thread(self.startUpAnimation,())
       self.connect()
       if self.connected:
           self.starting = False
           self.clearScreen()
           self.mainpage = True
           self.mainPageLoop()

    
    def isStarting (self):
        return self.starting

    def connect(self):
        time.sleep(1)
        self.connected = True

    def mainPageLoop(self):
        self.displayWidgets()
        self.updatedData = False
        while self.mainpage:
            self.updateData()
            if self.updatedData != True:
                time.sleep_ms(250)
                continue
            self.displayData()
            self.updatedData = False
            time.sleep_ms(250)

    def displayWidgets(self):
        self.clearScreen()
        self.tft.text((0, 0), 'Subie OBD v' + self.version, TFT.RED, self.font, 1, nowrap=True)

        widgetHeight = self.fontHeight + 2

        if (self.widgets == []):
            self.tft.text((0, widgetHeight), "No Widgets Set", TFT.RED, self.font, 2, nowrap=True)
            widgetHeight += self.fontHeight2 + 1

        if (self.connected == False):
            self.tft.text((0, widgetHeight), "Not Connected", TFT.RED, self.font, 2, nowrap=True)
            widgetHeight += self.fontHeight2 + 1

        for widget in self.widgets:
            self.tft.text((0, widgetHeight), widget['title']+': ', TFT.GREEN, self.font, 2, nowrap=True)
            widgetHeight += self.fontHeight2 + 1

    def displayData(self):
        self.tft.text((0, 0), 'Subie OBD v' + self.version, TFT.RED, self.font, 1, nowrap=True)

        widgetHeight = self.fontHeight + 2

        if (self.widgets == []):
            self.tft.text((0, widgetHeight), "No Widgets Set", TFT.RED, self.font, 2, nowrap=True)
            widgetHeight += self.fontHeight2 + 1

        if (self.connected == False):
            self.tft.text((0, widgetHeight), "Not Connected", TFT.RED, self.font, 2, nowrap=True)
            widgetHeight += self.fontHeight2 + 1

        for widget in self.widgets:
            dat = 'Error'
            try:
                dat = self.data[widget['key']]
            except KeyError:
                dat = 'N/A'
            x = (len(widget['title']) + 2) * self.font["Width"] * 2
            self.tft.fillrect((x, widgetHeight), (160, self.fontHeight2), TFT.BLACK)
            self.tft.text((x, widgetHeight),  str(dat) , TFT.GREEN, self.font, 2, nowrap=True)
            widgetHeight += self.fontHeight2 + 1

        

    def updateData(self):
        self.data = {'speed':  random.randint(0,120), 'rpm': random.randint(0,6000), 'coolant': random.randint(0,140), 'voltage': random.randint(0,14)}
        self.updatedData = True

    def defaultWidgets(self):
        self.addWidget('Speed', 'speed')
        self.addWidget('RPM', 'rpm')
        self.addWidget('Coolant', 'coolant')
        self.addWidget('Voltage', 'voltage')


    def addWidget(self, title, key):
        self.widgets.append({'title': title, 'key': key})
    

if __name__ == "__main__":
    spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
              sck=Pin(6), mosi=Pin(7), miso=None)
    tft=TFT(spi,11,10,12)
    tft.rotation(1)
    tft.initr()
    tft.rgb(True)

    subie = SubieObd(tft)
    subie.start()
