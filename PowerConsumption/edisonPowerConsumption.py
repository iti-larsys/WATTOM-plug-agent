import math
from PowerConsumption.powerConsumptionModule import PowerConsumption

class EdisonPowerConsumption(PowerConsumption):

    def __init__(self, socketControl, dataProcessingSemaphore, powerSamples):
        self.sensibility = 66
        super().__init__(socketControl, dataProcessingSemaphore, powerSamples)

    def calculateRMS(self,result, length):
        return (math.sqrt(result / length))*3300/(self.sensibility*1650);
