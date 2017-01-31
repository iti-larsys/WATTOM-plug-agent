import time, threading
from abc import ABC, abstractmethod

class PowerConsumption(ABC, threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.mainVoltage = 230

    def getPower(self):
        result = 0
        for sample in self.DAQSource.getDAQSamples_OUT():
            result += sample * sample
        # Calculates RMS current. 3300 = 3.3V/mV. 1650 is the max ADC count i can get with 3.3V
        ampRMS = self.calculateRMS(result,len(self.DAQSource.getDAQSamples_OUT()))
        print("Calculate power")
        # Calculates Power as an integer
        #TODO: How to pass main voltage
        power = (ampRMS * self.mainVoltage)
        print(round(power))
        # Ignores some of the noise
        if (ampRMS <= 0.10):
           power = 0
           ampRMS = 0
        return {'power': power, 'current': ampRMS, 'timestamp': str(time.time())}

    @abstractmethod
    def calculateRMS(self,result, length):
        pass
