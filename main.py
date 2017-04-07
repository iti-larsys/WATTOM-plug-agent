from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
#from LEDFeedback.ledModule import LedController
from LEDFeedback.addressableLed import AddressableLedController
from SocketControl.edisonControl import EdisonControl
from EventDetector.eventDetection import EventDetection
from WebServer.app import app, socketio
from WebSockets.WebSockets import WSHandler
import threading, time, queue
from Sending.sendingModule import DataSender
from Threads.DataAcquisitionThread import DataAcquisitionThread
from Threads.DataProcessingThread import DataProcessingThread
from mDNS.mDNS_Advertisement import mDNS_Advertisment
import time
import signal
import sys
import socket
import tornado.httpserver
import tornado.ioloop
import tornado.web
import netifaces as ni

ip = ni.ifaddresses('wlan0')[2][0]['addr']

mainVoltage = 230 # TODO Comes from a configuration file

socketControl = EdisonControl(mainVoltage)

mDNS = mDNS_Advertisment()

threads = []

def runFlask():
    socketio.run(app, host=ip, debug=True, use_reloader=False)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    mDNS.stopAdvertise()
    sys.exit(0)

if __name__ == "__main__":
    flaskThread = threading.Thread(target=runFlask, daemon=True)
    flaskThread.start()
    mDNS.advertise()
    signal.signal(signal.SIGINT, signal_handler)
    powerSamples = []
    dataProcessingSemaphore = threading.Semaphore(value=0)
    socketControl.initializeRelay()

    dataAcquisitionThread = DataAcquisitionThread(socketControl, dataProcessingSemaphore, powerSamples)
    dataProcessingThread = DataProcessingThread(socketControl,dataProcessingSemaphore,powerSamples)

    threads = [dataProcessingThread, dataAcquisitionThread]


    dataProcessingThread.start()
    dataAcquisitionThread.start()

    # Waits fr all threads to finish
    for t in threads:
        t.join()
    # samplesQueue = []
    # samplesQueueSemaphore = threading.Semaphore(value=60)
    # samplesQueueFlowControlSemaphore = threading.Semaphore(value=0)
    #
    # socketControl.initializeRelay()
    #
    # dataAcquisitionThread = EdisonRead(samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl)
    # powerCalculationThread = EdisonPowerConsumption(samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl)
    # ledControlThread = LedController( 20, 14, 21)
    #
    # url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.58:3000/api/json/plugs_events"
    # url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.58:3000/api/json/continuous_measuring"
    # dataSenderThread = DataSender(url1, url2)
    #
    # eventDetectorThread = EventDetection(dataSenderThread)
    #
    # flaskThread = threading.Thread(target=runFlask)
    # threads = [flaskThread, ledControlThread, dataSenderThread, powerCalculationThread,  dataAcquisitionThread]
    #
    # ##Starts the threads
    # flaskThread.start() #Starts the webserver
    # #Subscriver Threads
    # eventDetectorThread.start()
    # ledControlThread.start()
    # dataSenderThread.start()
    # powerCalculationThread.start()
    # powerCalculationThread.add(ledControlThread)
    # powerCalculationThread.add(dataSenderThread)
    # powerCalculationThread.add(eventDetectorThread)
    #
    # dataAcquisitionThread.start()
    #
    # ##Waits fr all threads to finish
    # for t in threads:
    #     t.join()
