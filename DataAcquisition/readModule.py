import time, threading
from abc import ABC, abstractmethod

class ADataAcquisition(ABC, ):
    result = 0
    readValue = 0
    countSamples = 0
    timestamp = time.time()

    def __init__(self, socketControl):
        self.socketControl = socketControl
        self.adc = self.socketControl.adc

    @abstractmethod
    def addDAQSample(self):
        pass