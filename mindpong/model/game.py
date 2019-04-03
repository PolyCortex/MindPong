from threading import Thread
import sys

from pymuse.signal import SignalData
import numpy as np
from enum import Enum
from queue import Empty

from mindpong.model.player import Player, SIGNAL_NAMES

DEFAULT_PORT_PLAYER_ONE = 5001
DEFAULT_PORT_PLAYER_TWO = 5002
TIMEOUT_READ_DATA = 0.01  # seconds


class GameState(Enum):
    INITIAL = 0,
    IN_PLAY = 1,
    FINISHED = 2


class Game():
    """ Represents the game state """

    def __init__(self, signals_callback):
        self.state: GameState = GameState.INITIAL
        self.winner = None
        self.callbacks = signals_callback
        self.players = [
            Player(DEFAULT_PORT_PLAYER_ONE, signals_callback),
            Player(DEFAULT_PORT_PLAYER_TWO, signals_callback)
        ]

    def start(self):
        if self.state is GameState.INITIAL:
            for player in self.players:
                player.start()
                player.is_playing = True

            self._update_thread = Thread(target=self._update_signal).start()
            self.state = GameState.IN_PLAY

    def _update_signal(self):
        print("Game started with " + str(len(self.players)) + " players")
        data = [np.nan] * len(self.players)

        while(self.state is GameState.IN_PLAY):
            try:
                data = self._get_players_data(data)
            except SystemExit:
                self.state = GameState.INITIAL
                break

            if self._has_undefined_signal(data):
                print("Warning: cannot get signal for player no "
                      + self._get_index_without_signal(data))
                continue

            for callback in self.callbacks:
                callback(data)

        for player in self.players:
            player.stop()

    def _get_players_data(self, data):
        for i, player in enumerate(self.players):
            try:
                while True:
                    # Try to pop until we have the newest data for the player
                    # only conserves the values elements
                    data[i] = self._get_mean_signal(player)
            except Empty:
                pass

        return data

    def _get_mean_signal(self, player):
        data: SignalData = player.signals.read(SIGNAL_NAMES[0], TIMEOUT_READ_DATA)
        return (data.time, np.nanmean(data.values))

    def _has_undefined_signal(self, data):
        return np.any([x is np.nan for x in data if x is not SignalData])

    def _get_index_without_signal(self, data):
        undefined_signal = [x is np.nan for x in data if x is not SignalData]
        return " ".join([str(i) for i, x in enumerate(undefined_signal) if x])
