
import os
from pathlib import Path

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

def get_project_root() -> Path:
    """Returns project root folder."""
    return os.path.abspath(os.curdir)

def create_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(237, 249, 255))
    palette.setColor(QPalette.PlaceholderText,  QColor(255, 85, 48))
    palette.setColor(QPalette.AlternateBase,    QColor(255, 65, 65))
    palette.setColor(QPalette.ToolTipBase,      Qt.white)

    return palette