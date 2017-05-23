# from DataAcquisition.edisonRead import EdisonRead
# from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
# #from LEDFeedback.ledModule import LedController
# from LEDFeedback.addressableLed import AddressableLedController
# from SocketControl.edisonControl import EdisonControl
# from EventDetector.eventDetection import EventDetection
# from WebServer.app import app, socketio, x, mDNS
# import threading, time, queue
# from Sending.sendingModule import DataSender
# from Threads.DataAcquisitionThread import DataAcquisitionThread
# from Threads.DataProcessingThread import DataProcessingThread
# from mDNS.mDNS_Advertisement import mDNS_Advertisment
# from multiprocessing import Process
# import time
# import signal
# import sys
# import socket
# import netifaces as ni
# import mraa
#
# ip = ni.ifaddresses('wlan0')[2][0]['addr']
#
# #mainVoltage = 230 # TODO Comes from a configuration file
#
# #socketControl = EdisonControl(mainVoltage)
#
# #mDNS = mDNS_Advertisment()
#
# #threads = []
#
# #x = mraa.Gpio(20)
#
# def signal_handler(signal, frame):
#     print('You pressed Ctrl+C!')
#     x.isrExit()
#     mDNS.stopAdvertise()
#     sys.exit(0)
#
# '''
# def runFlask():
#     socketio.run(app, debug=False, log_output=False, host=ip, use_reloader=False)
#
# def registerInterrupt():
#     x.dir(mraa.DIR_IN)
#     x.isr(mraa.EDGE_RISING, interruptHandler, x)
#
# def interruptHandler(gpio):
#     socketio.emit("heartbeat", {"timestamp": time.time(), "hostname": socket.gethostname()})
#
# def stopInterruptHandling():
#     x.isrExit()
# '''
#
# if __name__ == "__main__":
#     signal.signal(signal.SIGINT, signal_handler)
#     socketio.run(app, host=ip)
#     '''
#     flaskThread = threading.Thread(target=runFlask, daemon=True)
#     flaskThread.start()
#     mDNS.advertise()
#     signal.signal(signal.SIGINT, signal_handler)
#     readModule = EdisonRead(socketControl)
#     powerConsumptionModule = EdisonPowerConsumption(socketControl)
#     url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/plugs_events"
#     url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/continuous_measuring"
#     dataSenderModule = DataSender(url1, url2)
#     eventDetectorModule = EventDetection(dataSenderModule)
#     ledControlModule = AddressableLedController()
#     registerInterrupt()
#     powerConsumptionModule.add(ledControlModule)
#     powerConsumptionModule.add(dataSenderModule)
#     powerConsumptionModule.add(eventDetectorModule)
#     while 1:
#     #     pass
#         samples = readModule.addDAQSample()
#         powerConsumptionModule.getPower(samples)
#     '''
#     # powerSamples = []
#     # dataProcessingSemaphore = threading.Semaphore(value=0)
#     # socketControl.initializeRelay()
#     #
#     # dataAcquisitionThread = DataAcquisitionThread(socketControl, dataProcessingSemaphore, powerSamples)
#     # dataProcessingThread = DataProcessingThread(socketControl,dataProcessingSemaphore,powerSamples)
#     #
#     # threads = [dataProcessingThread, dataAcquisitionThread]
#     #
#     #
#     # dataProcessingThread.start()
#     # dataAcquisitionThread.start()
#     #
#     # # Waits fr all threads to finish
#     # for t in threads:
#     #     t.join()
#
#
#
#     # samplesQueue = []
#     # samplesQueueSemaphore = threading.Semaphore(value=60)
#     # samplesQueueFlowControlSemaphore = threading.Semaphore(value=0)
#     #
#     # socketControl.initializeRelay()
#     #
#     # dataAcquisitionThread = EdisonRead(samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl)
#     # powerCalculationThread = EdisonPowerConsumption(samplesQueue, samplesQueueSemaphore, samplesQueueFlowControlSemaphore, socketControl)
#     # ledControlThread = LedController( 20, 14, 21)
#     #
#     # url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.58:3000/api/json/plugs_events"
#     # url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.58:3000/api/json/continuous_measuring"
#     # dataSenderThread = DataSender(url1, url2)
#     #
#     # eventDetectorThread = EventDetection(dataSenderThread)
#     #
#     # flaskThread = threading.Thread(target=runFlask)
#     # threads = [flaskThread, ledControlThread, dataSenderThread, powerCalculationThread,  dataAcquisitionThread]
#     #
#     # ##Starts the threads
#     # flaskThread.start() #Starts the webserver
#     # #Subscriver Threads
#     # eventDetectorThread.start()
#     # ledControlThread.start()
#     # dataSenderThread.start()
#     # powerCalculationThread.start()
#     # powerCalculationThread.add(ledControlThread)
#     # powerCalculationThread.add(dataSenderThread)
#     # powerCalculationThread.add(eventDetectorThread)
#     #
#     # dataAcquisitionThread.start()
#     #
#     # ##Waits fr all threads to finish
#     # for t in threads:
#     #     t.join()
#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from mDNS.mDNS_Advertisement import mDNS_Advertisment
from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
from LEDFeedback.addressableLed import AddressableLedController
from SocketControl.edisonControl import EdisonControl
from EventDetector.eventDetection import EventDetection
from Sending.sendingModule import DataSender
import mraa, time, socket, signal, sys
import netifaces as ni

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

