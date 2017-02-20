import time, threading
from abc import ABC, abstractmethod

class ADataAcquisition(ABC, threading.Thread):
    result = 0
    readValue = 0
    countSamples = 0
    timestamp = time.time()

    def __init__(self, samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl):
        threading.Thread.__init__(self)
        self.samplesQueue = samplesQueue
        self.socketControl = socketControl
        self.adc = self.socketControl.adc
        self.samplesQueueSemaphore = samplesQueueSemaphore
        self.samplesQueueFlowControlSemaphore = samplesQueueFlowControlSemaphore

    @abstractmethod
    def addDAQSample(self):
        pass

    def run(self):
        while True:
            self.addDAQSample()