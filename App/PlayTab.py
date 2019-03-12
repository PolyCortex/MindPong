from collections import deque

import emoji
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QTabWidget, QGridLayout, QGroupBox, QLabel, QPushButton


class PlayTab(QTabWidget):

    PLAYER_ONE_POSITION = 0
    PLAYER_TWO_POSITION = 1

    START_GAME_STRING = "▶️   Start Game"
    STOP_GAME_STRING = "⏹️   Stop Game "
    def __init__(self):
        super().__init__()
        self.centralLayout = QGridLayout()
        self.playButton = QPushButton(emoji.emojize(PlayTab.START_GAME_STRING))
        self.gameState = 0
        self.init_ui()

    def init_ui(self):
        self.add_sub_layout(self.centralLayout, PlayTab.PLAYER_ONE_POSITION)
        self.add_sub_layout(self.centralLayout, PlayTab.PLAYER_TWO_POSITION)
        self.centralLayout.addWidget(self.playButton)
        self.playButton.clicked.connect(self.click_button_callback)
        self.setLayout(self.centralLayout)

    @staticmethod
    def add_sub_layout(parent_layout, layout_col_position):
        player_name = "Player " + str(layout_col_position + 1)
        player_label = QLabel(player_name)
        player_plot = PlotWidget()
        layout = QGridLayout()
        layout.addWidget(player_label)
        layout.addWidget(player_plot)
        group_box = QGroupBox()
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box, 0, layout_col_position)

    def click_button_callback(self):
        if self.gameState == 0:
            self.playButton.setText(PlayTab.STOP_GAME_STRING)
            self.gameState = 1
        else:
            self.playButton.setText(PlayTab.START_GAME_STRING)
            self.gameState = 0


class PlotWidget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.q = np.random.random(200)
        plot = pg.PlotWidget()
        layout.addWidget(plot)
        self.curve = plot.plot(self.q)


