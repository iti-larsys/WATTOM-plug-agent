from DataAcquisition.readModule import ADataAcquisition
from libs.Spark_ADC import Adc
import time

class EdisonRead(ADataAcquisition):

    def __init__(self, samplesQueue, samplesQueueLock):
        super().__init__(samplesQueue, samplesQueueLock)
        self.initializeAdc()
        self.adcZero = self.calibration()
        self.samples = []
        self.samplesNum = 500
        self.sampleTime = 0.1
        self.sampleInterval = self.sampleTime / self.samplesNum


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


    def addDAQSample(self):
        self.samples = []
        startTime = time.time() - self.sampleInterval
        for i in range (self.samplesNum):
            # To give some time before reading again
            if ((time.time() - startTime) >= self.sampleInterval):
                # Centers read value at zero
                readValue = self.adc.adc_read() - self.adcZero
                self.samples.append(readValue)
                startTime += self.sampleInterval
        samplesToQueue = {"samples": self.samples, "timestamp": time.time()}
        #print("These are my samples: " + str(samplesToQueue))
        self.samplesQueueLock.acquire()
        self.samplesQueue.put(samplesToQueue)
        self.samplesQueueLock.release()
        #print("I'm Here #2")

    def calibration(self):
        averageVoltage = 0
        for i in range(5000):
            averageVoltage += self.adc.adc_read()
        averageVoltage /= 5000
        return round(averageVoltage)
