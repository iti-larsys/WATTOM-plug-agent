import time, threading
from abc import ABC, abstractmethod
from PublishSubscriber import Publisher

class PowerConsumption(ABC, threading.Thread, Publisher):

    def __init__(self, mainVoltage, samplesQueue, samplesQueueLock,  processedSamplesQueue, processedSamplesQueueLock):
        threading.Thread.__init__(self)
        self.mainVoltage = mainVoltage
        self.samplesQueue = samplesQueue
        self.samplesQueueLock = samplesQueueLock
        self.processedSamplesQueue = processedSamplesQueue
        self.processedSamplesQueueLock = processedSamplesQueueLock

    def getPower(self):
        result = 0
        if not self.samplesQueue.empty():
            self.samplesQueueLock.acquire()
            samples = self.samplesQueue.get()
            self.samplesQueueLock.release()

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
            if (ampRMS <= 0.10):
               power = 0
               ampRMS = 0

            #Stores the samples in the processed sample queue
            self.processedSamplesQueueLock.acquire()
            self.processedSamplesQueue.put({'power': power, 'current': ampRMS, 'timestamp': str(samples["timestamp"])})
            #print("These are the processed samples: "+str(self.processedSamplesQueue) +  "this is my size" + str(self.processedSamplesQueue.qsize()))
            self.processedSamplesQueueLock.release()
        else:
            pass
            #print("I have nothing to do")
    @abstractmethod
    def calculateRMS(self,result, length):
        pass

    def run(self):
        while True:
            self.getPower()