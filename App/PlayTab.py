from collections import deque
import emoji
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QTabWidget, QGridLayout, QGroupBox, QLabel, QPushButton


class PlayTab(QTabWidget):

    P_ONE = 0
    P_TWO = 1

    START_GAME_STRING = "▶️   Start Game"
    STOP_GAME_STRING = "⏹️   Stop Game "

    def __init__(self):
        super().__init__()
        self.centralLayout = QGridLayout()
        self.playButton = QPushButton(emoji.emojize(PlayTab.START_GAME_STRING))
        self.playerPlotWidget = [PlotWidget(), PlotWidget()]
        self.gameState = 0
        self.init_ui()

    def init_ui(self):
        self.set_player_layouts(self.centralLayout)
        self.centralLayout.addWidget(self.playButton)
        self.playButton.clicked.connect(self.click_button_callback)
        self.setLayout(self.centralLayout)

    def set_player_layouts(self, parent_layout):

        # Player 1 layout:

        player1_name = "Player 1"
        player1_label = QLabel(player1_name)
        layout_player1 = QGridLayout()
        group_box_player1 = QGroupBox()
        layout_player1.addWidget(player1_label)
        layout_player1.addWidget(self.playerPlotWidget[PlayTab.P_ONE])
        group_box_player1.setLayout(layout_player1)
        parent_layout.addWidget(group_box_player1, 0, PlayTab.P_ONE)

        # Player 2 layout:

        player2_name = "Player 2"
        player2_label = QLabel(player2_name)
        layout_player2 = QGridLayout()
        group_box_player2 = QGroupBox()
        layout_player2.addWidget(player2_label)
        layout_player2.addWidget(self.playerPlotWidget[PlayTab.P_TWO])
        group_box_player2.setLayout(layout_player2)
        parent_layout.addWidget(group_box_player2, 0, PlayTab.P_TWO)

    def click_button_callback(self):
        if self.gameState == 0:
            self.playButton.setText(PlayTab.STOP_GAME_STRING)
            self.playerPlotWidget[PlayTab.P_ONE].start_timer()
            self.playerPlotWidget[PlayTab.P_TWO].start_timer()
            self.gameState = 1

        elif self.gameState == 1:
            self.playButton.setText(PlayTab.START_GAME_STRING)
            self.playerPlotWidget[PlayTab.P_ONE].stop_timer()
            self.playerPlotWidget[PlayTab.P_TWO].stop_timer()
            self.gameState = 0

        else:
            print("error in game state \n")


class PlotWidget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.plot = pg.PlotWidget()
        self.deque = deque(np.zeros(100), maxlen=100)
        self.curve = self.plot.plot()
        self.timer = pg.QtCore.QTimer()
        self.set_curve_axis()
        layout.addWidget(self.plot)

    def set_curve_axis(self):
        self.plot.plotItem.setLabel("left", "Amplitude", "mV")
        self.plot.plotItem.setLabel("bottom", "Temps", "s")

    def update(self):
        self.deque.append(np.random.random())
        self.curve.setData(self.deque)

    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def stop_timer(self):
        self.timer.stop()

