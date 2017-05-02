from flask import Flask
from flask_socketio import SocketIO

from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
socketio = SocketIO(app, engineio_logger=True)
import WebServer.routes
