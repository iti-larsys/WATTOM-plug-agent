from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
from LEDFeedback.ledModule import LedController
from SocketControl.edisonControl import EdisonControl
from WebServer.app import app
import threading, time, queue
from Sending.sendingModule import DataSender

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
    powerCalculationThread = EdisonPowerConsumption(samplesQueue, samplesQueueLock,  processedSamplesQueue, processedSamplesQueueLock, socketControl)
    ledControlThread = LedController( 20, 14, 21)

    url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/plugs_events"
    url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/continuous_measuring"
    dataSender = DataSender(url1, url2)

    flaskThread = threading.Thread(target=runFlask)
    threads = [flaskThread, ledControlThread, powerCalculationThread,  dataAcquisitionThread]


    ##Starts the threads
    flaskThread.start() #Starts the webserver
    #Subscriver Threads
    ledControlThread.start()
    powerCalculationThread.start()
    powerCalculationThread.add(ledControlThread)
    powerCalculationThread.add(dataSender)

    dataAcquisitionThread.start()

    ##Waits fr all threads to finish
    for t in threads:
        t.join()