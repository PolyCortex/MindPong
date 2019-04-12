
from PyQt5.QtGui import QPixmap, QPainter, QTransform
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize, QRect

from mindpong.view.utils import (
    get_image_file)

ARROW_FILE_NAME = 'arrow.png'


class ScalableArrow(QWidget):

    MAX_SCALE = 0.75

    def __init__(self, is_mirrored=False):
        super().__init__()
        self.visible = True
        self._is_mirrored = is_mirrored
        self._arrow_scale = self.MAX_SCALE
        self._init_pixmap()
        self.setFixedHeight(self.initial_pixmap.height()*self._arrow_scale)
        self.setFixedWidth(self.initial_pixmap.width()*self._arrow_scale)

    def _init_pixmap(self):
        self.initial_pixmap = QPixmap(get_image_file(ARROW_FILE_NAME))
        if self._is_mirrored:
            self.initial_pixmap = self.initial_pixmap.transformed(
                QTransform().scale(-1, 1))

    def sizeHint(self):
        return QSize(self.width(), self.height())

    def setWidth(self, scale):
        self._arrow_scale = min(scale*10, self.MAX_SCALE)
        self.update()

    def paintEvent(self, event):
        if self.visible:
            painter = QPainter()
            painter.begin(self)
            
            dest_dimensions = (self._arrow_scale * self.initial_pixmap.width(),
                            self._arrow_scale * self.initial_pixmap.height())

            dest_position = (self.width() - self.initial_pixmap.width()*self._arrow_scale if self._is_mirrored else 0,
                            self.height() / 2 - self.initial_pixmap.height()*self._arrow_scale / 2)

            painter.drawPixmap(dest_position[0], dest_position[1], dest_dimensions[0], dest_dimensions[1], self.initial_pixmap.scaled(
                dest_dimensions[0], dest_dimensions[1], transformMode=Qt.SmoothTransformation))
            painter.end()
