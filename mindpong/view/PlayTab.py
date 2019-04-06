import os
from collections import deque
import emoji
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import qsrand, QTime, qrand
from PyQt5.QtGui import QPalette, QWindow, QColor, QImage, QIcon
from PyQt5.QtWidgets import QWidget, QTabWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QMainWindow, QDialog, \
    QVBoxLayout, QHBoxLayout, QMessageBox
import time
from serial import SerialException


from mindpong.utils import get_project_root
from mindpong.view.utils import BACKGROUND_COLORS
from mindpong.model.game import GameState


class PlayTab(QTabWidget):

    START_GAME_STRING = "▶️ Start"
    STOP_GAME_STRING = "⏹️ Stop"

    def __init__(self):
        super().__init__()
        self.arrowPath = os.path.sep.join(
            [get_project_root(), 'img_src', 'arrow.png'])
        self.centralGridLayout: QGridLayout
        self.playButton = QPushButton(emoji.emojize(PlayTab.START_GAME_STRING))
        self.countDownModal = QDialog(self)
        self.gameState = 0
        self.init_ui()

    def init_ui(self):
        self.set_labels_layout()
        self.init_error_message_box()

    def set_labels_layout(self):

        self.centralGridLayout = QGridLayout()
        self.setLayout(self.centralGridLayout)
        arrow_label = QLabel("➡")
        arrow_label.setFixedSize(40, 20)
        self.centralGridLayout.addWidget(QLabel("player1"), 0, 0)
        self.centralGridLayout.addWidget(arrow_label, 0, 3, 1, 2)
        self.centralGridLayout.addWidget(QLabel("player2"), 0, 5)
        self.centralGridLayout.addWidget(QLabel("Math Question: "), 1, 0, 1, 2)
        self.centralGridLayout.addWidget(self.playButton, 2, 0, 1, 3)
        #button:

        self.playButton.setStyleSheet(BACKGROUND_COLORS['GREEN'])
        self.playButton.clicked.connect(self.click_start_button_callback)

    def init_error_message_box(self):
        self.errorBox: QMessageBox = QMessageBox()
        self.errorBox.setIcon(QMessageBox.Warning)
        self.errorBox.setWindowTitle("Mindpong")

    def set_delegate(self, delegate):
        self.delegate = delegate

    def click_start_button_callback(self):
        if self.delegate and self.delegate.game.state == GameState.INITIAL:
            self.start_game()

        elif self.delegate and self.delegate.game.state == GameState.IN_PLAY:
            self.delegate.end_game()
            self.playButton.setText(PlayTab.START_GAME_STRING)
            self.playButton.setStyleSheet(BACKGROUND_COLORS['GREEN'])

        else:
            print("error in game state \n")

    def start_game(self):
        try:
            self.delegate.start_game()
        except SerialException as e:
            self.errorBox.setText("Error: can't connect to serial %s port" % (self.delegate.serial_communication.port))
            self.errorBox.show()
            return

        self.playButton.setText(PlayTab.STOP_GAME_STRING)
        self.playButton.setStyleSheet(BACKGROUND_COLORS["RED"])


    def update_start_game_label(self):
        pass
