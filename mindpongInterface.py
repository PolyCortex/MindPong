import sys
from PyQt4 import QtGui, QtCore
import time
import serial
import pexpect

MUSES = {'Muse 1': 'Muse-0CCD', 'Muse 2': 'Muse-201E', 'Muse 3': 'Muse-4E4E', 'Muse 4': 'Muse-7F68'}

class MindpongInterface(QtGui.QMainWindow):
    change_images = QtCore.pyqtSignal(float, float)

    def __init__(self):
        super(MindpongInterface, self).__init__()
        self.setWindowTitle("MindPong")
        self.home()
        self.borneMin = 0.05
        self.borneMax = 0.4

    def home(self):
        # Define dimensions - Only works on windows ...
        #user32 = ctypes.windll.user32
        #user32.SetProcessDPIAware()
        #[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        [w, h] = [1300, 700]
        [w_btn, h_btn] = [100, 30]
        # Create labels
        self.speed1_label = QtGui.QLabel(self)
        self.speed1_pixmap = QtGui.QPixmap("./images/j1_0.gif")
        self.speed1_pixmap_1 = QtGui.QPixmap("./images/j1_1.gif")
        self.speed1_pixmap_2 = QtGui.QPixmap("./images/j1_2.gif")
        self.speed1_pixmap_3 = QtGui.QPixmap("./images/j1_3.gif")
        self.speed1_pixmap_4 = QtGui.QPixmap("./images/j1_4.gif")
        self.speed1_pixmap_5 = QtGui.QPixmap("./images/j1_5.gif")
        self.speed1_pixmap_6 = QtGui.QPixmap("./images/j1_6.gif")
        self.speed1_label.setPixmap(self.speed1_pixmap)
        self.speed1_label.resize(self.speed1_pixmap.width(), self.speed1_pixmap.height())
        self.speed1_label.move(w/4-600/2, h/2-600/2)
        self.speed2_label = QtGui.QLabel(self)
        self.speed2_pixmap = QtGui.QPixmap("./images/j2_0.gif")
        self.speed2_pixmap_1 = QtGui.QPixmap("./images/j2_1.gif")
        self.speed2_pixmap_2 = QtGui.QPixmap("./images/j2_2.gif")
        self.speed2_pixmap_3 = QtGui.QPixmap("./images/j2_3.gif")
        self.speed2_pixmap_4 = QtGui.QPixmap("./images/j2_4.gif")
        self.speed2_pixmap_5 = QtGui.QPixmap("./images/j2_5.gif")
        self.speed2_pixmap_6 = QtGui.QPixmap("./images/j2_6.gif")
        self.speed2_label.setPixmap(self.speed2_pixmap)
        self.speed2_label.resize(self.speed2_pixmap.width(), self.speed2_pixmap.height())
        self.speed2_label.move(3*w/4-600/2, h/2-600/2)
        # Create buttons
        self.exit_btn = QtGui.QPushButton("Quitter", self)
        self.exit_btn.resize(w_btn, h_btn)
        self.exit_btn.move(w/2-w_btn/2, h-2*h_btn)

        self.Combo1 = QtGui.QComboBox(self)
        self.Combo1.setObjectName("Muse Gauche")
        for muse_name in MUSES:
            self.Combo1.addItem(muse_name)
        self.Combo1.resize(w_btn, h_btn)
        self.Combo1.move(w / 4 - 1 * w_btn / 2, h - 1 * h_btn)

        self.connect1_btn = QtGui.QPushButton("Connecter J1", self)
        self.connect1_btn.resize(w_btn, h_btn)
        self.connect1_btn.move(w/4-3*w_btn/2, h-2*h_btn)
        self.unconnect1_btn = QtGui.QPushButton("Deconnecter J1", self)
        self.unconnect1_btn.resize(w_btn, h_btn)
        self.unconnect1_btn.move(w/4+w_btn/2, h-2*h_btn)
        self.unconnect1_btn.setDisabled(True)

        self.Combo2 = QtGui.QComboBox(self)
        self.Combo2.setObjectName("Muse Gauche")
        for muse_name in MUSES:
            self.Combo2.addItem(muse_name)
        self.Combo2.resize(w_btn, h_btn)
        self.Combo2.move(3*w / 4 - 1 * w_btn / 2, h - 1 * h_btn)

        self.connect2_btn = QtGui.QPushButton("Connecter J2", self)
        self.connect2_btn.resize(w_btn, h_btn)
        self.connect2_btn.move(3*w/4-3*w_btn/2, h-2*h_btn)
        self.unconnect2_btn = QtGui.QPushButton("Deconnecter J2", self)
        self.unconnect2_btn.resize(w_btn, h_btn)
        self.unconnect2_btn.move(3*w/4+w_btn/2, h-2*h_btn)
        self.unconnect2_btn.setDisabled(True)

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
        self.connect1_btn.clicked.connect(self.cb_connect1)
        self.unconnect1_btn.clicked.connect(self.cb_unconnect1)
        self.connect2_btn.clicked.connect(self.cb_connect2)
        self.unconnect2_btn.clicked.connect(self.cb_unconnect2)
        self.change_images.connect(self.update_data_Ard)

        # variables
        self.connexion_muse_P1 = None
        self.connexion_muse_P2 = None
        self.serial_channel = None
        self.port = 'COM1'  # arduino port, this line must be changed depending on the computer
        self.baud = 9600

        # Display window
        self.showFullScreen()

    def cb_close_app(self):
        # Make sure the Muse are disconnected
        # Close the GUI
        if self.connexion_muse_P1 is not None:
            self.connexion_muse_P1.sendcontrol('c')
            self.connexion_muse_P1 = None
        if self.connexion_muse_P2 is not None:
            self.connexion_muse_P2.sendcontrol('c')
            self.connexion_muse_P2 = None
        if self.serial_channel is not None:
            self.serial_channel.close()
        sys.exit()

    def cb_play(self):
        # Callback for when the game starts
        # Needs to update self.speedX_label when speed is changed. This is done by loading "jX_Y.gif" and displaying it,
        # with Y representing the speed level.
        # Needs to constantly update the connection status, which is, for each player, the text shown in the top corners
        # of the screen as "0 0 0 0 0 - 100%" initially. The 5 zeros represent the contact of the 5 electrodes, and
        # the 100% represents the battery life.
        # Needs to run for a set amount of time OR until a player has activated the contact detector at the finish line
        # At the end of execution, needs to put back the GUI in its initial state whilst keeping the Muse connected
        # Also, should verify if both Muse are connected or just one, since the game should be playable alone if needed
        # init port
        try:
            self.serial_channel = serial.Serial()
            self.serial_channel.port = self.port
            self.serial_channel.baudrate = self.baud
            self.serial_channel.readable()
            self.serial_channel.timeout = 1
            # open port
            self.serial_channel.open()
            # print(ser.is_open)
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

    def cb_connect1(self):
        # Needs to connect Muse to the program here
        # Verify that the connection is good
        # If the connection has failed, show an error message
        # If the connection is successful, disable the connect button and activate the unconnect one
        connect_status = ['================== Muse Status ==================', 'Connection failure 5', pexpect.EOF, pexpect.TIMEOUT]

        muse_P1 = MUSES[str(self.Combo1.currentText())]
        cmd = 'muse-io --osc osc.udp://localhost:5001 --device ' + muse_P1
        #cmd = ['muse-io', '--osc', 'osc.udp://localhost:5001', '--device', muse_P1]
        print cmd

    def cb_unconnect1(self):
        # Needs to disconnect the Muse and verify that the ports have been closed
        # If the disconnection is successful, disable the unconnect button and activate the connect one
        self.connexion_muse_P1.sendcontrol('c')
        self.connexion_muse_P1 = None
        print 'Killed process Muse P1'

        self.Combo1.setEnabled(True)
        self.connect1_btn.setEnabled(True)
        self.unconnect1_btn.setDisabled(True)
        self.connect1_btn.setStyleSheet("background-color: gray")

    def cb_connect2(self):
        # Needs to connect Muse to the program here
        # Verify that the connection is good
        # If the connection has failed, show an error message
        # If the connection is successful, disable the connect button and activate the unconnect one
        connect_status = ['================== Muse Status ==================', 'Connection failure 5', pexpect.EOF, pexpect.TIMEOUT]

        muse_P2 = MUSES[str(self.Combo2.currentText())]
        cmd = 'muse-io --osc osc.udp://localhost:5002 --device ' + muse_P2
        print cmd

    def cb_unconnect2(self):
        # Needs to disconnect the Muse and verify that the ports have been closed
        # If the disconnection is successful, disable the unconnect button and activate the connect one
        self.connexion_muse_P2.sendcontrol('c')
        self.connexion_muse_P2 = None
        print 'Killed process Muse P2'

        self.Combo2.setEnabled(True)
        self.connect2_btn.setEnabled(True)
        self.unconnect2_btn.setDisabled(True)
        self.connect2_btn.setStyleSheet("background-color: gray")

    @QtCore.pyqtSlot(float, float)
    def update_data_Ard(self, dataP1, dataP2):
        if not self.is_playing:
            print 'APPUYER SUR PLAY'
            return

        if 0.0 <= dataP1 < 0.05:
            self.speed1_label.setPixmap(self.speed1_pixmap)
        if 0.05 <= dataP1 < 0.1:
            self.speed1_label.setPixmap(self.speed1_pixmap_1)
        if 0.1 <= dataP1 < 0.2:
            self.speed1_label.setPixmap(self.speed1_pixmap_2)
        if 0.2 <= dataP1 < 0.3:
            self.speed1_label.setPixmap(self.speed1_pixmap_3)
        if 0.3 <= dataP1 < 0.5:
            self.speed1_label.setPixmap(self.speed1_pixmap_4)
        if 0.5 <= dataP1 <= 0.8:
            self.speed1_label.setPixmap(self.speed1_pixmap_5)
        if 0.8 <= dataP1 <= 1:
            self.speed1_label.setPixmap(self.speed1_pixmap_6)

        if 0.0 <= dataP2 < 0.05:
            self.speed2_label.setPixmap(self.speed2_pixmap)
        if 0.05 <= dataP2 < 0.1:
            self.speed2_label.setPixmap(self.speed2_pixmap_1)
        if 0.1 <= dataP2 < 0.2:
            self.speed2_label.setPixmap(self.speed2_pixmap_2)
        if 0.2 <= dataP2 < 0.3:
            self.speed2_label.setPixmap(self.speed2_pixmap_3)
        if 0.3 <= dataP2 < 0.5:
            self.speed2_label.setPixmap(self.speed2_pixmap_4)
        if 0.5 <= dataP2 <= 0.8:
            self.speed2_label.setPixmap(self.speed2_pixmap_5)
        if 0.8 <= dataP2 <= 1:
            self.speed2_label.setPixmap(self.speed2_pixmap_6)

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