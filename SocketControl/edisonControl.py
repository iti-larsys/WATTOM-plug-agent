from SocketControl.socketControl import SocketControl
from LEDFeedback.addressableLed import AddressableLedController
from libs.Spark_ADC import Adc
import mraa

class EdisonControl(SocketControl):

    def __init__(self, voltage):
        self.voltage = voltage
        self.initializeAdc()
        self.relay = mraa.Gpio(37)
        self.relay.dir(mraa.DIR_OUT)
        self.ledControl = AddressableLedController()

    def changeRelay(self):
        if self.relay.read():
            self.relay.write(0)
            self.ledController.changeRelayState(0)
            return False
        else:
            self.relay.write(1)
            self.ledController.changeRelayState(1)
            return True

    def initializeRelay(self):
        self.relay.write(1)
        #self.ledController.changeRelayState(1)

    def calibrate(self):
        averageVoltage = 0
        for i in range(5000):
            averageVoltage += self.adc.adc_read()
        averageVoltage /= 5000
        return round(averageVoltage)

    def initializeAdc(self):
        ain0_operational_status = 0b0
        ain0_input_multiplexer_configuration = 0b100
        ain0_programmable_gain_amplifier_configuration = 0b001
        ain0_device_operating_mode = 0b0
        ain0_data_rate = 0b100
        ain0_comparator_mode = 0b0
        ain0_compulator_polarity = 0b0
        ain0_latching_comparator = 0b0
        ain0_comparator_queue_and_disable = 0b11

        self.adc = Adc()
        self.adc.set_config_command(
            ain0_operational_status,
            ain0_input_multiplexer_configuration,
            ain0_programmable_gain_amplifier_configuration,
            ain0_device_operating_mode,
            ain0_data_rate,
            ain0_comparator_mode,
            ain0_compulator_polarity,
            ain0_latching_comparator,
            ain0_comparator_queue_and_disable
        )
