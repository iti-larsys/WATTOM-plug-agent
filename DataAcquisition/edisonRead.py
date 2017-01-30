from DataAcquisition.readModule import ADataAcquisition
from libs.Spark_ADC import Adc

class EdisonRead(ADataAcquisition):

    def __init__(self):
        self.initializeAdc()
        self.samples = []
        self.adcZero = self.calibration()

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

    def getDAQSamples_OUT(self):
        return self.samples

    def addDAQSample(self):
        while True:
            self.samples.append(self.adc.adc_read() - self.adcZero)

    def calibration(self):
        averageVoltage = 0
        for i in range(5000):
            averageVoltage += self.adc.adc_read()
        averageVoltage /= 5000
        return round(averageVoltage)