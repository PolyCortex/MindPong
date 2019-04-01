from enum import Enum

from mindpong.model.player import Player

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
        self.players = [
            Player(DEFAULT_PORT_PLAYER_ONE, signals_callback),
            Player(DEFAULT_PORT_PLAYER_TWO, signals_callback)
        ]

    def start(self):
        for player in self.players:
            player.start()
        self.state = GameState.IN_PLAY

    


        

