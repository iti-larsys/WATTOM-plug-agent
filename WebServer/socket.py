from WebServer.app import app, socketio
from PublishSubscriber.Subscriber import Subscriber

class Socket(Subscriber):
    def update(self, data):
        socketio.emit(data)