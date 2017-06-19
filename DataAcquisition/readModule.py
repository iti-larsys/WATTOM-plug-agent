import time
from abc import ABC, abstractmethod


class ADataAcquisition(ABC, ):
    result = 0
    readValue = 0
    countSamples = 0
    timestamp = time.time()

    def __init__(self, socket_control):
        self.socketControl = socket_control
        self.adc = self.socketControl.adc

    @abstractmethod
    def add_d_acq_sample(self):
        pass
