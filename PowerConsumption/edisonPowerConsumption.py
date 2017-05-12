import math
from PowerConsumption.powerConsumptionModule import PowerConsumption

class EdisonPowerConsumption(PowerConsumption):

    def __init__(self, socketControl):
        self.sensibility = 122.1
        super().__init__(socketControl)

    def calculateRMS(self,result, length):
        return (math.sqrt(result / length))*3300/(self.sensibility*1650);
