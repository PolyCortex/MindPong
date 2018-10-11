import numpy as np
import time

from serial_communication_service import SerialCommunicationService

class ArduinoCommunicationService(SerialCommunicationService):
    LOWER_BOUND = 0.05
    UPPER_BOUND = 0.4

    def __init__(self):
        super(ArduinoCommunicationService, self).__init__()

    def send_data(self, data):
        if not self.is_connected or self.serial_channel is None:
            return

        sent_value = ""
        relative_beta_list = np.clip(data, self.LOWER_BOUND, self.UPPER_BOUND)
        for relative_beta in relative_beta_list:
            sent_value += str(100 + int((relative_beta - self.LOWER_BOUND)/(self.UPPER_BOUND - self.LOWER_BOUND) * 255))

        try:
            print 'Reading', super(ArduinoCommunicationService, self).read_data()
            print 'Sending', sent_value
            super(ArduinoCommunicationService, self).send_data(sent_value)
            time.sleep(1)
        except Exception as e:
            print 'Error when sending data to microcontroller:', str(e)
            self.is_playing = False
    

arduino_communication_service = ArduinoCommunicationService()