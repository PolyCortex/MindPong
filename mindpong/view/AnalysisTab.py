from PyQt5.QtWidgets import QTabWidget

from collections import deque
import emoji
import numpy as np
from scipy import signal
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

from mindpong.model.services.historyreaderutils import read_player_signal, get_available_games
from mindpong.model.player import PlayerName
from pymuse.inputstream.muse_constants import MUSE_EEG_ACQUISITION_FREQUENCY


class AnalysisTab(QTabWidget):

    def __init__(self):
        super().__init__()
        self.game_selector = None
        self.centralLayout = None
        self.init_ui()

    def init_ui(self):
        self.centralLayout = QVBoxLayout()
        self.game_selector = self.create_game_selector()
        self.populate_game_selector()
        self.create_spectrograms('Game #0 - 2019-04-10-15_46_33')
        self.setLayout(self.centralLayout)

    def create_game_selector(self):
        self.centralLayout.addSpacing(20)
        game_selector = QComboBox(self)
        game_selector.setToolTip(
            'Please select a game to analyze the eeg activity.')
        game_selector.setFixedSize(230, 30)
        self.centralLayout.addWidget(game_selector)
        self.centralLayout.setAlignment(
            game_selector, Qt.AlignTop | Qt.AlignHCenter)
        return game_selector

    def populate_game_selector(self):
        self.game_list = get_available_games()
        self.game_selector.clear()
        if len(self.game_list):
            self.game_selector.addItems(self.game_list)
        else:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText('No Available Game for Analysis')
            line_edit.setReadOnly(True)
            self.game_selector.setLineEdit(line_edit)
        self.game_selector.update()
    
    def create_spectrograms(self, game_name: str):
        ELECTRODES_NUMBER = 4
        setConfigOptions(imageAxisOrder='row-major')
        spectrograms_layout = QGridLayout()
        for i, player_name in enumerate(PlayerName):
            for j in range(ELECTRODES_NUMBER):
                spectrograms_layout.addWidget(self.create_spectrogram(game_name, player_name, 'electrode %i'%j), j, i)
        self.centralLayout.addLayout(spectrograms_layout)

    def create_spectrogram(self, game_name: str, player_name: PlayerName, electrode_name: str):
        # https://stackoverflow.com/questions/51312923/plotting-the-spectrum-of-a-wavfile-in-pyqtgraph-using-scipy-signal-spectrogram
        f, t, Sxx = self._acquire_spectrogram_signal(game_name, player_name, electrode_name)
        widget = GraphicsLayoutWidget()
        plot = widget.addPlot()
        img = ImageItem()
        plot.addItem(img)
        hist = HistogramLUTItem()
        hist.setImageItem(img)
        widget.addItem(hist)
        hist.setLevels(np.min(Sxx), np.max(Sxx))
        hist.gradient.restoreState({
            'mode': 'rgb',
            'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]
        })
        img.setImage(Sxx)
        img.scale(t[-1]/np.size(Sxx, axis=1), f[-1]/np.size(Sxx, axis=0))
        plot.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
        plot.setLabel('bottom', "Time", units='s')
        plot.setLabel('left', "Frequency", units='Hz')
        return widget

    def set_delegate(self, delegate):
        self.delegate = delegate

    def _acquire_spectrogram_signal(self, game_name: str, player_name: PlayerName, electrode_name: str):
        eeg_signal = read_player_signal(game_name, player_name)
        f, t, Sxx = signal.spectrogram(np.array(eeg_signal[electrode_name]), MUSE_EEG_ACQUISITION_FREQUENCY, nperseg=128, detrend='linear', scaling='density')
        return self._remove_high_frequencies(f, t, Sxx)

    def _remove_high_frequencies(self, f, t, Sxx):
        F_MAX = 40
        freq_slice = np.where(f <= F_MAX)
        f   = f[freq_slice]
        Sxx = Sxx[freq_slice,:][0]
        return (f, t, Sxx)
