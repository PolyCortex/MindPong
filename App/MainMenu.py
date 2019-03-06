#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
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
        self._currentDirectory = os.path.dirname(os.path.realpath(__file__))
        self._logoPath = self._currentDirectory + os.path.sep + 'Images' + os.path.sep + 'logo_polyCortex.png'
        self.init_ui()
        self.settingTab = None
        self.playTab = None
        self.statsTab = None

    @property
    def current_directory(self):
        return self._currentDirectory

    @property
    def logo_path(self):
        return self._logoPath

    def center_menu(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def init_ui(self):
        self.center_menu()
        self.resize(MainMenu.DEFAULT_MENU_HEIGHT, MainMenu.DEFAULT_MENU_WIDTH)
        self.setWindowTitle('MindPong')
        self.setWindowIcon(QIcon(self._logoPath))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    sys.exit(app.exec_())
