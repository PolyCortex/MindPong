from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QScrollArea

class Scroller(QScrollArea):

    def __init__(self):
        super().__init__()

    def wheelEvent(self, ev):
        if ev.type() == QEvent.Wheel:
            ev.ignore()
