import time, threading
from abc import ABC, abstractmethod
from PublishSubscriber.Publisher import Publisher

class PowerConsumption(Publisher):

    def __init__(self, socketControl, dataProcessingSemaphore, powerSamples):
        self.socketControl = socketControl
        self.mainVoltage = self.socketControl.voltage
        self.dataProcessingSemaphore = dataProcessingSemaphore
        self.powerSamples = powerSamples

    def getPower(self, samples):
        result = 0
        print ("Going to calculate power")

        for sample in samples["samples"]:
            result += sample * sample
        # Calculates RMS current. 3300 = 3.3V/mV. 1650 is the max ADC count i can get with 3.3V
        ampRMS = self.calculateRMS(result,len(samples["samples"]))
        #print("Calculate power")
        # Calculates Power as an integer
        #TODO: How to pass main voltage
        power = (ampRMS * self.mainVoltage)
        #print(round(power))
        # Ignores some of the noise
        print("power " + str(power))
        print("RMS " + str(ampRMS))
        if (ampRMS <= 0.10):
            power = 0
            ampRMS = 0

        #Stores the samples in the processed sample queue
        #self.processedSamplesQueueLock.acquire()
        #self.processedSamplesQueue.put({'power': power, 'current': ampRMS, 'timestamp': str(samples["timestamp"])})
        #print("These are the processed samples: "+str(self.processedSamplesQueue) +  "this is my size" + str(self.processedSamplesQueue.qsize()))
        print("power " + str(power))
        print("RMS " + str(ampRMS))
        self.powerSamples.append({'power': power, 'current': ampRMS, 'timestamp': str(samples["timestamp"])})
        self.dataProcessingSemaphore.release()
        #self.processedSamplesQueueLock.release()

    @abstractmethod
    def calculateRMS(self,result, length):
        pass
