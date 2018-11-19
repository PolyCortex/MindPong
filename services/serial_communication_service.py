from serial import Serial, SerialTimeoutException

BAUD_RATE = 9600
PORT = 'COM5'
READ_TIMEOUT = 1

class SerialCommunicationService(object):
    is_connected = False
    _serial_channel = None


    def establish_communication(self):
        try: 
            self._serial_channel = Serial(port=PORT, baudrate=BAUD_RATE, timeout=READ_TIMEOUT)
        except Exception as error:
            print "Error when creating serial %s port: %s" %(PORT, error.message)
            raise(error)

        if not self._serial_channel.is_open:
            self._serial_channel.open()
        self.is_connected = True


    def close_communication(self):
        if self._serial_channel is not None:
            self._serial_channel.close()
            self.is_connected = False


    def is_data_available(self):
        return self._serial_channel.in_waiting


    def read_data(self, nb_bytes=1):
        bytes_received = self._serial_channel.read(nb_bytes)
        if bytes_received is not None:
            return [ord(byte) for byte in str(bytes_received)]
            
        return None


    def send_data(self, data):
        try:
            self._serial_channel.write(data)
        except SerialTimeoutException as e:
            print 'Error when sending data to microcontroller:', str(e)


serial_communication_service = SerialCommunicationService()