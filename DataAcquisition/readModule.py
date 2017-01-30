import time
from abc import ABC, abstractmethod

class ADataAcquisition(ABC):
    result = 0
    readValue = 0
    countSamples = 0
    timestamp = time.time()

    def __init__(self):
        pass

    @abstractmethod
    def getDAQSamples_OUT(self):
        pass

    @abstractmethod
    def addDAQSample(self):
        pass