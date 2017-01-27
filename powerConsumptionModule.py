import time
from abc import ABC, abstractmethod

class PowerConsumption(ABC):

    def __init__(self):
        self.mainVoltage = 230

    def getPower(self,samples):
        result = 0
        for sample in samples:
            result += sample * sample
        # Calculates RMS current. 3300 = 3.3V/mV. 1650 is the max ADC count i can get with 3.3V
        ampRMS = self.calculateRMS(result,samples.length)

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