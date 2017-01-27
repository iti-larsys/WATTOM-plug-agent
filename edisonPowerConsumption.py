import math
from powerConsumptionModule import PowerConsumption

class EdisonPowerConsumption(PowerConsumption):

    def __init__(self):
        self.sensibility = 66

    def calculateRMS(self,result, length):
        return (math.sqrt(result / length)) * 3300 / (self.sensibility * 1650)