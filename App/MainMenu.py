#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from App.PlayTab import PlayTab
from App.SettingsTab import SettingsTab
from App.StatsTab import StatsTab
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
import sys


class MainMenu(QMainWindow):

    # Class attributes/constants
    Y_COORD_UPPER_BOUND = 1080  # random value based on my screen dimensions
    X_COORD_UPPER_BOUND = 1920  # random value based on my screen dimensions
    DEFAULT_MENU_HEIGHT = 800
    DEFAULT_MENU_WIDTH = 640

    def __init__(self):
        super().__init__()
        # attributes:
        self._currentDirectory = os.path.dirname(os.path.realpath(__file__))
        self._logoPath = self._currentDirectory + os.path.sep + 'Images' + os.path.sep + 'logo_polyCortex.png'
        self.centralWidget = QWidget()
        self.tabWidget = QTabWidget()
        self.vBoxLayout = QVBoxLayout()
        self.statsTab = StatsTab()
        self.playTab = PlayTab()
        self.settingsTab = SettingsTab()
        # init methods
        self.init_ui()

    @property
    def current_directory(self):
        return self._currentDirectory

    @property
    def logo_path(self):
        return self._logoPath

    def center_menu(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        size = self.geometry()
        print(size)
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def init_ui(self):
        self.init_tabs()
        self.vBoxLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.vBoxLayout)
        self.resize(MainMenu.DEFAULT_MENU_HEIGHT, MainMenu.DEFAULT_MENU_WIDTH)
        self.center_menu()
        self.setWindowTitle('MindPong')
        self.setWindowIcon(QIcon(self._logoPath))
        self.show()

    def init_tabs(self):
        self.tabWidget.addTab(self.statsTab, "Statistics")
        self.tabWidget.addTab(self.playTab, "Play")
        self.tabWidget.addTab(self.settingsTab, "Settings")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    sys.exit(app.exec_())
