import sys
from PyQt4 import QtGui, QtCore
import time
import serial
import pexpect

class MindpongInterface(QtGui.QMainWindow):
    change_images = QtCore.pyqtSignal(float, float)

    def __init__(self):
        super(MindpongInterface, self).__init__()
        self.setWindowTitle("MindPong")
        self.home()
        self.borneMin = 0.05
        self.borneMax = 0.4

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
        self.change_images.connect(self.update_data_Ard)

        # variables
        self.serial_channel = None
        self.port = 'COM6'  # arduino port, this line must be changed depending on the computer
        self.baud = 9600

        self.showFullScreen()

    def cb_close_app(self):
        if self.serial_channel is not None:
            self.serial_channel.close()
        sys.exit()

    def cb_play(self):
        try:
            self.serial_channel = serial.Serial()
            self.serial_channel.port = self.port
            self.serial_channel.baudrate = self.baud
            self.serial_channel.readable()
            self.serial_channel.timeout = 1
            self.serial_channel.open()
        except Exception as e:
            print e
            print 'could not connect to port ' + self.port
            self.is_playing = False
            self.play_btn.setStyleSheet("background-color: red")
            return

        self.is_playing = True
        self.play_btn.setStyleSheet("background-color: green")
        self.play_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)

    def cb_stop(self):
        self.is_playing = False
        if self.serial_channel is not None:
            self.serial_channel.close()
        self.play_btn.setStyleSheet("background-color: grey")
        self.stop_btn.setDisabled(True)
        self.play_btn.setEnabled(True)

    def update_gauges(self, data, index):
        if 0.0 <= data < 0.05:
            self.gauges[index]['label'].setPixmap(self.gauges[index]['pixmaps'][0])
        if 0.05 <= data < 0.1:
            self.gauges[index]['label'].setPixmap(self.gauges[index]['pixmaps'][1])
        if 0.1 <= data < 0.2:
            self.gauges[index]['label'].setPixmap(self.gauges[index]['pixmaps'][2])
        if 0.2 <= data < 0.3:
            self.gauges[index]['label'].setPixmap(self.gauges[index]['pixmaps'][3])
        if 0.3 <= data < 0.5:
            self.gauges[index]['label'].setPixmap(self.gauges[index]['pixmaps'][4])
        if 0.5 <= data <= 0.8:
            self.gauges[index]['label'].setPixmap(self.gauges[index]['pixmaps'][5])
        if 0.8 <= data <= 1:
            self.gauges[index]['label'].setPixmap(self.gauges[index]['pixmaps'][6])

    @QtCore.pyqtSlot(float, float)
    def update_data_Ard(self, dataP1, dataP2):
        if not self.is_playing:
            print 'APPUYER SUR PLAY'
            return
            
        self.update_gauges(dataP1, 0)
        self.update_gauges(dataP2, 1)

        if self.serial_channel is not None: 
            if dataP1 < self.borneMin:
                dataP1 = self.borneMin
            if dataP2 < self.borneMin:
                dataP2 = self.borneMin

            if dataP1 > self.borneMax:
                dataP1 = self.borneMax
            if dataP2 > self.borneMax:
                dataP2 = self.borneMax

            DATA1 = (dataP1 - self.borneMin)/(self.borneMax - self.borneMin)
            DATA2 = (dataP2 - self.borneMin)/(self.borneMax - self.borneMin)
            valueP1 = int(100 + DATA1 * 255)
            valueP2 = int(100 + DATA2 * 255)

            try: #Here we only wanna send data no read...
                while self.serial_channel.in_waiting:
                    print 'Received', self.serial_channel.readline()
                # ------------------Decommenter ici pour competitionner avec l ordinateur.--------------
                #valueP2 = 165
                print 'Sending', valueP1, valueP2
                self.serial_channel.write(str(valueP1)+str(valueP2))  # between 100 and 355, this line will wait until message is effectively written on channel.
               
                print('valueP1: ', valueP1, 'valueP2: ', valueP2)
                time.sleep(1)
            except Exception as e:
                print 'Error when sending data to boat P1:', str(e)
                self.is_playing = False

        return