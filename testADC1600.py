import time, mraa, csv
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

startTime = time.time()
with open('1600_without_pause.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    while (time.time() - startTime < 1):
        readValue = pt1.adc_read()
        spamwriter.writerow([time.time(), readValue])

startTime = time.time()

with open('1600_with_pause.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
							quotechar='|', quoting=csv.QUOTE_MINIMAL)
    while (time.time() - startTime < 1):
        readValue = pt1.adc_read()
        spamwriter.writerow([time.time(), readValue])
        time.sleep(0.1)