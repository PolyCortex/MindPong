from collections import deque

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QTabWidget, QGridLayout, QGroupBox, QLabel


#import pyqtgraph.examples
#pyqtgraph.examples.run()


class PlayTab(QTabWidget):

    def __init__(self):
        super().__init__()
        self.plotWidget = PlotWidget()
        self.init_ui()

    def init_ui(self):
        parent_layout = QGridLayout()
        parent_layout.addWidget(self.plotWidget)
        self.add_sub_layout(parent_layout)
        self.setLayout(parent_layout)

    def add_sub_layout(self, parent_layout):
        label = QLabel("allo")
        layout = QGridLayout()
        layout.addWidget(label)
        group_box = QGroupBox()
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)


class PlotWidget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.q =np.random.random(200)
        plot = pg.PlotWidget()
        layout.addWidget(plot)
        self.curve = plot.plot(self.q)

    def update(self):
        self.curve.setData(self.q)

