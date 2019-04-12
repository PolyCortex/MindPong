from PyQt5.QtGui import QPixmap, QPainter, QTransform, QBrush, QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize, QRect



class MathQuestions(QWidget):

    BOTTOM_MARGIN = 60
    BACKGROUND_COLOR_CODE = '#cfdef7'

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.height() - self.BOTTOM_MARGIN)

    def sizeHint(self):
        return QSize(self.width(), self.height())

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        color = QColor()
        color.setNamedColor(self.BACKGROUND_COLOR_CODE)
        painter.setBrush(QBrush(color, Qt.Dense2Pattern))
        painter.setPen(Qt.darkBlue);
        painter.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3);

        painter.end()

