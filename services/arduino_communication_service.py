import struct
import numpy as np
import time

from serial_communication_service import SerialCommunicationService

LOWER_BOUND = 0.05
UPPER_BOUND = 0.4

class ArduinoCommunicationService(SerialCommunicationService):
    
    def __init__(self):
        super(ArduinoCommunicationService, self).__init__()

    def send_data(self, data):
        if not self.is_connected or self.serial_channel is None:
            return

        value_to_send = self.get_clipped_signals(data)
        value_byte = bytes(bytearray(value_to_send))

        try:
            if super(ArduinoCommunicationService, self).is_data_available():
                print 'Reading', super(ArduinoCommunicationService, self).read_data(2)
            print 'Sending', value_to_send
            super(ArduinoCommunicationService, self).send_data(value_byte)
        except Exception as e:
            print 'Error when sending data to microcontroller:', str(e)
            self.is_playing = False
    
    def get_clipped_signals(self, signals):
        clipped_list = np.clip(signals, LOWER_BOUND, UPPER_BOUND)
        return [self.get_clipped_value(x) for x in clipped_list]
    
    def get_clipped_value(self, value):
        return int(255 * (value - LOWER_BOUND)/(UPPER_BOUND - LOWER_BOUND))

arduino_communication_service = ArduinoCommunicationService()