ip = ni.ifaddresses('wlan0')[2][0]['addr']

mainVoltage = 230 # TODO Comes from a configuration file

socketControl = EdisonControl(mainVoltage)

mDNS = mDNS_Advertisment()
x = mraa.Gpio(20)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    x.isrExit()
    mDNS.stopAdvertise()
    sys.exit(0)

def registerInterrupt():
     x.dir(mraa.DIR_IN)
     x.isr(mraa.EDGE_RISING, interruptHandler, x)


def background_thread():
    """Example of how to send server generated events to clients."""
    registerInterrupt()
    signal.signal(signal.SIGINT, signal_handler)
    readModule = EdisonRead(socketControl)
    powerConsumptionModule = EdisonPowerConsumption(socketControl)
    url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/plugs_events"
    url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/continuous_measuring"
    #dataSenderModule = DataSender(url1, url2)
    #eventDetectorModule = EventDetection(dataSenderModule)
    ledControlModule = AddressableLedController()
    powerConsumptionModule.add(ledControlModule)
    #powerConsumptionModule.add(dataSenderModule)
    #powerConsumptionModule.add(eventDetectorModule)

    while 1:
        #pass
        socketio.sleep(0.5)
        samples = readModule.addDAQSample()
        powerConsumptionModule.getPower(samples)

def interruptHandler(gpio):
    timestamp = time.time()
    print("Vou enviar heartbeat")
    #socketio.sleep(1)
    socketio.emit("heartbeat", {"timestamp": timestamp, "hostname": socket.gethostname()})

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('initConfig')
def receiveInitialConfigs(message):
    socketControl.changeRelay(message["relayState"])
    AddressableLedController().initializeLeds(message["orientation"], message["position"], message["delay"],
                                              message["relayState"], message["personNear"])

@socketio.on('changeRelayState')
def changeRelayState(message):
    socketControl.changeRelay(message["relayState"])
    AddressableLedController().changeRelayState(message["relayState"])

@socketio.on('changeOrientation')
def changeOrientation(message):
    print(message)
    print("Going to change orientation")
    AddressableLedController().changeOrientation(message["orientation"])

@socketio.on('changePersonNear')
def changePersonNear(message):
    AddressableLedController().personChange(message["personNear"])

@socketio.on('changeDelay')
def changeDelay(message):
    AddressableLedController().changeDelay(message["delay"])

@socketio.on('changePosition')
def changePosition(message):
    AddressableLedController().changeLed(message["position"])

@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')

@socketio.on('selected')
def selected(message):
    AddressableLedController().makeSelectedFeedback()

@socketio.on('connect')
def test_connect():
    print("Client connected")
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    mDNS.advertise()
    socketio.run(app, host=ip)
