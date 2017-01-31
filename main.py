from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
import threading, time, queue

if __name__ == "__main__":

    samplesQueue = queue.Queue(60)
    processedSamplesQueue = queue.Queue(60)
    samplesQueueLock = threading.Lock()
    processedSamplesQueueLock = threading.Lock()

    dataAcquisitionThread= EdisonRead(samplesQueue,samplesQueueLock)
    #ledController = LedController()
    powerCalculationThread = EdisonPowerConsumption()
    startTime = time.time()
    while True:
        dataAcquisition.addDAQSample()

        powerConsumption.getPower()
        startTime = time.time()
