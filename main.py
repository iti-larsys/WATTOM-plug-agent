from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
from LEDFeedback.ledModule import LedController
from SocketControl.edisonControl import EdisonControl
from WebServer.app import app
import threading, time, queue, mraa #TODO REMOVE MRAA


mainVoltage = 230 # TODO Comes from a configuration file
socketControl = EdisonControl(mainVoltage)

def runFlask():
    app.run("0.0.0.0", debug=True, use_reloader=False)

if __name__ == "__main__":
    samplesQueue = queue.Queue(60)
    processedSamplesQueue = queue.Queue(60)
    samplesQueueLock = threading.Lock()
    processedSamplesQueueLock = threading.Lock()

    socketControl.initializeRelay()

    dataAcquisitionThread= EdisonRead(samplesQueue,samplesQueueLock, socketControl)
    #ledController = LedController()
    powerCalculationThread = EdisonPowerConsumption(samplesQueue, samplesQueueLock,  processedSamplesQueue, processedSamplesQueueLock, socketControl)
    ledControl = LedController( 20, 14, 21, processedSamplesQueue, processedSamplesQueueLock)
    flaskThread = threading.Thread(target=runFlask)
    threads = [dataAcquisitionThread,powerCalculationThread, flaskThread]

    ##Starts the threads
    flaskThread.start()
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
