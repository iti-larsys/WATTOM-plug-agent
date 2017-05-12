from flask import Flask
from flask_socketio import SocketIO
from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
#from LEDFeedback.ledModule import LedController
from LEDFeedback.addressableLed import AddressableLedController
from SocketControl.edisonControl import EdisonControl
from EventDetector.eventDetection import EventDetection
import threading, time, queue
from Sending.sendingModule import DataSender
from mDNS.mDNS_Advertisement import mDNS_Advertisment
from random import random
import time
import signal
import sys
import socket
import netifaces as ni
import mraa

app = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True)


thread = None

mainVoltage = 230 # TODO Comes from a configuration file

socketControl = EdisonControl(mainVoltage)

mDNS = mDNS_Advertisment()
mDNS.advertise()

x = mraa.Gpio(20)

def registerInterrupt():
    x.dir(mraa.DIR_IN)
    x.isr(mraa.EDGE_RISING, interruptHandler, x)

def interruptHandler(gpio):
    socketio.sleep(1)
    socketio.emit("heartbeat", {"timestamp": time.time(), "hostname": socket.gethostname()})

def stopInterruptHandling():
    x.isrExit()

def background_thread(self):
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    # infinite loop of magical random numbers
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})
        '''
        readModule = EdisonRead(socketControl)
        powerConsumptionModule = EdisonPowerConsumption(socketControl)
        url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/plugs_events"
        url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/continuous_measuring"
        #dataSenderModule = DataSender(url1, url2)
        #eventDetectorModule = EventDetection(dataSenderModule)
        ledControlModule = AddressableLedController()
        registerInterrupt()
        powerConsumptionModule.add(ledControlModule)
        #powerConsumptionModule.add(dataSenderModule)
        #powerConsumptionModule.add(eventDetectorModule)
        while 1:
            #     pass
            samples = readModule.addDAQSample()
            powerConsumptionModule.getPower(samples)
            
        '''

import WebServer.routes
