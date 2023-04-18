from PyQt6.QtWidgets import QPushButton, QDialog, QLabel, QGridLayout
from PyQt6.QtCore import Qt


class MessageDialog(QDialog):
    """
    A general message dialog.
    """

    def __init__(self, parent=None, title="", message=""):
        """
        Inintializes the dialog with the given title and message.
        """
        super().__init__(parent)
        self.setWindowTitle(title)

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
