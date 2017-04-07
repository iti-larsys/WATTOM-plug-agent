import mraa, struct

class AddressableLedController():

    __instance = None

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
        data = bytearray([4,personState])
        self.changeLeds(data)

    def changeDelay(self, delay):
        data = bytearray([5,delay])
        self.changeLeds(data)

    def changeLed(self, ledID):
        data = bytearray([6,ledID])
        self.changeLeds(data)

    def initializeLeds(self, orientation, delay, ledID, relayState, personState):
        print("mandei inicializar")
        # first byte at 0 indicates, that we are sending the initial config, second indicates the kind of movement
        data = bytearray([0,orientation, delay, ledID, relayState, personState])
        self.changeLeds(data)

    def changeLeds(self, data):
        print(data)
        AddressableLedController.i2c.write(data)
        print("Enviei")