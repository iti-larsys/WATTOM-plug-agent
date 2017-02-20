import time, threading
from PublishSubscriber.Subscriber import Subscriber

class EventDetection (Subscriber, threading.Thread):

    def __init__(self, dataSender):
        threading.Thread.__init__(self)
        self.storePowerSamples = []
        self.previousEventTime = 0
        self.timeThreshold = 5
        self.powerThreshold = 25
        self.dataSender = dataSender
        self.eventSemaphore = threading.Semaphore(value=0)
        self.bufferSamples = []

    def update(self, data):
        print ("Going to check event")
        self.bufferSamples.append(data["power"])

    def run(self):
        stateValue = ""
        while True:
            self.eventSemaphore.acquire()
            print("Calculating event")
            self.storePowerSamples.append(self.bufferSamples.pop(0))
            if len(self.storePowerSamples) >= 5:
                # Calculates the average when the buffer is full
                storeAveragePowerBegin = (self.storePowerSamples[0] + self.storePowerSamples[1]) / 2
                storeAveragePowerEnd = (self.storePowerSamples[3] + self.storePowerSamples[4]) / 2
                averageDifference = storeAveragePowerBegin - storeAveragePowerEnd  # Module difference between the averages

                if time.time() - self.previousEventTime >= self.timeThreshold:  # Block Event Detection
                    if abs(averageDifference) >= self.powerThreshold:  # An event happened.
                        # Detects the triggers Up or Down
                        if averageDifference < 0:
                            print(" ### Turned a new device on ###")
                            stateValue = "ON"
                            self.previousEventTime = time.time()
                        elif averageDifference >= 0:
                            print(" ### Turned a device off ###")
                            stateValue = "OFF"
                            self.previousEventTime = time.time()
                        postEventData = {'type': stateValue, 'timestamp': time.time()}
                        self.dataSender.sendDataEvent(postEventData)
                self.storePowerSamples.pop(0)  # Remove one of the items it doesn't matter the order.