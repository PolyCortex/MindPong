from PyQt5.QtWidgets import QTabWidget


class SettingsTab(QTabWidget):

    def __init__(self):
        super().__init__()

    def set_delegate(self, delegate):
        self.delegate = delegate

