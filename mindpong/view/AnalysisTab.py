from PyQt5.QtWidgets import QTabWidget

from collections import deque
import emoji
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QGridLayout,
    QComboBox,
    QLabel,
    QLineEdit
)

from PyQt5.QtCore import Qt


class AnalysisTab(QTabWidget):

    def __init__(self):
        super().__init__()
        self.centralLayout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.create_game_selector()
        self.setLayout(self.centralLayout)

    def create_game_selector(self):
        game_selector = QComboBox(self)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText('No Available Game for Analysis')
        line_edit.setReadOnly(True)
        game_selector.setLineEdit(line_edit)
        game_selector.setToolTip('Please select a game to analyze the eeg activity.')
        game_selector.setFixedSize(230,30)
        self.centralLayout.addWidget(game_selector)
        self.centralLayout.setAlignment(game_selector, Qt.AlignCenter)

        # TODO: We'll only be use in the function that reads for saved game
        game_selector.addItems(['Game #0 - 2019-04-10-19_20_38', 'Game #1 - 2019-04-10-19_20_41'])

    def set_delegate(self, delegate):
        self.delegate = delegate
