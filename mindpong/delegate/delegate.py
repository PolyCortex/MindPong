from mindpong.model.game import Game, GameState
from mindpong.model.serial_communication import SerialCommunication


class Delegate():
    """ Manages the interaction from the view to the model """

    def set_model(self, game, serial_communication):
        self.game: Game = game
        self.serial_communication: SerialCommunication = serial_communication

    def start_game(self):
        self.serial_communication.establish_communication()
        self.game.state = GameState.IN_PLAY

    def end_game(self):
        self.game.state = GameState.INITIAL
        self.serial_communication.close_communication()
