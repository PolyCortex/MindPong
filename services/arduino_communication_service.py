import struct
import numpy as np
import time

from serial_communication_service import SerialCommunicationService

LOWER_BOUND = 0.05
UPPER_BOUND = 0.4

class ArduinoCommunicationService(SerialCommunicationService):

    def send_data(self, data):
        if not self.is_connected:
            return

        if super(ArduinoCommunicationService, self).is_data_available():
            print 'Reading', super(ArduinoCommunicationService, self).read_data(2)

        value_to_send = self._get_clipped_signals(data)
        print 'Sending', value_to_send
        super(ArduinoCommunicationService, self).send_data(bytearray(value_to_send))
    

    def _get_clipped_signals(self, signals):
        clipped_list = np.clip(signals, LOWER_BOUND, UPPER_BOUND)
        return [self._get_clipped_value(x) for x in clipped_list]
    

    def _get_clipped_value(self, value):
        return int(255 * (value - LOWER_BOUND)/(UPPER_BOUND - LOWER_BOUND))

arduino_communication_service = ArduinoCommunicationService()