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
    QScrollArea,
    QComboBox,
    QLabel,
    QWidget,
    QLineEdit
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPalette
from pyqtgraph import setConfigOptions, GraphicsLayoutWidget, ImageItem, HistogramLUTItem

from mindpong.model.services.historyreaderutils import read_player_signal, get_available_games
from mindpong.model.player import PlayerName
from pymuse.inputstream.muse_constants import MUSE_EEG_ACQUISITION_FREQUENCY

NO_AVAILABLE_GAMES = 'No Available Game for Analysis'
SCROLL_AREA_HEIGHT = 3000

class AnalysisTab(QTabWidget):

    def __init__(self):
        super().__init__()
        self.game_list = None
        self.game_selector = None
        self.scrollarea = None
        self.centralLayout = None
        self.analysisLayout = None
        self.graphics_layout = None
        self.spectrogram_widgets = []
        self.init_ui()

    def init_ui(self):
        self.centralLayout = QVBoxLayout()
        self.analysisLayout = QVBoxLayout()
        self.game_selector = self.create_game_selector()
        self.analysisLayout.addSpacing(40)
        self.analysisLayout.setSpacing(40)
        self.analysisLayout.addWidget(self.game_selector)
        self.analysisLayout
        self.analysisLayout.setAlignment(self.game_selector, Qt.AlignTop | Qt.AlignHCenter)
        self.populate_game_selector()
        if len(self.game_list):
            self.graphics_layout = self.create_graphics_layout(self.game_selector.currentText())
            self.analysisLayout.addLayout(self.graphics_layout)
        scrollarea = self.create_scroll_area()
        self.centralLayout.addWidget(scrollarea)
        self.setLayout(self.centralLayout)

    def create_scroll_area(self):
        scrollarea = QScrollArea(self)
        widget = QWidget()
        widget.setMinimumHeight(SCROLL_AREA_HEIGHT)
        widget.setLayout(self.analysisLayout)
        scrollarea.setWidget(widget)
        scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollarea.setWidgetResizable(True)
        return scrollarea

    def create_game_selector(self):
        game_selector = QComboBox(self)
        game_selector.setToolTip(
            'Please select a game to analyze the eeg activity.')
        game_selector.setFixedSize(230, 30)
        game_selector.currentTextChanged.connect(self.on_game_selector_change)
        return game_selector

    def populate_game_selector(self):
        self.game_list = get_available_games()
        self.game_selector.clear()
        if len(self.game_list):
            self.game_selector.addItems(self.game_list)
        else:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(NO_AVAILABLE_GAMES)
            line_edit.setReadOnly(True)
            self.game_selector.setLineEdit(line_edit)
        self.game_selector.update()
    
    def create_graphics_layout(self, game_name: str):
        ELECTRODES_NUMBER = 4
        setConfigOptions(imageAxisOrder='row-major')
        graphics_layout = QGridLayout()
        graphics_layout.setHorizontalSpacing(100)
        graphics_layout.setVerticalSpacing(60)
        for i, player_name in enumerate(PlayerName):
            for j in range(ELECTRODES_NUMBER):
                spectrogram_widget = GraphicsLayoutWidget()
                self.spectrogram_widgets.append((spectrogram_widget, player_name, j))
                graphics_layout.addWidget(spectrogram_widget, j, i)
        return graphics_layout

    def add_spectrogram_to_widget(self, widget: GraphicsLayoutWidget, game_name: str, player_name: PlayerName, electrode_name: str):
        # https://stackoverflow.com/questions/51312923/plotting-the-spectrum-of-a-wavfile-in-pyqtgraph-using-scipy-signal-spectrogram
        f, t, Sxx = self._acquire_spectrogram_signal(game_name, player_name, electrode_name)
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

    def set_delegate(self, delegate):
        self.delegate = delegate

    def on_game_selector_change(self, selected_game):
        if len(selected_game) and self.spectrogram_widgets is not None:
            for spectrogram_widget in self.spectrogram_widgets:
                spectrogram_widget[0].clear()
                self.add_spectrogram_to_widget(spectrogram_widget[0], selected_game, spectrogram_widget[1], "electrode %i"%spectrogram_widget[2])
            self.analysisLayout.update()

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
