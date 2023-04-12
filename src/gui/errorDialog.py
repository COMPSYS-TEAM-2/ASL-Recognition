from PyQt6.QtWidgets import QPushButton, QDialog, QLabel, QGridLayout
from PyQt6.QtCore import Qt


class ErrorDialog(QDialog):
    # Dialog to train the database
    def __init__(self,message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error!")

        self.mainLayout = QGridLayout()

        self.errorLbl = QLabel(f"{message}")
        self.mainLayout.addWidget(
            self.errorLbl, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.okBtn = QPushButton("Ok")
        self.okBtn.clicked.connect(self.close)
        self.mainLayout.addWidget(
            self.okBtn, 1, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.mainLayout)
        self.show()
