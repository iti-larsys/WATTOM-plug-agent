import mraa
import time
import threading

class LedController(threading.Thread):

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

    def greenLed(self):
        """
        Green color definition
        :return:
        """
        self.pwmGreen.write(0.5000)
        self.pwmRed.write(0.0000)
        self.pwmBlue.write(0.0000)

    def yellowLed(self):
        """
        Yellow color definition
        :return:
        """
        self.pwmGreen.write(0.5000)
        self.pwmRed.write(0.5000)
        self.pwmBlue.write(0.0000)

    def redLed(self):
        """
        Red Color definition
        :return:
        """
        self.pwmGreen.write(0.0000)
        self.pwmRed.write(1.0000)
        self.pwmBlue.write(0.0000)

    def run(self):
        """
        Changes the led color according with the value
        :param power:
        :return:
        """
        self.greenLed()
        while True:
            if not self.processedSamplesQueue.empty():
                self.processedSamplesQueueLock.acquire()
                power = self.processedSamplesQueue.get()["power"]
                self.processedSamplesQueueLock.release()
                if power >= 1000:
                    self.redLed()
                elif power > 300 and power < 1000:
                    self.yellowLed()
                    #print("Yellow")
                else:
                    self.greenLed()
            else:
                print("Don't need to change LED's")

"""
if __name__ == "__main__":
    ledContoller = LedController(20,14,21)

    while True:
        power = 0
        while power <= 4400:
            ledContoller.changeLeds(power)
            power = power + 50
            print("THe power is : " + str(power))
"""