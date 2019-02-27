#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QTabBar
from PyQt5.QtGui import QIcon


class MainMenu(QWidget):
    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    logoPath = currentDirectory + os.path.sep + 'Images' + os.path.sep + 'logo_polyCortex.png'
    def __init__(self):
        super().__init__()
        self.width = 1920
        self.height = 1080
        self.x = 0
        self.y = 100
        self.init_ui()

    def init_ui(self):

        print(self.currentDirectory)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle('MindPong')
        self.setWindowIcon(QIcon(self.logoPath))

        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    sys.exit(app.exec_())
