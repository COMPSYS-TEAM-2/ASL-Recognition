# Therefore the initial window should have buttons to import data or view the dataset
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QMessageBox 
import time

class TrainDialog(QDialog):
    # Dialog to train the database
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Download MNIST and Model Training")
        self.setFixedSize(300, 400)  # TODO Fix size

        # Text edit
        self.textBrowserTrain = QTextBrowser(self)
        self.textBrowserTrain.resize(290, 320)
        self.textBrowserTrain.move(5, 5)

        # Progress Bar
        self.pbar = QProgressBar(self)
        self.pbar.resize(290, 30)
        self.pbar.move(5, 335)
        self.pbar.setMaximum(100)
        self.pbar.setValue(0)
        self.pbar.show()

        self.train_btn.clicked.connect(self.getTrainingPercentage)

        # Cancel Button
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.resize(95, 20)
        self.cancel_btn.move(200, 375)
        self.cancel_btn.clicked.connect(self.close)

    #Function for when trianing starts to make progress on the prog bar 
    def startTraining(self):
        count = 0
        while count != 101 :
            x = count / (100) * 100
            time.sleep(0.02)
            self.pbar.setValue(count)
            count = count + 1
            if count == 100 :
                msg = QMessageBox()
                msg.setText("TRAINING IS COMPLETE")
                msg.setWindowTitle("COMPLETE")
                
                msg.exec()


        
        
    
    #Function that gets the user inputted value which corresponds to the % value of the training set they would like to train
    def getTrainingPercentage(self):
        self.percentage, ok = QInputDialog.getInt(self,"Input Percentage","What Percentage of the training set would you like to train ?")
        
        # if percentage is greater than 100 
        if  self.percentage > 101 :
           
            msg = QMessageBox()
            msg.setText("You cannot training more than 100 percent of the training set.")
            msg.setInformativeText("PERCENTAGE LIMIT EXCEEDED")
            msg.setWindowTitle("ERROR!")
            msg.exec()

        # if percentage is less than 0 
        elif  self.percentage < 0 :
           
            msg = QMessageBox()
            msg.setText("You cannot training less than 1 percent of the training set.")
            msg.setInformativeText("PERCENTAGE MINIMUM EXCEEDED")
            msg.setWindowTitle("ERROR!")
            msg.exec()

        #if valid percentage train the model
        else:
            self.startTraining()
            

        




            
    
    
    
    
        
        
    
        




