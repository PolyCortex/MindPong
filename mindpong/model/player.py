from pymuse.pipeline import Pipeline
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.pipelinestages.outputstream.muse_csv_output_stream import MuseCSVOutputStream
from pymuse.signal import SignalData

from enum import Enum

DEFAULT_IP_ADDRESS = "127.0.0.1"
SIGNAL_NAMES = ['beta_relative', 'eeg']


class PlayerName(Enum):
    PLAYER_ONE = 'Player One'
    PLAYER_TWO = 'Player Two'


class Player(object):
    """ defines the properties of a player """

    def __init__(self, player_name: PlayerName, signal_callbacks, port, ip_address=DEFAULT_IP_ADDRESS):
        if not isinstance(player_name, PlayerName):
            raise TypeError(
                'player_name parameter must be of type enum PlayerName')
        self._player_name = player_name
        self._port = port
        self._signal_callbacks = signal_callbacks
        self._ip_address = ip_address
        self._signals = None
        self._eeg_pipeline = None
        self.is_playing = False

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def signals(self):
        return self._signals

    @ip_address.setter
    def ip_address(self, ip_address):
        self._ip_address = ip_address

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    def start(self, game_number: int):
        """
        Called when the start button is pressed
        """
        self._configure_pipeline(game_number)
        if not self.is_playing:
            self.signals.start()
            self.eeg_pipeline.start()
            self.is_playing = True

    def stop(self):
        if self.is_playing:
            self._signals.shutdown()
            self.eeg_pipeline.shutdown()
        self.is_playing = False

    def _configure_pipeline(self, game_name):
        self._signals = MuseOSCInputStream(
            SIGNAL_NAMES, self._ip_address, self._port)
        self.eeg_pipeline = Pipeline(self.signals.get_signal('eeg'),
                                     MuseCSVOutputStream('History/%s/%s' % (game_name, self._player_name.value)))
