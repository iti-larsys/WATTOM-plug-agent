import mraa, struct, time
from PublishSubscriber.Subscriber import Subscriber
from threading import Timer

def interruptHandler(self,gpio):
   print("pin " + str(gpio.getPin(True)) + " = " + str(gpio.read()))

class AddressableLedController(Subscriber):

    __instance = None
    x = mraa.Gpio(20)
    selected = False

    def __new__(cls):
        if AddressableLedController.__instance is None:
            AddressableLedController.__instance = object.__new__(cls)
        AddressableLedController.i2c = mraa.I2c(6)
        AddressableLedController.i2c.address(8)
        return AddressableLedController.__instance

    def changePower(self, power):
        # Done once
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(power) & 0xFFFFFFFF)
        data = bytearray([1,y1,y2,y3,y4])#,power])
        self.changeLeds(data)

    def changeRelayState(self, relayState):
        data = bytearray([2,relayState])
        self.changeLeds(data)

    '''
    def changeOrientation(self, orientation):
        data = bytearray([3,orientation])
        self.changeLeds(data)
    '''
    def personChange(self, personState):
        print("person " + str(personState))
        data = bytearray([4,personState])
        self.changeLeds(data)

    def changeDelay(self, delay):
        print ("Delay " + str(delay))
        # Done once
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(delay) & 0xFFFFFFFF)
        data = bytearray([3, y1, y2, y3, y4])
        self.changeLeds(data)

    def initializeLeds(self, leds, relayState, personNear, delay):
        # first byte at 0 indicates, that we are sending the initial config, second indicates the kind of movement
        # Done once
        print(leds)
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(delay) & 0xFFFFFFFF)
        data = bytearray([0, relayState, personNear, len(leds), y1, y2, y3, y4])
        self.changeLeds(data)
        for led in leds:
            data = bytearray([4])
            data.append(int(led["position"]))
            data.append(int(led["orientation"]))
            data.append(int(led["red"]))
            data.append(int(led["green"]))
            data.append(int(led["blue"]))
            self.changeLeds(data)

    def changeLeds(self, data):
        print(data)
        AddressableLedController.i2c.write(data)
        print("Enviei")

    def makeSelectedFeedback(self, selectedLed):
        data = bytearray([6, int(selectedLed)])
        self.changeLeds(data)
        #self.selected = True
        r = Timer(5.0, self.stopSelectedFeedback, [int(selectedLed)])
        r.start()

    def stopSelectedFeedback(self, selectedLed):
        data = bytearray([7, selectedLed])
        self.changeLeds(data)
        #self.selected = False

    def stopMovement(self):
        data = bytearray([8])
        self.changeLeds(data)

    def update(self, data):
        if not self.selected:
            self.changePower(data["power"])

