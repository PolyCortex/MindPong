from threading import Thread

import numpy as np

from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.signal import SignalData
from pymuse.configureshutdown import configure_shutdown

DEFAULT_IP_ADDRESS = "127.0.0.1"
SIGNAL_NAMES = ['beta_relative']


class Player(object):
    """ defines the properties of a player """

    def __init__(self, port, signal_callbacks, ip_address=DEFAULT_IP_ADDRESS):
        self._ip_address = ip_address
        self._port = port
        self._signal_callbacks = signal_callbacks
        self.is_playing = False
        self.signals = MuseOSCInputStream(SIGNAL_NAMES, ip_address, port)
        configure_shutdown(self.signals)


    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        if not self.is_playing:
            self._ip_address = ip_address
            self.signals: MuseOSCInputStream = MuseOSCInputStream(
                SIGNAL_NAMES, self._ip_address, self._port)
        else:
            raise Exception(
                "The player is currently playing. Stop the game before setting params")

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        if not self.is_playing:
            self._port = port
            self.signals = MuseOSCInputStream(
                SIGNAL_NAMES, self._ip_address, self._port)
        else:
            raise Exception(
                "The player is currently playing. Stop the game before setting params")

    def start(self):
        if not self.is_playing:
            try:
                self.signals.start()
                self._update_thread = Thread(target=self._update_signal).start()
            except Exception as e:
                print(e)
                raise Exception("Player: Unable to start thread")
            self.is_playing = True

    def stop(self):
        if self.is_playing:
            self.is_playing = False
            self._update_thread.join()
            self.signals.shutdown()

    def _update_signal(self):
        signals = []
        print("Player on port " + str(self._port) + ": started acquisition")
        while(self.is_playing):
            data: SignalData = self.signals.read(SIGNAL_NAMES[0])
            signal = (data.time, np.nanmean(data.values))
            for callback in self._signal_callbacks:
                callback(signal)
