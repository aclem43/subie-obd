from st7735 import TFT
class Widget:
    def __init__(self, title, key) -> None:
        self.title = title
        self.key = key

        self.lowColor = TFT.BLUE
        self.defaultColor = TFT.GREEN
        self.warningColor = TFT.YELLOW
        self.dangerColor = TFT.ORANGE
        self.criticalColor = TFT.RED

        self.lowValue = 0
        self.defaultValue = 1
        self.warningValue = 2
        self.dangerValue = 3
        self.criticalValue = 4


    def setColorValues(self, low, default, warning, danger, critical):
        self.lowValue = low
        self.defaultValue = default
        self.warningValue = warning
        self.dangerValue = danger
        self.criticalValue = critical

    def setColors(self, low, default, warning, danger, critical):
        self.lowColor = low
        self.defaultColor = default
        self.warningColor = warning
        self.dangerColor = danger
        self.criticalColor = critical

    

    def getColor(self, value):
        if value <= self.lowValue:
            return self.lowColor
        elif value <= self.defaultValue:
            return self.defaultColor
        elif value <= self.warningValue:
            return self.warningColor
        elif value <= self.dangerValue:
            return self.dangerColor
        else:
            return self.criticalColor


    def getTitle(self):
        return self.title
    
    def getKey(self):
        return self.key

    def setTitle(self, title):
        self.title = title
    
    def setKey(self, key):
        self.key = key