import RPi.GPIO as GPIO
import time
 
relay_pin = 23
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin,GPIO.OUT)
GPIO.setwarnings(False)

class PiSocketController():

    status = False

    def __new__(cls):
        """
        Create a Singleton
        :return:
        """
        if PiSocketController.__instance is None:
            PiSocketController.__instance = object.__new__(cls)
       # AddressableLedController.i2c = mraa.I2c(6)
       # AddressableLedController.i2c.address(8)
        return PiSocketController.__instance

    def ON(self):
        print("Controlling socket yo!!")
        print ("Settin low - LED ON")
        GPIO.output (relay_pin,GPIO.HIGH)
        #time.sleep(2)
        self.status = True

    def OFF(self):
        #set low
        print ("Setting low - LED OFF")
        GPIO.output (relay_pin,GPIO.LOW)
        #time.sleep(2)
        self.status = False