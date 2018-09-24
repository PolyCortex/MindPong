import serial

class SerialCommunicationService:
    BAUD = 9600
    PORT = 'COM6'

    def __init__(self):
        self.serial_channel = None

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

    def close_communication(self):
        if self.serial_channel is not None:
            self.serial_channel.close()

    def read_data(self):
        while self.serial_channel.in_waiting:
            return self.serial_channel.readline()

    def send_data(self, data):
        self.serial_channel.write(data)

