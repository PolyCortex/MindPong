
from PyQt5.QtGui import QPixmap, QPainter, QTransform
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize

from mindpong.view.utils import (
    get_image_file)

ARROW_FILE_NAME = 'arrow.png'


class ScalableArrow(QWidget):
    def __init__(self, is_mirrored=False):
        super().__init__()
        self.counter = 0.5
        self.initial_pixmap = QPixmap(get_image_file(ARROW_FILE_NAME))
        self.is_mirrored = is_mirrored
        if is_mirrored:
            self.initial_pixmap = self.initial_pixmap.transformed(
                QTransform().scale(-1, 1))
        self.setFixedHeight(self.initial_pixmap.height()*0.5)
        self.setFixedWidth(self.initial_pixmap.width()*0.5)


    def sizeHint(self):
        return QSize(self.width(), self.height())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawRoundedRect(0,5,self.width()-5, self.height()-7,3,3);
        dest_dimensions = (self.counter * self.initial_pixmap.width(),
                           self.counter * self.initial_pixmap.height())

        print(self.height() / 2, self.initial_pixmap.height()*self.counter / 2)

        dest_position = (self.width() - self.initial_pixmap.width()*self.counter if self.is_mirrored else 0,
                         self.height() / 2 - self.initial_pixmap.height()*self.counter / 2)
        painter.drawPixmap(dest_position[0], dest_position[1], dest_dimensions[0], dest_dimensions[1], self.initial_pixmap.scaled(
            dest_dimensions[0], dest_dimensions[1], transformMode=Qt.SmoothTransformation))
        painter.end()
        self.counter -= 0.01
