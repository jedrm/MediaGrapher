import sys
import subprocess
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QResizeEvent, QCursor

from PyQt6.QtWidgets import (QMenu, QLineEdit, QTextEdit,QApplication, QFileDialog, QGridLayout, QLabel, QMainWindow,
     QMenu, QPushButton, QVBoxLayout, QWidget, QApplication, QDialog, QRadioButton)
from PyQt6.QtCore import Qt, QSize, QRect, QEvent, QSettings

# Create the app's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.getSettingValues()
    
    def getSettingValues(self):
        self.setting_geometry = QSettings('MediaGrapher', 'Window Size')
        self.restoreGeometry(self.setting_geometry.value('Window Size'))

        #self.setting_parameters = QSettings('MediaGrapher', 'Parameters')

    def initUi(self):
        self.setWindowTitle("MediaGrapher")
        #self.resize(500,350) #width, height

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
        #Doesn't change cursor yet
        #QApplication.setOverrideCursor(Qt.CursorShape.BusyCursor)
        self.setCursor(Qt.CursorShape.SizeBDiagCursor) #changes cursor, but doesn't work here or when resetting

        #QMainWindow.resizeEvent(self, event)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        #Saves window size
        self.setting_geometry = QSettings('MediaGrapher', 'Window Size').setValue('Window Size', self.saveGeometry())
        #self.setting_geometry.setValue('Window Size', self.saveGeometry())

    def setParameters(self):
        #https://www.pythonguis.com/tutorials/pyqt6-creating-multiple-windows/
        #self.w = settingWindow()
        pass
        
class settingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500,350)
        layout = QVBoxLayout()
        self.label = QLabel("Settings")
        layout.addWidget(self.label)
        self.setLayout(layout)

        #Probably best to enter in the main window
        output_filename = QLineEdit()
        layout.addWidget(output_filename)

        #self.layout.addWidget(QLabel("Algorithm"))
        algo_canny = QRadioButton("Canny", self)
        algo_canny.toggled.connect(self.update)
        algo_sobel = QRadioButton("Sobel", self)
        algo_sobel.toggled.connect(self.update)

        layout.addWidget(algo_canny)
        layout.addWidget(algo_sobel)

    def update(self):
        #gets radio button value
        rb = self.sender()

        #check if radio button is checked
        if rb.isChecked():
            print(f"{rb.text()} is selected")

    

# Create the app, the main window, and run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

