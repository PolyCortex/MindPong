from PyQt5.QtGui import QPixmap, QPainter, QTransform, QBrush, QColor, QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QSize, QRect

from mindpong.model.mathexercise import MathMode

class MathQuestions(QWidget):

    BOTTOM_MARGIN = 0
    BACKGROUND_COLOR_CODE = '#cfdef7'

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.height() - self.BOTTOM_MARGIN)
        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self._set_labels()

    def _set_labels(self):
        # Question Label
        self._math_question = QLabel("Initializing...")
        self._math_question.setFont(QFont("Times", 16, QFont.Bold))
        self._math_question.setMargin(70)
        self._math_question.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.grid.addWidget(self._math_question)

        # Equation label
        self._equation_label = QLabel("Initializing...")
        self._equation_label.setFont(QFont("Times", 35, QFont.Bold))
        self._equation_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.grid.addWidget(self._equation_label, 1, 0)

    def set_delegate(self, delegate):
        self.delegate = delegate
        self._link_model()

    def _link_model(self):
        self._math_question.setText(self.delegate.game.math_exercices.get_question())
        self._equation_label.setText(self.delegate.game.math_exercices.get_equation())
    
    def sizeHint(self):
        return QSize(self.width(), self.height())

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        color = QColor()
        color.setNamedColor(self.BACKGROUND_COLOR_CODE)
        painter.setBrush(QBrush(color, Qt.Dense2Pattern))
        painter.setPen(Qt.darkBlue)
        painter.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3);

        painter.end()

