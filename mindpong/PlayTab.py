import os
from collections import deque
import emoji
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import qsrand, QTime, qrand
from PyQt5.QtGui import QPalette, QWindow, QColor, QImage, QIcon
from PyQt5.QtWidgets import QWidget, QTabWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QMainWindow, QDialog, \
    QVBoxLayout, QHBoxLayout
import time


class PlayTab(QTabWidget):

    START_GAME_STRING = "▶️ Start"
    STOP_GAME_STRING = "⏹️ Stop"

    def __init__(self):
        super().__init__()
        self.currentDirectory = os.path.dirname(os.path.realpath(__file__))
        self.arrowPath = self.currentDirectory + os.path.sep + 'Images' + os.path.sep + 'arrow.png'
        self.centralGridLayout: QGridLayout
        self.playButton = QPushButton(emoji.emojize(PlayTab.START_GAME_STRING))
        self.countDownModal = QDialog(self)
        self.gameState = 0
        self.init_ui()

    def init_ui(self):
        self.set_labels_layout()

    def set_labels_layout(self):

        self.centralGridLayout = QGridLayout()
        self.setLayout(self.centralGridLayout)
        arrow_label = QLabel("➡")
        arrow_label.setFixedSize(40, 20)
        self.centralGridLayout.addWidget(QLabel("player1"), 0, 0)
        self.centralGridLayout.addWidget(arrow_label, 0, 3, 1, 2)
        self.centralGridLayout.addWidget(QLabel("player2"), 0, 5)
        self.centralGridLayout.addWidget(QLabel("Math Question: "), 1, 0, 1, 2)
        self.centralGridLayout.addWidget(self.playButton, 2,0, 1, 3)
        #button:

        self.playButton.setStyleSheet("background-color: #00a443")
        self.playButton.clicked.connect(self.click_start_button_callback)


    def click_start_button_callback(self):
        if self.gameState == 0:
            self.playButton.setText(PlayTab.STOP_GAME_STRING)
            self.playButton.setStyleSheet("background-color: #ff0000")
            self.gameState = 1

        elif self.gameState == 1:
            self.playButton.setText(PlayTab.START_GAME_STRING)
            self.playButton.setStyleSheet("background-color: #00a443")
            self.gameState = 0

        else:
            print("error in game state \n")

    def update_start_game_label(self):
        pass
