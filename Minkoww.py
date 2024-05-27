import sys

import PySide6
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPlainTextEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QFileDialog,
)


class Minkoww_Window(QWidget):
    def __init__(self):
        super(Minkoww_Window, self).__init__()

        self.GRID = QGridLayout()

        self.setWindowTitle("Minkoww")
        self.setMinimumSize(640, 360)
        self.resize(1280, 720)
        self.initUI()

    def initUI(self):
        self.setLayout(self.GRID)


if __name__ == "__main__":
    Minkoww_QApplication = QApplication()
    Minkoww_GUI = Minkoww_Window()
    Minkoww_GUI.show()
    sys.exit(Minkoww_QApplication.exec())
