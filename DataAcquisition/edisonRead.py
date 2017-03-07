from DataAcquisition.readModule import ADataAcquisition
from libs.Spark_ADC import Adc
import time, csv

class EdisonRead(ADataAcquisition):

    def __init__(self, socketControl):
        super().__init__(socketControl)
        self.samples = []
        self.samplesNum = 500
        self.sampleTime = 0.1
        self.sampleInterval = self.sampleTime / self.samplesNum
        self.adcZero = self.socketControl.calibrate()


    def addDAQSample(self):
        print("Reading function")
        self.samples = []
        startTime = time.time()
        while time.time() - startTime < 1:
            # Centers read value at zero
            readValue =  self.adc.adc_read() - self.adcZero
            self.samples.append(readValue)
        #print(str(self.samples))
        return {"samples": self.samples, "timestamp": time.time()}
