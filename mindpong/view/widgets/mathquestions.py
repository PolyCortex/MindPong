from os import path

from PyQt5.QtGui import QPixmap, QPainter, QTransform, QBrush, QColor, QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSize, QRect

from mindpong.model.mathexercise import MathMode

STYLE_SHEET_PATH = path.join(path.dirname(__file__), "styles.css")

class MathQuestions(QWidget):

    BACKGROUND_COLOR_CODE = '#cfdef7'
    INITIALIZING_TITLE = "Initializing..."
    CHECK_ANSWER_BUTTON_TITLE = 'Check Answer'
    NEXT_QUESTION_BUTTON_TITLE = 'Next Question'

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.height() - 10)
        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self._set_labels()
        self._set_configuration_panel()

    def _set_labels(self):
        # Question Label
        self._math_question = QLabel(self.INITIALIZING_TITLE)
        self._math_question.setFont(QFont("Times", 16, QFont.Bold))
        self._math_question.setMargin(70)
        self._math_question.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.grid.addWidget(self._math_question, 0, 0, 1, 1)

        # Equation label
        self._equation_label = QLabel(self.INITIALIZING_TITLE)
        self._equation_label.setFont(QFont("Times", 35, QFont.Bold))
        self.grid.addWidget(self._equation_label, 1, 0, (Qt.AlignCenter))

    def _set_configuration_panel(self):
        self.config_panel_layout = QVBoxLayout()

        # Math mode combo box

        #option.setMaximumWidth(option.width() * 0.3)
        #option.setStyleSheet("padding: 10px 0px; margin: 30px 50px 0px 0px;")

        # Difficulty combo box

        #option.setMaximumWidth(option.width() * 0.3)
        #option.setStyleSheet("padding: 10px 0px; margin: 30px 50px 0px 0px;")

        # Answer and next question button
        self.check_answer_button = QPushButton(self.CHECK_ANSWER_BUTTON_TITLE)
        self.check_answer_button.setMaximumWidth(self.check_answer_button.width() * 0.3)
        self.check_answer_button.setStyleSheet(open(STYLE_SHEET_PATH).read())

        #self.config_panel_layout.addWidget(options[0])
        #self.config_panel_layout.addWidget(options[1])
        self.config_panel_layout.addSpacing(80)
        self.config_panel_layout.addWidget(self.check_answer_button)
        self.grid.addLayout(self.config_panel_layout, 0, 1, 2, 1, (Qt.AlignVCenter))

    def set_delegate(self, delegate):
        self.delegate = delegate
        self._link_model()

    def _link_model(self):
        self._exercice_model = self.delegate.game.math_exercices
        self._math_question.setText(self._exercice_model.get_question())
        self._equation_label.setText(self._exercice_model.get_equation())
    
    def sizeHint(self):
        return QSize(self.width(), self.height())

    def paintEvent(self, e):
        """ paints the background with the blue border """
        painter = QPainter()
        painter.begin(self)
        
        color = QColor()
        color.setNamedColor(self.BACKGROUND_COLOR_CODE)
        painter.setBrush(QBrush(color, Qt.Dense2Pattern))
        painter.setPen(Qt.darkBlue)
        painter.drawRoundedRect(0, 5, self.width()-5, self.height()-7, 3, 3);

        painter.end()

