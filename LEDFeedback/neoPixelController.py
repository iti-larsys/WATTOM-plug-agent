import time
import argparse
from NeoPixelAnimationWorker import NeoPixelAnimationWorker
from neopixel import *

# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class NeoPixelController():
    # parser = None
    # args   = []
    strip      = None
    running    = True
    __instance = None
    worker1    = None
   # x = mraa.Gpio(20)
    selected = False

    def __new__(cls):
        """
        Create a Singleton
        :return:
        """
        if NeoPixelController.__instance is None:
            NeoPixelController.__instance = object.__new__(cls)
       # AddressableLedController.i2c = mraa.I2c(6)
       # AddressableLedController.i2c.address(8)
        return NeoPixelController.__instance

    def startup(self):
        # Process arguments
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
        self.args = self.parser.parse_args()

        # Create NeoPixel object with appropriate configuration.
        NeoPixelController.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        NeoPixelController.strip.begin()
        print("Neo pixel initialized!!")
        #self.simpleTarget(Color(255, 0, 0))
	self.colorWipe(Color(0,0,0),10)

    # Define functions which animate LEDs in various ways.
    def colorWipe(self,color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        print("wipping modafaca")
        for i in range(NeoPixelController.strip.numPixels()):
            NeoPixelController.strip.setPixelColor(i, color)
            NeoPixelController.strip.show()
            time.sleep(wait_ms/1000.0)
		
    def stop(self):
	if(NeoPixelController.worker1!=None):
	    NeoPixelController.worker1.stopAnimation()

    def changeDelay(self, d):
        if(NeoPixelController.worker1!=None):
            NeoPixelController.worker1.changeDelay(d)

    def select(self,led):
        if(NeoPixelController.worker1!=None):
            NeoPixelController.worker1.animate(led)

    def initialize_leds(self, leds, relay_state, person_near,socket, delay,background):
        if(NeoPixelController.worker1==None):
            NeoPixelController.worker1 = NeoPixelAnimationWorker(NeoPixelController.strip,leds,socket,delay,background)
            NeoPixelController.worker1.start()
        else:
            NeoPixelController.worker1.stopAnimation()
            NeoPixelController.worker1 = NeoPixelAnimationWorker(NeoPixelController.strip,leds,socket,delay,background)
            NeoPixelController.worker1.start()

        # Define functions which animate LEDs in various ways.
    def simpleTarget(self,color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        print("wipping modafaca")
        NeoPixelController.worker1 = NeoPixelAnimationWorker(NeoPixelController.strip,1)
        NeoPixelController.worker1.start()
        #NeoPixelController.strip.setPixelColor(0, color)
        # while NeoPixelController.running:
        #     for i in range(0, NeoPixelController.strip.numPixels()-1):
        #         NeoPixelController.strip.setPixelColor(i+1, color)
        #         NeoPixelController.strip.setPixelColor(i, Color(0,0,0))
        #         NeoPixelController.strip.show()
        #         print(NeoPixelController.strip.getPixels())
        #         time.sleep(1)
        #     NeoPixelController.strip.setPixelColor( NeoPixelController.strip.numPixels()-1, Color(0,0,0))
