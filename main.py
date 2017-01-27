import time, mraa, math
from libs.Spark_ADC import Adc

ain0_operational_status = 							0b0
ain0_input_multiplexer_configuration = 				0b100
ain0_programmable_gain_amplifier_configuration =	0b001
ain0_device_operating_mode =						0b0
ain0_data_rate =									0b100
ain0_comparator_mode = 								0b0
ain0_compulator_polarity = 							0b0
ain0_latching_comparator	=						0b0
ain0_comparator_queue_and_disable =					0b11

pt1 = Adc()
pt1.set_config_command(
						ain0_operational_status,
						ain0_input_multiplexer_configuration,
						ain0_programmable_gain_amplifier_configuration,
						ain0_device_operating_mode,
						ain0_data_rate,
						ain0_comparator_mode,
						ain0_compulator_polarity,
						ain0_latching_comparator,
						ain0_comparator_queue_and_disable
					  )

sampleTime = 0.1
samples = 500
sampleInterval = sampleTime / samples

MainsVoltage = 230

sensibility = 66

adcZero = 0

#Use mraa 37 when using DFRobot (DFR338) shield or 13 when using edison kit
Relay = mraa.Gpio(37);
Relay.dir(mraa.DIR_OUT); #set the gpio direction to output

#Turns relay on/off according to relayState value at beginning
Relay.write(1);


def determineADCzero():
    averageVoltage = 0
    for i in range(5000):
        averageVoltage += pt1.adc_read()
    averageVoltage /= 5000
    return round(averageVoltage)


def getPower():
    result = 0
    countSamples = 0
    storeSamples = []
    startTime = time.time() - sampleInterval
    print("Getting samples")
    print("zero:" + str(adcZero))
    while (countSamples < samples):
        # To give some time before reading again
        if ((time.time() - startTime) >= sampleInterval):
            # Centers read value at zero
            readValue = pt1.adc_read() - adcZero
            storeSamples.append(readValue)
            # Squares all values and sums them
            result += (readValue * readValue)
            countSamples += 1
            startTime += sampleInterval
    print("Doing RMS")
    # Calculates RMS current. 3300 = 3.3V/mV. 1650 is the max ADC count i can get with 3.3V
    AmpRMS = (math.sqrt(result / countSamples)) * 3300 / (sensibility * 1650)

    print("Calculate power")
    # Calculates Power as an integer
    Power = (AmpRMS * MainsVoltage)
    print(round(Power))


print("Determining zero")
adcZero = determineADCzero()
print("Start measuring power")
while True:
    getPower()
