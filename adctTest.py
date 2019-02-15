import Adafruit_ADS1x15
import time

adc = Adafruit_ADS1x15.ADS1015(address=0x48)
adc.start_adc(0, gain=2/3)
mVperAmp = 185
def getMaxValue():
       sensorMax = 0
       start_time = int(round(time.time() * 1000))
       i=0
       while((int(round(time.time() * 1000))-start_time) < 50*5): #sample for 1000ms
           sensorValue =  adc.get_last_result()
           sensorMax =sensorMax + sensorValue
           i = i+1
           time.sleep(0.02)    
       return sensorMax/i


print('Reading ADS1x15 values, press Ctrl-C to quit...')
    # Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
GAIN = 2/3
i=0

def getVPP():
  result = 0
  readValue = 0;             
  maxValue = 0;          
  minValue = 4096
  start_time =int(round(time.time() * 1000))
  while((int(round(time.time() * 1000))-start_time) < 1000): #sample for 1 Sec
       readValue = adc.get_last_result()
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

while(i<300):
    getVPP()
    Voltage = getVPP()
    VRMS = (Voltage/2.0) *0.707; 
    AmpsRMS = (VRMS * 1000)/mVperAmp
    print(" Amps RMS "+str(AmpsRMS))
    print(" cons :"+str(AmpsRMS*230))
    i=i+1
    # sensor_max = getMaxValue()
    # # print("sensor_max = "+str(sensor_max))
    # #       #the VCC on the Grove interface of the sensor is 5v
    # # v =(float)((sensor_max-4096)*5)/2048
    # # a  =(v*1000/185)
    # # print("The effective value of the current is(in mA):" +str(a))
    # amplitude_current=(float)(sensor_max-1024)/2048*5/185*1000000
    # effective_value=amplitude_current/1.414
    # minimum_current=1/1024*5/185*1000000/1.414
    #       #Only for sinusoidal alternating current
    # print("The amplitude of the current is(in mA): "+str(amplitude_current))
    # print("The effective value of the current is(in mA):" +str(effective_value))
    # print("the minimum current is (mA) "+str(minimum_current))     