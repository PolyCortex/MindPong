import numpy as np
import time

from serial_communication_service import SerialCommunicationService

class ArduinoCommunicationService(SerialCommunicationService):
    LOWER_BOUND = 0.05
    UPPER_BOUND = 0.4
    MIN_FAN_SPEED = 30
    PADDING = 3

    def __init__(self):
        super(ArduinoCommunicationService, self).__init__()

    def send_data(self, data):
        if not self.is_connected or self.serial_channel is None:
            return

        value_to_send = self.get_clipped_signals(data)

        try:
            print 'Reading', super(ArduinoCommunicationService, self).read_data()
            print 'Sending', value_to_send
            super(ArduinoCommunicationService, self).send_data("".join(value_to_send))
            time.sleep(1)
        except Exception as e:
            print 'Error when sending data to microcontroller:', str(e)
            self.is_playing = False
    
    def get_clipped_signals(self, signals):
        clipped_list = np.clip(signals, self.LOWER_BOUND, self.UPPER_BOUND)
        return [
            str(self.get_clipped_value(x)).zfill(self.PADDING)
            for x in clipped_list
        ]
    
    def get_clipped_value(self, value):
        return int(255 * (value - self.LOWER_BOUND)/(self.UPPER_BOUND - self.LOWER_BOUND)) + self.MIN_FAN_SPEED

arduino_communication_service = ArduinoCommunicationService()