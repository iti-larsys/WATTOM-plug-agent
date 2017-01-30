from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
import _thread, time

if __name__ == "__main__":
    dataAcquisition = EdisonRead()
    #ledController = LedController()
    powerConsumption = EdisonPowerConsumption(dataAcquisition)
    startTime = time.time()
    while True:
        dataAcquisition.addDAQSample()

        powerConsumption.getPower()
        startTime = time.time()
