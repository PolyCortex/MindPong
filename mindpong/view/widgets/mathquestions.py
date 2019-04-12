from PyQt5.QtGui import QPixmap, QPainter, QTransform, QBrush, QColor, QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QSize, QRect

MODES = ['DRILL', 'GAP']

QUESTIONS = {
    MODES[0]: "Question: Resolve the following equation",
    MODES[1]: "Question: Fill the gap with the the following operators: (+ - x %)"
}

class MathQuestions(QWidget):

    BOTTOM_MARGIN = 60
    BACKGROUND_COLOR_CODE = '#cfdef7'

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.height() - self.BOTTOM_MARGIN)
        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Question Label
        math_question = QLabel(QUESTIONS[MODES[0]])
        math_question.setFont(QFont("Times", 18, QFont.Bold))
        math_question.setMargin(70)
        math_question.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.grid.addWidget(math_question, 0, 0, 1, 1, (Qt.AlignHCenter))

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

