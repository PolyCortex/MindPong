from threading import Thread
import sys

import numpy as np
from enum import Enum

from mindpong.model.player import Player, SIGNAL_NAMES

DEFAULT_PORT_PLAYER_ONE = 5001
DEFAULT_PORT_PLAYER_TWO = 5002

class GameState(Enum):
    INITIAL   = 0,
    IN_PLAY   = 1,
    FINISHED  = 2

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
        print("Game started with "+ str(len(self.players)) + " players")
        while(self.state is GameState.IN_PLAY):
            try:
                data = [self._get_mean_signal(player) for player in self.players]
            except SystemExit:
                self.state = GameState.INITIAL
                break
                
            for callback in self.callbacks:
                callback(data)

        for player in self.players:
            player.stop()
        sys.exit()

    def _get_mean_signal(self, player):
        data: SignalData = player.signals.read(SIGNAL_NAMES[0])
        return (data.time, np.nanmean(data.values))

    


        

