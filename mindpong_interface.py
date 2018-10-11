import sys
from PyQt4 import QtGui, QtCore
import pexpect
import math

from services.arduino_communication_service import arduino_communication_service
from constants import BACKGROUND_COLORS, WINDOW_SIZE, BUTTON_SIZE

class MindpongInterface(QtGui.QMainWindow):
    change_images = QtCore.pyqtSignal(list)

    def __init__(self):
        super(MindpongInterface, self).__init__()
        self.setWindowTitle("MindPong")
        self.home()

    def home(self):
        # Define dimensions - Only works on windows ...
        #user32 = ctypes.windll.user32
        #user32.SetProcessDPIAware()
        #[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        [w, h] = [WINDOW_SIZE["W"], WINDOW_SIZE["H"]]

        self.gauges = [
            self.create_gauge(index, position) 
            for index, position in enumerate([(w/4-300, h/2-300), (3*w/4-300, h/2-300)])
        ] 
        self.create_buttons()
        self.connect_interface_callbacks()
        self.showFullScreen()

    def create_gauge(self, index, position):
        pixmaps = [QtGui.QPixmap("./images/j" + str(index + 1) + "_" + str(x) + ".png") for x in range(7)]
        gauge = { 'label': QtGui.QLabel(self), 'pixmaps': pixmaps }
        gauge['label'].setPixmap(pixmaps[0])
        gauge['label'].resize(pixmaps[0].width(), pixmaps[0].height())
        gauge['label'].move(position[0], position[1])
        return gauge

    def create_buttons(self):
        [w_btn, h_btn] = [BUTTON_SIZE["W"], BUTTON_SIZE["H"]]
        [w, h]         = [WINDOW_SIZE["W"], WINDOW_SIZE["H"]]

        self.exit_btn = self.create_button("Quitter", w/2-w_btn/2, h-2*h_btn)
        self.play_btn = self.create_button("Jouer",   w/2-w_btn/2, h/2)
        self.stop_btn = self.create_button("Stop",    w/2-w_btn/2, h/2+2*h_btn)
        self.stop_btn.setDisabled(True)

    def create_button(self, label, position_x, position_y):
        btn = QtGui.QPushButton(label, self)
        btn.resize(BUTTON_SIZE["W"], BUTTON_SIZE["H"])
        btn.move(position_x, position_y)
        return btn
    
    def connect_interface_callbacks(self):
        self.exit_btn.clicked.connect(self.cb_close_app)
        self.play_btn.clicked.connect(self.cb_play)
        self.stop_btn.clicked.connect(self.cb_stop)
        self.change_images.connect(self.update_gauges)

    def cb_close_app(self):
        arduino_communication_service.close_communication()
        sys.exit()

    def cb_play(self):
        try:
            arduino_communication_service.establish_communication()
        except Exception as e:
            self.play_btn.setStyleSheet(BACKGROUND_COLORS["RED"])
            return
        self.play_btn.setStyleSheet(BACKGROUND_COLORS["GREEN"])
        self.play_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)

    def cb_stop(self):
        arduino_communication_service.close_communication()
        self.play_btn.setStyleSheet(BACKGROUND_COLORS["GREY"])
        self.stop_btn.setDisabled(True)
        self.play_btn.setEnabled(True)

    @QtCore.pyqtSlot(list)
    def update_gauges(self, relative_beta_list):
        if not arduino_communication_service.is_connected:
            return

        for index, relative_beta in enumerate(relative_beta_list):
            pixmap_index = int(relative_beta * 7)
            self.gauges[index]['label'].setPixmap(
                self.gauges[index]['pixmaps'][pixmap_index]
            )