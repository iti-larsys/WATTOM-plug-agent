from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
from LEDFeedback.ledModule import LedController
import threading, time, queue, mraa #TODO REMOVE MRAA

if __name__ == "__main__":
    mainVoltage = 230 # TODO Comes from a configuration file
    samplesQueue = queue.Queue(60)
    processedSamplesQueue = queue.Queue(60)
    samplesQueueLock = threading.Lock()
    processedSamplesQueueLock = threading.Lock()
    relay = mraa.Gpio(37)
    relay.dir(mraa.DIR_OUT)
    relay.write(1)

    dataAcquisitionThread= EdisonRead(samplesQueue,samplesQueueLock)
    #ledController = LedController()
    powerCalculationThread = EdisonPowerConsumption(mainVoltage, samplesQueue, samplesQueueLock,  processedSamplesQueue, processedSamplesQueueLock)
    ledControl = LedController( 20, 14, 21, processedSamplesQueue, processedSamplesQueueLock)
    threads = [dataAcquisitionThread,powerCalculationThread]

    ##Starts the threads
    ledControl.start()
    powerCalculationThread.start()
    dataAcquisitionThread.start()
    ##Waits fr all threads to finish
    for t in threads:
        t.join()



    #while True:
    #    dataAcquisition.addDAQSample()

    #    powerConsumption.getPower()
    #    startTime = time.time()
