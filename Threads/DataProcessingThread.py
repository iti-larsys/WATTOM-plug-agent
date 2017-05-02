import threading, time
#from LEDFeedback.ledModule import LedController
from LEDFeedback.addressableLed import AddressableLedController
from EventDetector.eventDetection import EventDetection
from Sending.sendingModule import DataSender
from random import randint

class DataProcessingThread(threading.Thread):
    def __init__(self, socketControl, dataProcessingSemaphore, powerSamples):
        threading.Thread.__init__(self)
        self.daemon = True
        #self.ledControl = LedController(20, 14, 21)

        self.ledControl = AddressableLedController()

        url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.43.27:3000/api/json/plugs_events"
        url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.43.27:3000/api/json/continuous_measuring"
        self.dataSender = DataSender(url1, url2)

        self.socketControl = socketControl

        self.eventDetector = EventDetection(self.dataSender)
        self.dataProcessingSemaphore = dataProcessingSemaphore
        self.powerSamples = powerSamples

    def run(self):
        while True:
            self.dataProcessingSemaphore.acquire()
            print("Going to process")
            data = self.powerSamples.pop(0)
            '''self.ledControl.changeState(data["power"])
            self.ledControl.colorChange()'''
            # first byte at 1 indicates, that we are sending the power, second indicates the power
            self.ledControl.changePower(data["power"])
            '''power = randint(0,2000)
            print(power)
            self.ledControl.changePower(power)'''
            time.sleep(0.5 )
            #self.dataSender.sendDataValues({'power': data["power"], 'current': data["current"], 'timestamp': data["timestamp"]})
            #self.eventDetector.detectEvent(data["power"])
