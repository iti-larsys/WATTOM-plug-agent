import math
from PowerConsumption.powerConsumptionModule import PowerConsumption

class EdisonPowerConsumption(PowerConsumption):

    def __init__(self, DAQSource):
        self.sensibility = 66
        super().__init__(DAQSource)

    def calculateRMS(self,result, length):
        return (math.sqrt(result / length)) * 3300 / (self.sensibility * 1650)