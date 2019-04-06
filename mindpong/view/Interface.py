import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
#import pyqtgraph.examples
#pyqtgraph.examples.run()


app = QtGui.QApplication([])
view = pg.GraphicsView()
l = pg.GraphicsLayout(border=(100,100,100))
view.setCentralItem(l)
view.show()
view.setWindowTitle('Pymuse')
view.resize(800,600)

text=('Voici la page de jeu pour le pymuse. Cest encore un essaie, bla bla bla')

l.addLabel(text, col = 0, colspan = 4)
l.nextRow()

p1 = l.addLabel('decompte')
p2 = l.addLabel('resultat')
vb = l.addViewBox(lockAspect=True)
img = pg.ImageItem(np.random.normal(size=(100,100)))
vb.addItem(img)
vb.autoRange()

l.nextRow()
l2 = l.addLayout(colspan=3, border=(50,0,0))
l2.setContentsMargins(10, 10, 10, 10)
l2.addLabel("voici le graphique montrant les 2 participants", colspan=3)
l2.nextRow()
l2.addLabel('Montre le niveau de concentration', angle=-90, rowspan=2)
p21 = l2.addPlot(title="Multiple curves")
curve1 = p21.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
curve2 = p21.plot(np.random.normal(size=110)+5, pen=(51,255,153), name="Green curve")
data1 = np.random.normal(size=(10,50))
data2 = np.random.normal(size=(10,50))
ptr = 0
l2.nextRow()
l2.addLabel("Montre le temps", col=1, colspan=2)
##end of participant graph flow

started = 0

## button
proxy = QtGui.QGraphicsProxyWidget()
button = QtGui.QPushButton('play game')
proxy.setWidget(button)


l.nextRow()
l3 = l.addLayout(colspan=3, border=(50,0,0))
p4 = l3.addLabel('green : player 1 <br> red: player2')
p5 = l3.addItem(proxy)




# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


def update():
    global curve1, data1, ptr, p2
    global curve2, data2, ptr, p2
    curve1.setData(data1[ptr % 10])
    curve2.setData(data2[ptr % 10])
    if ptr == 0:
        p2.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1

if started == 1:
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()
