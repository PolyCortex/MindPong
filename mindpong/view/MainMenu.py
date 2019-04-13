#!/usr/bin/python3
# -*- coding: utf-8 -*-

from mindpong.view.PlayTab import PlayTab
from mindpong.view.SettingsTab import SettingsTab
from mindpong.view.AnalysisTab import AnalysisTab
from mindpong.model.services.historyreaderutils import get_available_games
from mindpong.model.game import Game, GameState
from mindpong.utils import get_project_root
from mindpong.view.utils import MINDPONG_TITLE

import sys
import os
import emoji
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class MainMenu(QMainWindow):

    DEFAULT_MENU_HEIGHT = 800
    DEFAULT_MENU_WIDTH = 640
    PLAY_TAB_INDEX = 1
    SETTINGS_TAB_INDEX = 2

    def __init__(self):
        super().__init__()
        # attributes:
        self._logoPath = os.path.sep.join([get_project_root(), 'img_src', 'logo_polyCortex.png'])
        self.centralWidget = QWidget()
        self.tabWidget = QTabWidget()
        self.vBoxLayout = QVBoxLayout()
        self.analysisTab = AnalysisTab()
        self.playTab = PlayTab()
        self.settingsTab = SettingsTab()
        # init methods
        self.init_ui()
        self.tabWidget.currentChanged.connect(self.onChange)


    @property
    def current_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def logo_path(self):
        return self._logoPath

    def init_ui(self):
        self.init_tabs()
        self.vBoxLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.vBoxLayout)
        self.resize(MainMenu.DEFAULT_MENU_HEIGHT, MainMenu.DEFAULT_MENU_WIDTH)
        self.showMaximized()
        self.setWindowTitle(MINDPONG_TITLE)
        self.setWindowIcon(QIcon(self._logoPath))

    def init_tabs(self):
        self.tabWidget.addTab(self.playTab, emoji.emojize(":video_game: Play  "))
        self.tabWidget.addTab(self.analysisTab, "📊 Analysis")
        self.tabWidget.addTab(self.settingsTab, emoji.emojize(" ⚙ Settings"))
        self.tabWidget.setStyleSheet("QTabBar::tab { height: 50px; width: 300px}")
        

    def set_delegate(self, delegate):
        self.delegate = delegate
        self.playTab.set_delegate(delegate)
        self.analysisTab.set_delegate(delegate)
        self.settingsTab.set_delegate(delegate)

    def closeEvent(self, event):
        self.delegate.end_game()
    
    def onChange(self, tab_idx):
        if tab_idx == self.PLAY_TAB_INDEX:
            self.analysisTab.populate_game_selector()
        elif tab_idx == self.SETTINGS_TAB_INDEX:
            self.settingsTab.populate_fields()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    sys.exit(app.exec_())
