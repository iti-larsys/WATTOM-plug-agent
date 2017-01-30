import mraa
import time

class LedController:

    def __init__(self, pinRed, pinBlue, pinGreen):
        self.pwmRed = mraa.Pwm(pinRed)
        self.pwmGreen = mraa.Pwm(pinGreen)
        self.pwmBlue = mraa.Pwm(pinBlue)
        #Enables the pin's
        self.pwmRed.enable(True)
        self.pwmGreen.enable(True)
        self.pwmBlue.enable(True)


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

    def changeLeds(self,power):
        """
        Changes the led color according with the value
        :param power:
        :return:
        """
        if power >= 1000:
            self.redLed()
        elif power > 300 and power < 1000:
            self.yellowLed()
            #print("Yellow")
        else:
            #print("Green")
            self.greenLed()

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