import sys
import subprocess
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QResizeEvent, QCursor

from PyQt6.QtWidgets import (QMenu, QLineEdit, QTextEdit,QApplication, QFileDialog, QGridLayout, QLabel, QMainWindow,
     QMenu, QPushButton, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt, QSize, QRect, QEvent

# Create the app's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("MediaGrapher")
        self.resize(500,350) #width, height

        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)

        self.initMenu()
        self.initInputField()
        self.initScriptButton()

        self.show()
        
    def initMenu(self):
        #Set Parameters
        setParametersAct = QAction('&Set Parameters', self)
        setParametersAct.triggered.connect(self.setParameters)

        #Exit Action
        exitAct = QAction('&Exit', self)
        exitAct.triggered.connect(self.close)

        #Menu Bar
        menuBar = self.menuBar()
        menuMediaGrapher = menuBar.addMenu("Media Grapher")
        menuMediaGrapher.addAction(setParametersAct)
        menuMediaGrapher.addAction(exitAct)

    def initInputField(self):
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter URL for Image/Video")
        self.layout.addWidget(self.inputField)

    def initScriptButton(self):
        #Button to run script
        button = QPushButton("Download and Graph Image/Video")
        #button.clicked.connect(self.close) #close window for now, implement logic for button later
        button.clicked.connect(self.runScript)
        self.layout.addWidget(button)
    
    def runScript(self):
        try:
            subprocess.run(["python", "mediagrapher.py", self.inputField.text()])
        except Exception as e:
            print(f"Error running script: {e}")

    def resizeEvent (self, event: QtGui.QResizeEvent) -> None:
        QMainWindow.resizeEvent(self, event)
    
    def setParameters(self):
        #https://www.pythonguis.com/tutorials/pyqt6-creating-multiple-windows/
        pass

class settingWindow(QWidget):
    def __init__(self):
        super().__init__()
        
# Create the app, the main window, and run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

