from abc import ABC, abstractmethod

class SocketControl(ABC):

    @abstractmethod
    def changeRelay(self):
        pass

    def setVoltage(self, voltage):
        self.voltage = voltage

    @abstractmethod
    def calibrate(self):
        pass