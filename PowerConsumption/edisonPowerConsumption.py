import math
from PowerConsumption.powerConsumptionModule import PowerConsumption

class EdisonPowerConsumption(PowerConsumption):

    def __init__(self, samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl):
        self.sensibility = 66
        super().__init__(samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl)

    def calculateRMS(self,result, length):
        return (math.sqrt(result / length)) * 3300 / (self.sensibility * 1650)