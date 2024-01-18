import sys
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QResizeEvent, QCursor

from PyQt6.QtWidgets import (QLineEdit, QTextEdit,QApplication, QFileDialog, QGridLayout, QLabel, QMainWindow,
     QMenu, QPushButton, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt, QSize, QRect, QEvent

# Create the app's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediaGrapher")
        self.resize(500,350) #width, height
    
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.inputField = QLineEdit()

        #Button to run script
        button = QPushButton("Download and Graph Image/Video")
        button.clicked.connect(self.close) #close window for now, implement logic for button later
        
        #self.setCentralWidget(button)
        layout.addWidget(self.inputField)
        layout.addWidget(button)
        self.show()

    def resizeEvent (self, event: QtGui.QResizeEvent) -> None:
        QMainWindow.resizeEvent(self, event)


# Create the app, the main window, and run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

