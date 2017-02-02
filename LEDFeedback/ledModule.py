import mraa
import threading
from PublishSubscriber import Subscriber

class LedController(threading.Thread, Subscriber):

    def __init__(self, pinRed, pinBlue, pinGreen, processedSamplesQueue, processedSamplesQueueLock):
        threading.Thread.__init__(self)
        self.pwmRed = mraa.Pwm(pinRed)
        self.pwmGreen = mraa.Pwm(pinGreen)
        self.pwmBlue = mraa.Pwm(pinBlue)
        #Enables the pin's
        self.pwmRed.enable(True)
        self.pwmGreen.enable(True)
        self.pwmBlue.enable(True)
        self.processedSamplesQueue = processedSamplesQueue
        self.processedSamplesQueueLock = processedSamplesQueueLock
        # STATE CONSTANTS
        self.CONST_STATE_GREEN = "green"
        self.CONST_STATE_YELLOW = "yellow"
        self.CONST_STATE_RED = "red"
        #Leds State
        self.currentState = self.CONST_STATE_GREEN
        self.pastState = self.CONST_STATE_GREEN
        #The color min value
        self.CONST_GRADIENT = 0.10

        self.pinRed = 0.0000
        self.pinBlue = 0.0000
        self.pinGreen = 0.0000

    def led(self,valueGreen, valueRed):
        """
        Led color change
        :param valueGreen:
        :param valueRed:
        :return:
        """
        self.pwmGreen.write(valueGreen)
        self.pwmRed.write(valueRed)

    def changeState(self, power):
        """
        Will make the current state var according with the power received.
        :param power:
        :return:
        """
        self.pastState = self.currentState
        if power >= 1000:
            self.currentState = self.CONST_STATE_RED
        elif power > 300 and power < 1000:
            self.currentState = self.CONST_STATE_YELLOW
        else:
            self.currentState = self.CONST_STATE_GREEN


    def colorChange(self):
        if self.currentState == self.CONST_STATE_RED:
            if self.pastState == self.CONST_STATE_RED:
                self.led(0.0000,1.0000)
                self.pinRed = 1.0000
                self.pinGreen = 0.0000
            elif self.pastState == self.CONST_STATE_YELLOW:
                self.pinGreen = self.pinGreen + self.CONST_GRADIENT
                self.led(0.0000, 1.0000)
                if self.pinGreen <= 0.0000 and self.pinRed >= 1.0000:
                    self.pastState = self.CONST_STATE_RED
            else:
                self.pinRed = self.pinRed + self.CONST_GRADIENT
                self.pinGreen = self.pinGreen - self.CONST_GRADIENT
                self.led(self.pinGreen, self.pinRed)
                if self.pinGreen <= 0.0000 and self.pinRed >= 1.0000:
                    self.pastState = self.CONST_STATE_RED


        if self.currentState == self.CONST_STATE_YELLOW:
            if self.pastState == self.CONST_STATE_YELLOW:
                self.led(1.0000,1.0000)
                self.pinRed = 1.0000
                self.pinGreen = 1.0000
            elif self.pastState == self.CONST_STATE_RED:
                self.pinGreen = self.pinGreen + self.CONST_GRADIENT
                self.led(self.pinGreen, 1.0000)
                if self.pinGreen >= 1.0000 and self.pinRed >= 1.0000:
                    self.pastState = self.CONST_STATE_YELLOW
            else :
                self.pinRed = self.pinRed + self.CONST_GRADIENT
                self.led(1.0000, self.pinRed)
                if (self.pinGreen >= 1.0000 and self.pinRed >= 1.0000):
                    self.pastState = self.CONST_STATE_YELLOW


        if self.currentState == self.CONST_STATE_GREEN:
            if self.pastState == self.CONST_STATE_GREEN:
                self.led(1.0000,0.0000) #TODO PROBABLY NEED TO TI CHANFE THE GREEN VALUE AN NOT CHANGE IT SO NEED TO READ FROM THE PIN
                self.pinRed = 0.0000
                self.pinGreen = 1.0000
            elif self.pastState == self.CONST_STATE_RED:
                self.pinRed = self.pinRed - self.CONST_GRADIENT
                self.pinGreen = self.pinGreen + self.CONST_GRADIENT
                self.led(self.pinGreen,self.pinRed)
                if self.pinGreen >= 1.0000 and self.pinRed <= 0.0000:
                    self.pastState = self.CONST_STATE_GREEN
            else:
                self.pinRed = self.pinRed - self.CONST_GRADIENT
                self.led(1.0000,self.pinRed)
                if self.pinGreen >= 1.0000 and self.pinRed <= 0.0000:
                    self.pastState = self.CONST_STATE_GREEN

    def update(self,data):
        print("Subscriber LED " + data)

    def run(self):
        """
        Changes the led color according with the value
        :param power:
        :return:
        """
        ##Right after startup subscrive to a publisher



        #Starts the plug with green power
        while True:
            power = 20
            self.changeState(self, power)
            self.colorChange()

"""
if __name__ == "__main__":
    ledContoller = LedController(20,14,21)

    while True:
        power = 0
        while power <= 4400:
            if ledContoller.currentState == ledContoller.CONST_NO_STATE:
                ledContoller.greenLedTransition()
                ledContoller.currentState = ledContoller.CONST_STATE_GREEN
"""