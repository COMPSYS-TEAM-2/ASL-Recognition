from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QScrollArea, QFormLayout, QGroupBox
from PyQt6.QtGui import QPixmap


class TestImagesDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("View Testing Images")
        self.setGeometry(0, 0, 950, 500)
        self.scrollArea = QScrollArea(widgetResizable=True)
        self.scrollLayout = QFormLayout()

        groupBox = QGroupBox()
        groupBox.setLayout(self.scrollLayout)

        self.myPixmap = QPixmap("./data/american_sign_language.PNG")
        self.pixmapLabel = QLabel()
        self.pixmapLabel.setPixmap(self.myPixmap)
        self.scrollLayout.addRow(self.pixmapLabel)
        self.labelName = QLabel("MINST Training set")
        self.scrollLayout.addRow(self.labelName)
        self.myPixmap = QPixmap("./data/american_sign_language.PNG")
        self.pixmapLabel = QLabel()
        self.pixmapLabel.setPixmap(self.myPixmap)
        self.scrollLayout.addRow(self.pixmapLabel)
        self.labelName = QLabel("MINST Training set")
        self.scrollLayout.addRow(self.labelName)

        self.scrollArea.setWidget(groupBox)
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)
        self.show()
