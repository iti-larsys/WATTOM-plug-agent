import threading
import time
import socket


class AdcWorker(threading.Thread):
    adc = None
    running = True

    def __init__(self, adc,socket):
        threading.Thread.__init__(self)
        self.adc = adc
        self.adc.start_adc(0, gain=2/3)
        self.adc._device._logger.propagate = False
        self.socket = socket

    def stopAquisition(self):
        self.running = False
        print('stoping aquisition!!')
    
    def getMaxValue(self):
       sensorMax = 0
       start_time = int(round(time.time() * 1000))
       while((int(round(time.time() * 1000))-start_time) < 1000): #sample for 1000ms
           sensorValue =  self.adc.read_adc(0, gain=2/3)
           if (sensorValue > sensorMax): 
               #record the maximum sensor value
               sensorMax = sensorValue
       return sensorMax
    def getVPP(self):
        result = 0
        readValue = 0;             
        maxValue = 0;          
        minValue = 4096
        start_time =int(round(time.time() * 1000))
        while((int(round(time.time() * 1000))-start_time) < 1000): #sample for 1 Sec
            readValue = self.adc.get_last_result()
            #see if you have a new maxValue
            if (readValue > maxValue):
                # /*record the maximum sensor value*/
                maxValue = readValue
            if (readValue < minValue): 
                #/*record the maximum sensor value*/
                minValue = readValue
        
        # Subtract min from max
        result = ((maxValue - minValue) * 5.0)/4096.0        
        return result

    def stopAquisition(self):
        self.running = False

    def run(self):
        print('Reading ADS1x15 values, press Ctrl-C to quit...')
        # Print nice channel column headers.
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        print('-' * 37)
        while(self.running):
            Voltage = self.getVPP()
            VRMS = (Voltage/2.0) *0.707; 
            AmpsRMS = (VRMS * 1000)/185
            print(" Amps RMS "+str(AmpsRMS))
            print(" cons :"+str(AmpsRMS*230))
            self.socket.emit("powerData",{"data":(AmpsRMS*230),"hostname": socket.gethostname()})
        print("finishing ADC thread")
        self.adc.stop_adc()

