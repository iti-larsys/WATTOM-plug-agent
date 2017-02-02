from WebServer.app import app
from main import socketControl
from flask import json, request

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