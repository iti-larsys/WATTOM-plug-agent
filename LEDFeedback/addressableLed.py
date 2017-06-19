from threading import Timer

import mraa
import struct

from PublishSubscriber.Subscriber import Subscriber


def interrupt_handler(self, gpio):
    print("pin " + str(gpio.getPin(True)) + " = " + str(gpio.read()))


# noinspection PyMethodMayBeStatic
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

    def change_power(self, power):
        # Done once
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(power) & 0xFFFFFFFF)
        data = bytearray([1, y1, y2, y3, y4])  # ,power])
        self.change_leds(data)

    def change_relay_state(self, relay_state):
        data = bytearray([2, relay_state])
        self.change_leds(data)

    '''
    def changeOrientation(self, orientation):
        data = bytearray([3,orientation])
        self.changeLeds(data)
    '''

    def person_change(self, person_state):
        print("person " + str(person_state))
        data = bytearray([4, person_state])
        self.change_leds(data)

    def change_delay(self, delay):
        print("Delay " + str(delay))
        # Done once
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(delay) & 0xFFFFFFFF)
        data = bytearray([3, y1, y2, y3, y4])
        self.change_leds(data)

    def initialize_leds(self, leds, relay_state, person_near, delay):
        # first byte at 0 indicates, that we are sending the initial config, second indicates the kind of movement
        # Done once
        print(leds)
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(delay) & 0xFFFFFFFF)
        data = bytearray([0, relay_state, person_near, len(leds), y1, y2, y3, y4])
        self.change_leds(data)
        for led in leds:
            data = bytearray([4])
            data.append(int(led["position"]))
            data.append(int(led["orientation"]))
            data.append(int(led["red"]))
            data.append(int(led["green"]))
            data.append(int(led["blue"]))
            self.change_leds(data)

    def change_leds(self, data):
        print(data)
        AddressableLedController.i2c.write(data)
        print("Enviei")

    def make_selected_feedback(self, selected_led):
        data = bytearray([6, int(selected_led)])
        self.change_leds(data)
        # self.selected = True
        r = Timer(5.0, self.stop_selected_feedback, [int(selected_led)])
        r.start()

    def stop_selected_feedback(self, selected_led):
        data = bytearray([7, selected_led])
        self.change_leds(data)
        # self.selected = False

    def stop_movement(self):
        data = bytearray([8])
        self.change_leds(data)

    def update(self, data):
        if not self.selected:
            self.change_power(data["power"])
