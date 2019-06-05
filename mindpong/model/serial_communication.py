import sys
from glob import glob

from serial import Serial, SerialException
import numpy as np

BAUD_RATE = 9600
DEFAULT_PORT = 'COM4'
READ_TIMEOUT = 1

LOWER_BOUND = 0.01
UPPER_BOUND = 0.4


class SerialCommunication():
    """ Manages the communication and sends the data to the Arduino """

    def __init__(self):
        self._serial_channel = Serial()
        self._serial_channel.baudrate = BAUD_RATE
        available_ports = self.get_available_serial_ports()
        self._serial_channel.port =  DEFAULT_PORT if len(available_ports) == 0 else available_ports[0]


    @property
    def baudrate(self):
        return self._serial_channel.baudrate

    @baudrate.setter
    def baudrate(self, new_baudrate):
        if not self._serial_channel.is_open:
            self._serial_channel.baudrate = new_baudrate
        else:
            raise Exception("Close connection before changing baudrate")


    @property
    def port(self):
        return self._serial_channel.port


    @port.setter
    def set_port(self, new_port):
        if not self._serial_channel.is_open:
            self._serial_channel.port = new_port
        else:
            raise Exception("Close connection before changing port")


    def get_available_serial_ports(self):
        """ Returns a list of all ports that can be opened """
        if self._serial_channel.is_open:
            raise Exception("Close connection before")

        result = []
        for port in self._list_all_possibles_ports():
            try:
                Serial(port).close()
                result.append(port)
            except (OSError, SerialException):
                pass
        return result


    def establish_communication(self):
        """ 
        Enables the communication with the arduino with the latest parameters 
        
        Throws a SerialException is it cannot connect to port
        """
        try:
            self._serial_channel.open()
        except SerialException as error:
            print("Error when connecting to serial %s port" % (self._serial_channel.port))
            raise(SerialException)


    def send_data(self, data):
        """ prints feedback data from the arduino and sends the new data """
        if self._is_data_available():
            print(("Reading : ", self._read_bytes(len(data))))

        data = [x[1] for x in data]

        if self._is_data_valid(data):
            value_to_send = self._get_clipped_signals(data)
            print(('Sending', value_to_send))
            try:
                self._serial_channel.write(bytearray(value_to_send))
            except SerialTimeoutException as e:
                print('Error when sending data to microcontroller:' + str(e))        


    def close_communication(self):
        self._serial_channel.close()


    def _list_all_possibles_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        
        return ports


    def _read_bytes(self, nb_bytes=1):
        bytes_received = []
        for _ in range(nb_bytes):
            bytes_received.append(self._serial_channel.read(1))

        return [ord(byte) for byte in bytes_received if byte]        


    def _is_data_available(self):
        return self._serial_channel is not None and self._serial_channel.is_open and self._serial_channel.in_waiting


    def _is_data_valid(self, data):
        return self._serial_channel is not None and self._serial_channel.is_open and not np.any(np.isnan(data))


    def _get_clipped_signals(self, signals):
        clipped_list = np.clip(signals, LOWER_BOUND, UPPER_BOUND)
        return [int(255 * (x - LOWER_BOUND)/(UPPER_BOUND - LOWER_BOUND)) for x in clipped_list]

