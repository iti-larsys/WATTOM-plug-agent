#! /user/bin/env python
#import mraa
import netifaces as ni
import signal
import socket
import sys
import time
import os.path
import Adafruit_ADS1x15
import logging
from flask import Flask, request, Response
from flask_socketio import SocketIO, emit 
from neopixel import Color


#from DataAcquisition.edisonRead import EdisonRead
from LEDFeedback.addressableLed import AddressableLedController
#from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
#from SocketControl.edisonControl import EdisonControl
from mDNS.MdnsAdvertisment import MdnsAdvertisment
from SocketControl.piSocketControl import PiSocketController
from LEDFeedback.neoPixelController import NeoPixelController
from DataAcquisition.adcWorker import AdcWorker
from DataAcquisition.adcReaderModule import AdcReaderModule

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "gevent"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

ip = ni.ifaddresses('wlan0')[2][0]['addr']
#ip = ni.ifaddresses('eth0')[2][0]['addr']
mainVoltage = 230  # TODO Comes from a configuration file

#socket_control = EdisonControl(mainVoltage)

mDNS = MdnsAdvertisment()
#x = mraa.Gpio(20)

#ADC stuff
adc = Adafruit_ADS1x15.ADS1015(address=0x48)

def signal_handler(signal, frame):
    """
    Invoked when Ctrl+C is pressed
    :param signal:
    :param frame:
    :return:
    """
    print('You pressed Ctrl+C!')
    mDNS.stop_advertise()
    NeoPixelController().stop()
    AdcReaderModule().stop()
    sys.exit(0)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)
#
#   DEBUG INDEX STUFF
#


def register_interrupt():
    """
    Register an Software interrupt to handle the Arduino Heartbeats
    :return:
    """
    x.dir(mraa.DIR_IN)
    x.isr(mraa.EDGE_RISING, interrupt_handler, x)


def background_thread():
    """
    Background thread that handle all the code that is not related with the communication with the broker
    Like receiveing the hearbeats, reading and calculating power, and sending it to server
    :return:
    """
    print("Background thread started")
    #register_interrupt()
    signal.signal(signal.SIGINT, signal_handler)
   # read_module = EdisonRead(socket_control)
   # power_consumption_module = EdisonPowerConsumption(socket_control)
    url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/plugs_events"
    url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/continuous_measuring"
    # dataSenderModule = DataSender(url1, url2)
    # eventDetectorModule = EventDetection(dataSenderModule)
    led_control_module = AddressableLedController()
    #power_consumption_module.add(led_control_module)
    # power_consumption_module.add(dataSenderModule)
    # power_consumption_module.add(eventDetectorModule)

    while 1:
        # pass
        socketio.sleep(0.5)  # This can't be removed, otherwise the heartbeats sending will fail
        #print('aqui')
        #sendHeartBeat()
        # samples = read_module.addDAQSample()
        # power_consumption_module.getPower(samples)


def sendHeartBeat():
    """
    Handles the Arduino Heartbeats and sends it to the broker
    :param gpio:
    :return:
    """
    timestamp = time.time()
    print("Vou enviar heartbeat")
    # socketio.sleep(1)
    socketio.emit("heartbeat", {"timestamp": timestamp, "hostname": socket.gethostname()})

def interrupt_handler(gpio):
    """
    Handles the Arduino Heartbeats and sends it to the broker
    :param gpio:
    :return:
    """
    timestamp = time.time()
    print("Vou enviar heartbeat")
    # socketio.sleep(1)
    socketio.emit("heartbeat", {"timestamp": timestamp, "hostname": socket.gethostname()})


@socketio.on('initConfig')
def receive_initial_configs(message):
    #socket_control.initialize_relay(message["relayState"])
    print(message)
    if('background' in message.keys()):
        background = {'red':message['background']['red'],'green':message['background']['green'], 'blue':message['background']['blue']}
    else:
        background = {'red':0,'green':0, 'blue':0}

    print(background)
    #{u'delay': 200, u'leds': [{u'blue': 255, u'position': 10, u'green': 255, u'orientation': 1, u'red': 255}], u'relayState': 0, u'personNear': 1}
    # AddressableLedController().initialize_leds(message["leds"], message["relayState"], message["personNear"],
    #                                            message["delay"])
    NeoPixelController().initialize_leds(message["leds"], message["relayState"], message["personNear"],socketio, message["delay"],background)
    AdcReaderModule().initialize_adc_worker(adc,socketio)

@socketio.on('changeRelayState')
def change_relay_state(message):
    print(message['relayState'])
    if(int(message['relayState'])==1):
        PiSocketController().ON()
    else:
        PiSocketController().OFF()

@socketio.on('changePersonNear')
def change_person_near(message):
    AddressableLedController().person_change(message["personNear"])


@socketio.on('changeDelay')
def change_delay(message):
    NeoPixelController().changeDelay(message["delay"])


@socketio.on('changePosition')
def change_position(message):
    print(message["position"])
    #AddressableLedController().changeLed(message["position"])


@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')


@socketio.on('selected')
def selected(message):
    print(message['led'])
    NeoPixelController().select(message['led'])
    #AddressableLedController().make_selected_feedback(message["led"])


@socketio.on('stop')
def selected(message):
    print('stoping leds')
    NeoPixelController().stop()

    #AddressableLedController().stop_movement()
####
##  DEBUG MESSAGE
###
@socketio.on('debug')
def selected(message):
    print(NeoPixelController())
    NeoPixelController().startup()

@socketio.on('stop_debug')
def stop(message):
    NeoPixelController().stop()

@socketio.on('aquisition')
def startStopAq(message):
    if(message['command']==1):
        AdcReaderModule().initialize_adc_worker(adc)
    else:
        AdcReaderModule().stop()



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

@app.route('/',methods=['GET'])
def index():
    content = get_file('debug_index.html')
    return Response(content,mimetype="text/html")

if __name__ == '__main__':
   NeoPixelController().startup()
   mDNS.advertise()
   PiSocketController().OFF()
   socketio.run(app, host=ip)
   #print("aqui")
   ##app.run(host=ip)                 
    
   
