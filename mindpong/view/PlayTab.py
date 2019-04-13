import os
from typing import List

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QTabWidget, QGridLayout, QLabel, 
    QPushButton, QDialog, QMessageBox,
    QStyleFactory
)
from PyQt5.QtCore import Qt, pyqtSignal
import emoji
from serial import SerialException


from mindpong.view.utils import (
    BACKGROUND_COLORS, IMAGES_PATH, MINDPONG_TITLE,
    get_image_file)
from mindpong.view.widgets.scalablearrow import ScalableArrow
from mindpong.view.widgets.mathquestions import MathQuestions
from mindpong.model.game import GameState

PINGPONG_FILE_NAME = 'ball.png'
RED_PLAYER_FILE_NAME = 'red_player.png'
BLUE_PLAYER_FILE_NAME = 'blue_player.png'


class PlayTab(QTabWidget):
    update_signal_event = pyqtSignal(list)

    START_GAME_STRING = "▶️ Start"
    STOP_GAME_STRING = "⏹️ Stop"

    # (width_scale, height_scale)
    BALL_SCALE = (0.25, 0.25)

    def __init__(self):
        super().__init__()
        self.setStyle(QStyleFactory.create('Fusion'))

        # Layout
        self.centralGridLayout: QGridLayout
        # Widgets
        self.playButton: QPushButton
        self.errorBox: QMessageBox 
        # Custom Widgets
        self.math_question_widget: MathQuestions
        self.arrow_labels: List[ScalableArrow]
        # Labels
        self.player_logo_labels: List[QLabel]
        self.player_title_labels: List[QLabel]
        self.ball_label: QLabel

        self.init_ui()


    def init_ui(self):
        self.centralGridLayout = QGridLayout()
        self.centralGridLayout.setRowMinimumHeight(2, 150)
        self.setLayout(self.centralGridLayout)

        self.init_buttons()
        self.init_error_message_box()
        self.init_custom_widgets()
        self.init_labels()
        self.init_callbacks()

    def init_buttons(self):
        self.playButton = QPushButton(emoji.emojize(PlayTab.START_GAME_STRING))
        self.playButton.setStyleSheet(BACKGROUND_COLORS['GREEN'])
        self.playButton.clicked.connect(self._click_start_button_callback)
        self.centralGridLayout.addWidget(self.playButton, 2, 2, 1, 3)

    def init_error_message_box(self):
        self.errorBox = QMessageBox()
        self.errorBox.setIcon(QMessageBox.Warning)
        self.errorBox.setWindowTitle(MINDPONG_TITLE)

    def init_custom_widgets(self):
        # arrow pixmaps
        self.arrow_labels = [ScalableArrow(is_mirrored=True), ScalableArrow()]
        self.centralGridLayout.addWidget(self.arrow_labels[0], 0, 2, 1, 1, (Qt.AlignVCenter))
        self.centralGridLayout.addWidget(self.arrow_labels[1], 0, 4, 1, 1, (Qt.AlignVCenter))

        # mathquestions widget
        self.math_question_widget = MathQuestions()
        self.centralGridLayout.addWidget(self.math_question_widget, 1, 1, 1, 5, (Qt.AlignVCenter))

    def init_labels(self):
        # Create Player logos
        self.player_logo_labels = [
            self.get_picture_label(get_image_file(RED_PLAYER_FILE_NAME), (0.25, 0.25), (Qt.AlignCenter)),
            self.get_picture_label(get_image_file(BLUE_PLAYER_FILE_NAME), (0.25, 0.25), (Qt.AlignCenter))
        ]
        self.centralGridLayout.addWidget(self.player_logo_labels[0], 0, 0, 1, 2)
        self.centralGridLayout.addWidget(self.player_logo_labels[1], 0, 5, 1, 2)

        # Create Player title labels
        self.player_title_labels = self.set_players_labels()
        self.centralGridLayout.addWidget(self.player_title_labels[0], 0, 0, 1, 2)
        self.centralGridLayout.addWidget(self.player_title_labels[1], 0, 5, 1, 2)

        # Create ball pixmaps
        self.ball_label = self.get_picture_label(get_image_file(PINGPONG_FILE_NAME), self.BALL_SCALE, Qt.AlignCenter)
        self.centralGridLayout.addWidget(self.ball_label, 0, 3, 1, 1)
        self.ball_label.setFixedWidth(self.ball_label.pixmap().width())


    def set_players_labels(self):
        players = [QLabel("Player one"), QLabel("Player two")]
        for player in players:
            player.setFont(QFont("Times", 18, QFont.Bold))
            player.setMargin(70)
            player.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        return players
        
    def init_callbacks(self):
        self.update_signal_event.connect(self._update_signal)

    ###########################################################

    def get_picture_label(self, path, scale, alignment):
        label = QLabel()
        label.setAlignment(alignment)
        pixmap = QPixmap(path)
        label.setPixmap(pixmap.scaled(pixmap.width() * scale[0], pixmap.height() * scale[1]))
        return label

    def set_delegate(self, delegate):
        self.delegate = delegate
        self.math_question_widget.set_delegate(delegate)

    def _update_signal(self, signal):
        # player 1 signal means - player 2 signal means
        signal_difference = signal[0][1] - signal[1][1]
        current_winner = 0 if signal_difference > 0 else 1
        current_loser = 0 if current_winner is 1 else 1

        self.arrow_labels[current_winner].visible = True
        self.arrow_labels[current_loser].visible = False
        self.arrow_labels[current_loser].update()
        self.arrow_labels[current_winner].setWidth(abs(signal_difference))
        self.arrow_labels[current_winner].update()


    def _click_start_button_callback(self):
        if self.delegate and self.delegate.game.state == GameState.INITIAL:
            self._start_game()

        elif self.delegate and self.delegate.game.state == GameState.IN_PLAY:
            self.delegate.end_game()
            self.playButton.setText(PlayTab.START_GAME_STRING)
            self.playButton.setStyleSheet(BACKGROUND_COLORS['GREEN'])

        else:
            print("error in game state \n")

    def _start_game(self):
        try:
            self.delegate.start_game()
        except SerialException as e:
            self.errorBox.setText("Error: can't connect to serial %s port" % (self.delegate.serial_communication.port))
            self.errorBox.show()
            return

        self.playButton.setText(PlayTab.STOP_GAME_STRING)
        self.playButton.setStyleSheet(BACKGROUND_COLORS["RED"])
        

    def resizeEvent(self, event):
        # TODO: adjust labels to fit the screen correctly
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/qresizeevent.html
        return super(PlayTab, self).resizeEvent(event)
