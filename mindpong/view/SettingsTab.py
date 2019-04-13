from PyQt5.QtGui import QFont, QPixmap, QIntValidator
from PyQt5.QtWidgets import (
    QTabWidget, QVBoxLayout, QLabel, 
    QPushButton, QFormLayout, QMessageBox,
    QLineEdit, QComboBox
)

from mindpong.model.serial_communication import SerialCommunication

TITLE_FONT = QFont("Times", 22, QFont.Bold)
SUBTITLE_FONT = QFont("Times", 18, QFont.Bold)
FIELD_FONT = QFont("Times", 12)
BAUD_RATES= ['1200', '2400', '4800', '9600','19200', '38400', '57600', '115200']

class SettingsTab(QTabWidget):

    def __init__(self):
        super().__init__()

        self.delegate = None
        self.registered_widgets = []
        self.centralLayout = QVBoxLayout()
        self.setLayout(self.centralLayout)
        self.port_line_edit_p1 = None
        self.port_line_edit_p2 = None
        self.baud_combo_box = None
        self.port_combo_box = None


    def _init_muse_configs(self):
        muse_label = QLabel("Muse")
        muse_label.setFont(TITLE_FONT)
        self.centralLayout.addWidget(muse_label)

        player_one_label = QLabel("Player One")
        player_one_label.setFont(SUBTITLE_FONT)
        self.centralLayout.addWidget(player_one_label)
        self.port_line_edit_p1 = self._create_player_form_layout("Port :", QIntValidator(1, 65535),  self.delegate.game.players[0].port)

        player_two_label = QLabel("Player Two")
        player_two_label.setFont(SUBTITLE_FONT)
        self.centralLayout.addWidget(player_two_label)
        self.port_line_edit_p2 = self._create_player_form_layout("Port :", QIntValidator(1, 65535),  self.delegate.game.players[1].port)
        self.registered_widgets.extend([muse_label, player_one_label, player_two_label])
    
    def _create_player_form_layout(self, label, validator, current_port):
        form_layout = QFormLayout()

        port_config_label = QLabel(label)
        port_config_label.setFont(FIELD_FONT)
        port_line_edit = QLineEdit()
        port_line_edit.setMaximumWidth(self.width()*0.1)
        port_line_edit.setText(str(current_port))
        if validator is not None:
            port_line_edit.setValidator(validator)
        
        form_layout.addRow(port_config_label, port_line_edit)
        self.registered_widgets.extend([port_config_label, port_line_edit])
        self.centralLayout.addLayout(form_layout)
        return port_line_edit

    def _init_serial_com_configs(self):
        serial_label = QLabel("Serial Communication")
        serial_label.setFont(TITLE_FONT)
        self.centralLayout.addWidget(serial_label)

        # port combo box
        port_form_layout = QFormLayout()
        port_config_label = QLabel("Port: ")
        port_config_label.setFont(FIELD_FONT)
        self.port_combo_box = QComboBox(self)
        self.port_combo_box.setMaximumWidth(self.width()*0.1)
        self.port_combo_box.addItems(self.delegate.serial_communication.get_available_serial_ports())
        self.port_combo_box.setCurrentText(self.delegate.serial_communication.port)
        self.port_combo_box.update()
        port_form_layout.addRow(port_config_label, self.port_combo_box)
        self.centralLayout.addLayout(port_form_layout)

        #baud rate combo box
        baud_form_layout = QFormLayout()
        baud_config_label = QLabel("Baud Rate: ")
        baud_config_label.setFont(FIELD_FONT)
        self.baud_combo_box = QComboBox(self)
        self.baud_combo_box.setMaximumWidth(self.width()*0.1)
        self.baud_combo_box.addItems(BAUD_RATES)
        self.baud_combo_box.setCurrentText(str(self.delegate.serial_communication.baudrate))
        self.baud_combo_box.update()
        baud_form_layout.addRow(baud_config_label, self.baud_combo_box)

        self.centralLayout.addLayout(baud_form_layout)
        self.registered_widgets.extend([serial_label, port_config_label, self.port_combo_box, baud_config_label, self.baud_combo_box])

    def set_delegate(self, delegate):
        self.delegate = delegate
        self.populate_fields()

    def save(self):
        self.delegate.game.players[0].port = int(self.port_line_edit_p1.text())
        self.delegate.game.players[1].port = int(self.port_line_edit_p2.text())
        self.delegate.serial_communication.set_port =self.port_combo_box.currentText()
        self.delegate.serial_communication.baudrate = int(self.baud_combo_box.currentText())
        

    def populate_fields(self):
        # delete all items from layout
        for widget in self.registered_widgets:
            widget.setParent(None)

        self._init_muse_configs()
        self._init_serial_com_configs()
        
        self.save_button = QPushButton('Save settings')
        self.save_button.setMaximumWidth(self.width()*0.08)
        self.save_button.clicked.connect(self.save)
        self.centralLayout.addWidget(self.save_button)
        self.registered_widgets.extend([self.save_button])

