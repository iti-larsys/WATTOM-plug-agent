from DataAcquisition.readModule import ADataAcquisition
from libs.Spark_ADC import Adc
import time

class EdisonRead(ADataAcquisition):

    def __init__(self, samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl):
        super().__init__(samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl)
        self.samples = []
        self.samplesNum = 500
        self.sampleTime = 0.1
        self.sampleInterval = self.sampleTime / self.samplesNum
        self.adcZero = self.socketControl.calibrate()


    def addDAQSample(self):
        print("Reading function")
        self.samples = []
        startTime = time.time() - self.sampleInterval
        i = 0
        while i < self.samplesNum:
            # To give some time before reading again
            if ((time.time() - startTime) >= self.sampleInterval):
                # Centers read value at zero
                readValue = self.adc.adc_read() - self.adcZero
                self.samples.append(readValue)
                startTime += self.sampleInterval
                i+=1
            else:
                print("making time on reading")
        samplesToQueue = {"samples": self.samples, "timestamp": time.time()}
        #print("These are my samples: " + str(samplesToQueue))

        #TODO: ATTENTION!!! WHEN IT'S FULL IT WILL BLOCK THE PROCESS
        if self.samplesQueueSemaphore.acquire(blocking=False):
            #print("adding samples to queue")
            self.samplesQueue.append(samplesToQueue)
            #print("samples added to queue")
            self.samplesQueueFlowControlSemaphore.release()
        else:
            print("loosing samples")

        #print("I'm Here #2")
