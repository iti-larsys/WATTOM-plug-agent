from WebServer.app import app, socketio
from main import socketControl
from flask import json, request
from flask.ext.socketio import SocketIO, emit
from LEDFeedback.addressableLed import AddressableLedController

@app.route('/relay', methods=['GET', 'POST'])
def relay():
    if request.method == 'POST':
        return json.dumps(socketControl.changeRelay())
    else:
        return json.dumps(socketControl.relay.read())

@app.route('/voltage/', methods=['POST'])
def voltage():
    voltage = request.form["voltage"]
    socketControl.setVoltage(voltage)
    return json.dumps(voltage)

@app.route('/calibrate', methods=['POST'])
def calibrate():
    socketControl.calibrate()
    return json.dumps(True)

@socketio.on('initConfig')
def test_message(message):
    AddressableLedController().initializeLeds(message["orientation"], message["position"], message["delay"],message["relayState"], message["personNear"])