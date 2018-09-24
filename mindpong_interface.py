import sys
from PyQt4 import QtGui, QtCore
import time
import pexpect
import math

from services.serial_communication_service import SerialCommunicationService

class MindpongInterface(QtGui.QMainWindow):
    LOWER_BOUND = 0.05
    UPPER_BOUND = 0.4
    change_images = QtCore.pyqtSignal(list)

    def __init__(self):
        super(MindpongInterface, self).__init__()
        self.setWindowTitle("MindPong")
        self.home()
        self.serial_communication_service = SerialCommunicationService()

    def create_gauge(self, index, position):
        pixmaps = [QtGui.QPixmap("./images/j" + str(index + 1) + "_" + str(x) + ".png") for x in range(7)]
        gauge = { 'label': QtGui.QLabel(self), 'pixmaps': pixmaps }
        gauge['label'].setPixmap(pixmaps[0])
        gauge['label'].resize(pixmaps[0].width(), pixmaps[0].height())
        gauge['label'].move(position[0], position[1])
        return gauge

    def home(self):
        # Define dimensions - Only works on windows ...
        #user32 = ctypes.windll.user32
        #user32.SetProcessDPIAware()
        #[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        [w, h] = [1300, 700]
        [w_btn, h_btn] = [100, 30]
        # Create labels
        self.gauges = [
            self.create_gauge(index, position) 
            for index, position in enumerate([(w/4-300, h/2-300), (3*w/4-300, h/2-300)])
        ] 

        # Create buttons
        self.exit_btn = QtGui.QPushButton("Quitter", self)
        self.exit_btn.resize(w_btn, h_btn)
        self.exit_btn.move(w/2-w_btn/2, h-2*h_btn)

        self.play_btn = QtGui.QPushButton("Jouer", self)
        self.play_btn.resize(w_btn, h_btn)
        self.play_btn.move(w/2-w_btn/2, h/2)
        self.is_playing = False

        self.stop_btn = QtGui.QPushButton("Stop", self)
        self.stop_btn.resize(w_btn, h_btn)
        self.stop_btn.move(w / 2 - w_btn / 2, h / 2 + 2 * h_btn)
        self.stop_btn.setDisabled(True)

        # Associate callbacks
        self.exit_btn.clicked.connect(self.cb_close_app)
        self.play_btn.clicked.connect(self.cb_play)
        self.stop_btn.clicked.connect(self.cb_stop)
        self.change_images.connect(self.send_data_arduino)
        self.change_images.connect(self.update_gauges)

        self.showFullScreen()

    def cb_close_app(self):
        self.serial_communication_service.close_communication()
        sys.exit()

    def cb_play(self):
        try:
            self.serial_communication_service.establish_communication()
        except Exception as e:
            self.is_playing = False
            self.play_btn.setStyleSheet("background-color: red")
            return

        self.is_playing = True
        self.play_btn.setStyleSheet("background-color: green")
        self.play_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)

    def cb_stop(self):
        self.serial_communication_service.close_communication()
        self.is_playing = False
        self.play_btn.setStyleSheet("background-color: grey")
        self.stop_btn.setDisabled(True)
        self.play_btn.setEnabled(True)

    @QtCore.pyqtSlot(list)
    def update_gauges(self, relative_beta_list):
        if not self.is_playing:
            return

        for index, relative_beta in enumerate(relative_beta_list):
            pixmap_index = int(relative_beta * 7)
            self.gauges[index]['label'].setPixmap(
                self.gauges[index]['pixmaps'][pixmap_index]
            )


    @QtCore.pyqtSlot(list)
    def send_data_arduino(self, relative_beta_list):
        if not self.is_playing or self.serial_communication_service.serial_channel is None:
            return

        sent_value = ""
        for relative_beta in relative_beta_list:
            relative_beta = self.LOWER_BOUND if relative_beta < self.LOWER_BOUND else relative_beta
            relative_beta = self.UPPER_BOUND if relative_beta > self.UPPER_BOUND else relative_beta
            sent_value += str(100 + int((relative_beta - self.LOWER_BOUND)/(self.UPPER_BOUND - self.LOWER_BOUND) * 255))

        try:
            print 'Reading', self.serial_communication_service.read_data()
            print 'Sending', sent_value
            self.serial_communication_service.send_data(sent_value)
            time.sleep(1)
        except Exception as e:
            print 'Error when sending data to microcontroller:', str(e)
            self.is_playing = False
