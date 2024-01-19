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
        self.w = settingWindow()
        setParametersAct = QAction('&Set Parameters', self)
        setParametersAct.setShortcut('Ctrl+P')
        setParametersAct.triggered.connect(self.show_settingWindow)

        #Exit Action
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)

        #Menu Bar
        menuBar = self.menuBar()
        menuMediaGrapher = menuBar.addMenu("Media Grapher")
        menuMediaGrapher.addAction(setParametersAct)
        menuMediaGrapher.addAction(exitAct)

    def show_settingWindow(self, checked):
        #Shows Setting Window
        self.w.show()     

    def initInputField(self):
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter URL for Image/Video")
        self.layout.addWidget(self.inputField)

    def initScriptButton(self):
        #Button to run script
        button = QPushButton("Download and Graph Image/Video")
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.clicked.connect(self.runScript)
        button.setShortcut("Return")
        self.layout.addWidget(button)
    
    def runScript(self):
        try:
            subprocess.run(["python", "mediagrapher.py", self.inputField.text()])
        except Exception as e:
            print(f"Error running script: {e}")

    def resizeEvent (self, event: QtGui.QResizeEvent) -> None:
        print("Resizing")
        #Doesn't change cursor yet
        QMainWindow.setCursor(self, QCursor(Qt.CursorShape.ForbiddenCursor))
        #QMainWindow.resizeEvent(self, event)

    def setParameters(self):
        #https://www.pythonguis.com/tutorials/pyqt6-creating-multiple-windows/
        #self.w = settingWindow()
        pass
        
class settingWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Settings")
        layout.addWidget(self.label)
        self.setLayout(layout)

# Create the app, the main window, and run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

