from PyQt5.QtWidgets import QTabWidget

from collections import deque
import emoji
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QComboBox,
    QLabel,
    QLineEdit
)
from PyQt5.QtCore import Qt
from pyqtgraph import setConfigOptions, GraphicsLayoutWidget, ImageItem, HistogramLUTItem


class AnalysisTab(QTabWidget):

    def __init__(self):
        super().__init__()
        self.centralLayout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.create_game_selector()
        self.create_spectrograms()
        self.setLayout(self.centralLayout)

    def create_game_selector(self):
        self.centralLayout.addSpacing(20)
        game_selector = QComboBox(self)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText('No Available Game for Analysis')
        line_edit.setReadOnly(True)
        game_selector.setLineEdit(line_edit)
        game_selector.setToolTip(
            'Please select a game to analyze the eeg activity.')
        game_selector.setFixedSize(230, 30)
        self.centralLayout.addWidget(game_selector)
        self.centralLayout.setAlignment(
            game_selector, Qt.AlignTop | Qt.AlignHCenter)
        # TODO: We'll only be use in the function that reads for saved game
        #game_selector.addItems(['Game #0 - 2019-04-10-19_20_38', 'Game #1 - 2019-04-10-19_20_41'])

    def create_spectrograms(self):
        setConfigOptions(imageAxisOrder='row-major')
        spectrograms_layout = QGridLayout()
        spectrograms_layout.addWidget(self.create_spectrogram(), 0, 0)
        spectrograms_layout.addWidget(self.create_spectrogram(), 0, 1)
        spectrograms_layout.addWidget(self.create_spectrogram(), 1, 0)
        spectrograms_layout.addWidget(self.create_spectrogram(), 1, 1)
        spectrograms_layout.addWidget(self.create_spectrogram(), 2, 0)
        spectrograms_layout.addWidget(self.create_spectrogram(), 2, 1)
        spectrograms_layout.addWidget(self.create_spectrogram(), 3, 0)
        spectrograms_layout.addWidget(self.create_spectrogram(), 3, 1)
        self.centralLayout.addLayout(spectrograms_layout)

    def create_spectrogram(self):
        win = GraphicsLayoutWidget()
        p1 = win.addPlot()
        img = ImageItem()
        p1.addItem(img)
        hist = HistogramLUTItem()
        hist.setImageItem(img)
        win.addItem(hist)
        win.show()
        #hist.setLevels(np.min(Sxx), np.max(Sxx))
        hist.gradient.restoreState(
            {'mode': 'rgb',
             'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]})
       # img.setImage(Sxx)
        #img.scale(t[-1]/np.size(Sxx, axis=1), f[-1]/np.size(Sxx, axis=0))
        #p1.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
        p1.setLabel('bottom', "Time", units='s')
        p1.setLabel('left', "Frequency", units='Hz')
        return win


    def set_delegate(self, delegate):
        self.delegate = delegate
