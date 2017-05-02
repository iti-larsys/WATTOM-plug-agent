from WebServer.app import app, socketio
from main import socketControl
from flask import json, request
from flask_socketio import SocketIO, emit
from LEDFeedback.addressableLed import AddressableLedController

# @app.route('/relay', methods=['GET', 'POST'])
# def relay():
#     if request.method == 'POST':
#         return json.dumps(socketControl.changeRelay())
#     else:
#         return json.dumps(socketControl.relay.read())
#
# @app.route('/voltage/', methods=['POST'])
# def voltage():
#     voltage = request.form["voltage"]
#     socketControl.setVoltage(voltage)
#     return json.dumps(voltage)
#
# @app.route('/calibrate', methods=['POST'])
# def calibrate():
#     socketControl.calibrate()
#     return json.dumps(True)

@socketio.on('connect')
def test_connect():
    print('Client new Connection')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

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
