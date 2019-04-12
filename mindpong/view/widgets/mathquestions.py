from os import path

from PyQt5.QtGui import QPixmap, QPainter, QTransform, QBrush, QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize, QRect

STYLE_SHEET_PATH = path.join(path.dirname(__file__), "style.css")

class MathQuestions(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.height())

    def sizeHint(self):
        return QSize(self.width(), self.height())

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        painter.setBrush(QBrush(QColor(207, 222, 247), Qt.Dense2Pattern))
        painter.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3);

        painter.end()

