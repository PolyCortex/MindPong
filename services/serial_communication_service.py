import serial

class SerialCommunicationService(object):
    BAUD = 9600
    PORT = 'COM6'

    def __init__(self):
        self.serial_channel = None
        self.is_connected = False

    def establish_communication(self):
        try: 
            self.serial_channel = serial.Serial()
            self.serial_channel.port = self.PORT
            self.serial_channel.baudrate = self.BAUD
            self.serial_channel.readable()
            self.serial_channel.timeout = 1
            self.serial_channel.open()
        except Exception as e:
            print 'SerialCommunicationService: Could not connect to port ' + self.PORT
            print e
            raise(e)
        self.is_connected = True

    def close_communication(self):
        if self.serial_channel is not None:
            self.serial_channel.close()
            self.is_connected = False

    def is_data_available(self):
        return self.serial_channel.in_waiting

    def read_data(self, nb_bytes=1):
        bytes_received = self.serial_channel.read(nb_bytes)
        if bytes_received is not None:
            return [ord(byte) for byte in str(bytes_received)]
            
        return None

    def send_data(self, data):
        self.serial_channel.write(data)

serial_communication_service = SerialCommunicationService()