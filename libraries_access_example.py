import mraa
import time, signal, sys
from libs.SF_ADC import ADS1x15


def signal_handler(signal, frame):
    print ('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
# print 'Press Ctrl+C to exit'

# Select the gain
# gain = 6144  # +/- 6.144V
gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Select the sample rate
# sps = 128   # 128 samples per second
sps = 250  # 250 samples per second
# sps = 490   # 490 samples per second
# sps = 920   # 920 samples per second
# sps = 1600  # 1600 samples per second
# sps = 2400  # 2400 samples per second
# sps = 3300  # 3300 samples per second

# Initialise the ADC
# Full options = ADCS1x15(address=0x48, I2CPort=1)
adc = ADS1x15()

# Read channel 0 in single-ended mode using the settings above
x = 0
startTime = time.time()
while True:
    volts = adc.readADCSingleEnded(0, gain, sps) / 1000
    print ("%.6f" % (volts))
    print ("The Sample Number is :" + str(x))
    x = x + 1
    if x > 250 :
        x = 0
        print("The time to acquire 500 samples is: " + str(time.time()-startTime))

#If using DFRobot shield use these (they map to PWM 3, 5 and 9)
'''pwmRed = mraa.Pwm(20)
pwmGreen = mraa.Pwm(21)

pwmRed.enable(True)
pwmGreen.enable(True)

while True:
    pwmGreen.write(0)
    pwmRed.write(1)
    time.sleep(0.2)
    pwmRed.write(0)
    pwmGreen.write(1)
    time.sleep(0.2)
'''