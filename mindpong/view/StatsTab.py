from PyQt5.QtWidgets import QTabWidget

from collections import deque
import emoji
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QTabWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QMainWindow, QDialog

from mindpong.model.game import GameState

class StatsTab(QTabWidget):
    P_ONE = 0
    P_TWO = 1

    START_GAME_STRING = "▶️   Start Game"
    STOP_GAME_STRING = "⏹️   Stop Game "
    RESTART_GAME_STRING = "⟳ Restart Game"

    def __init__(self):
        super().__init__()
        self.centralLayout = QGridLayout()
        self.playButton = QPushButton(emoji.emojize(StatsTab.START_GAME_STRING))
        self.playerPlotWidget = [PlotWidget(), PlotWidget()]
        self.countDownModal = QDialog(self)
        self.gameState = 0
        self.init_ui()

    def init_ui(self):
        self.set_player_layouts(self.centralLayout)
        self.set_buttons()
        self.setLayout(self.centralLayout)

    def set_player_layouts(self, parent_layout):

        # Player 1 layout:

        player1_name = "Player 1"
        player1_label = QLabel(player1_name)
        layout_player1 = QGridLayout()
        group_box_player1 = QGroupBox()
        layout_player1.addWidget(player1_label)
        layout_player1.addWidget(self.playerPlotWidget[StatsTab.P_ONE])
        group_box_player1.setLayout(layout_player1)
        parent_layout.addWidget(group_box_player1, 0, StatsTab.P_ONE)

        # Player 2 layout:

        player2_name = "Player 2"
        player2_label = QLabel(player2_name)
        layout_player2 = QGridLayout()
        group_box_player2 = QGroupBox()
        layout_player2.addWidget(player2_label)
        layout_player2.addWidget(self.playerPlotWidget[StatsTab.P_TWO])
        group_box_player2.setLayout(layout_player2)
        parent_layout.addWidget(group_box_player2, 0, StatsTab.P_TWO)

    def set_buttons(self):
        self.playButton.setStyleSheet("background-color: #00a443")
        self.centralLayout.addWidget(self.playButton, 1, 0, 1, 1)
        self.playButton.clicked.connect(self.click_start_button_callback)
    
    def set_delegate(self, delegate):
        self.delegate = delegate

    def click_start_button_callback(self):
        if self.delegate and self.delegate.game.state == GameState.INITIAL:
            self.playButton.setText(StatsTab.STOP_GAME_STRING)
            self.playButton.setStyleSheet("background-color: #ff0000")
            self.playerPlotWidget[StatsTab.P_ONE].start_timer()
            self.playerPlotWidget[StatsTab.P_TWO].start_timer()
            self.gameState = 1

        elif self.delegate and self.delegate.game.state == GameState.IN_PLAY:
            self.playButton.setText(StatsTab.START_GAME_STRING)
            self.playButton.setStyleSheet("background-color: #00a443")
            self.playerPlotWidget[StatsTab.P_ONE].stop_timer()
            self.playerPlotWidget[StatsTab.P_TWO].stop_timer()
            self.gameState = 0

        else:
            print("error in game state \n")

    def click_restart_button_callback(self):
        if self.playerPlotWidget[0].deque or self.playerPlotWidget[1].deque:
            for plotWidget in self.playerPlotWidget:
                plotWidget.deque.clear()
                plotWidget.timeCount = 0

        # self.countDownWindow
        self.countDownModal.setStyleSheet("opacity: 0.1")
        self.countDownModal.setModal(True)
        # self.countDownModal.show()

        self.gameState = 0
        self.click_start_button_callback()


class PlotWidget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.plot = pg.PlotWidget()
        self.set_curve_axis()
        self.deque = deque(maxlen=1000)
        self.curve = self.plot.plot()
        self.timer = pg.QtCore.QTimer()
        self.timeCount = 0
        layout.addWidget(self.plot)

    def set_curve_axis(self):
        self.plot.plotItem.setLabel("left", "Amplitude", "mV")
        self.plot.plotItem.setLabel("bottom", "Temps", "s")

    def update(self):
        self.timeCount += 1
        data_tuple1 = (self.timeCount, np.random.random())
        self.timeCount += 1
        data_tuple2 = (self.timeCount, np.random.random())
        self.timeCount += 1
        data_tuple3 = (self.timeCount, np.random.random())
        self.deque.append(data_tuple1)
        self.deque.append(data_tuple2)
        self.deque.append(data_tuple3)
        min_val: int
        max_val: int
        time_array = []
        data_array = []
        for data_tuple in self.deque:
            time_array.append(data_tuple[0])
            data_array.append(data_tuple[1])

        # min_val = min(time_array)
        # max_val = max(time_array)
        # timestamps = np.linspace(min_val, max_val, 1000)
        self.curve.setData(x=time_array, y=data_array)

    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(12)

    def stop_timer(self):
        self.timer.stop()