import time, threading
from PublishSubscriber.Subscriber import Subscriber

class EventDetection (Subscriber):

    def __init__(self, dataSender):
        self.storePowerSamples = []
        self.previousEventTime = 0
        self.timeThreshold = 5
        self.powerThreshold = 25
        self.dataSender = dataSender
    def update(self, data):
        print ("Going to check event")
        self.detectEvent(data["power"])

    def detectEvent(self, power):
        stateValue = ""
        print("Calculating event")
        self.storePowerSamples.append(power)
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