import math
from PowerConsumption.powerConsumptionModule import PowerConsumption

class EdisonPowerConsumption(PowerConsumption):

    def __init__(self,mainVoltage, samplesQueue, samplesQueueLock,  processedSamplesQueue, processedSamplesQueueLock):
        self.sensibility = 66
        super().__init__(mainVoltage, samplesQueue, samplesQueueLock,  processedSamplesQueue, processedSamplesQueueLock)

    def calculateRMS(self,result, length):
        return (math.sqrt(result / length)) * 3300 / (self.sensibility * 1650)