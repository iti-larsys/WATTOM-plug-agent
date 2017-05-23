import mraa, struct
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

    def changeOrientation(self, orientation):
        data = bytearray([3,orientation])
        self.changeLeds(data)

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
        data = bytearray([5, y1, y2, y3, y4])
        self.changeLeds(data)

    def changeLed(self, ledID):
        data = bytearray([6,ledID])
        self.changeLeds(data)

    def initializeLeds(self, orientation, ledID, delay, relayState, personState):
        # first byte at 0 indicates, that we are sending the initial config, second indicates the kind of movement
        # Done once
        print ("Delay " + str(delay))
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(delay) & 0xFFFFFFFF)
        data = bytearray([0,orientation, ledID, relayState, personState, y1, y2, y3, y4])
        self.changeLeds(data)

    def changeLeds(self, data):
        print(data)
        AddressableLedController.i2c.write(data)
        print("Enviei")

    def makeSelectedFeedback(self):
        data = bytearray([6, 1])
        self.changeLeds(data)
        self.selected = True
        r = Timer(10.0, self.stopSelectedFeedback)
        r.start()

    def stopSelectedFeedback(self):
        data = bytearray([6, 0])
        self.changeLeds(data)
        self.selected = False

    def update(self, data):
        if not self.selected:
            self.changePower(data["power"])

