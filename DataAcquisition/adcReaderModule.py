import argparse
from adcWorker import AdcWorker
class AdcReaderModule:
    worker1    = None
    __instance = None

    def __new__(cls):
        """
        Create a Singleton
        :return:
        """
        if AdcReaderModule.__instance is None:
            AdcReaderModule.__instance = object.__new__(cls)
       # AddressableLedController.i2c = mraa.I2c(6)
        # AddressableLedController.i2c.address(8)
        return AdcReaderModule.__instance

    def initialize_adc_worker(self,adc,socket):
        if(AdcReaderModule.worker1==None):
            AdcReaderModule.worker1 = AdcWorker(adc,socket)
            AdcReaderModule.worker1.start()
       # else:
       #     AdcReaderModule.worker1.stopAquisition()
       #     AdcReaderModule.worker1 = AdcWorker(adc,socket)
       #     AdcReaderModule.worker1.start()
    
    def stop(self):
        AdcReaderModule.worker1.stopAquisition()