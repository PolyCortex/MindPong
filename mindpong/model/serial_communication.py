import sys
from glob import glob

from serial import Serial, SerialException
import numpy as np

BAUD_RATE = 9600
PORT = 'COM5'
READ_TIMEOUT = 1


class SerialCommunication():
    def __init__(self):
        self._serial_channel = Serial()
        self._serial_channel.port = PORT
        self._serial_channel.baudrate = BAUD_RATE

    def set_baudrate(self, baudrate):
        if not self._serial_channel.is_open:
            self._serial_channel.baudrate = baudrate
        else:
            raise Exception("Close connection before changing baudrate")

    def set_port(self, port):
        if not self._serial_channel.is_open:
            self._serial_channel.port = port
        else:
            raise Exception("Close connection before changing port")

    def get_available_serial_ports(self):
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
        try:
            self._serial_channel.open()
        except SerialException as error:
            print("Error when creating serial %s port" % (self._serial_channel.port))
            raise(error)

        self.is_connected = True

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