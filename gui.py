import os
import sys
import subprocess

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QAction, QResizeEvent, QCursor
from PyQt6.QtWidgets import (QMenu, QHBoxLayout, QComboBox,QLineEdit, QTextEdit, QApplication, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QApplication, QDialog, QRadioButton,QDialogButtonBox, QGroupBox)
from PyQt6.QtCore import Qt,QSettings
from superqt import QLabeledRangeSlider

# Create the app's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.getSettingValues()
    
    # TODO: Save choice of algorithm and thresholds for a user future use
    def getSettingValues(self):
        self.setting_geometry = QSettings('MediaGrapher', 'Window Size')
        self.restoreGeometry(self.setting_geometry.value('Window Size'))

        #self.setting_parameters = QSettings('MediaGrapher', 'Parameters')

    # TODO Changing cursor icon when resizing window
    # TODO Add a button to navigate to the output folder/file
    # TODO Add a button to open the output file
    # TODO Add a button to reset settings to default if additional settings are added
    # TODO Utilize a settings window to save user preferences if additional settings are added in the future
    def initUi(self):
        self.setWindowTitle("MediaGrapher")
        #self.resize(500,350) #width, height

        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)

        self.process = QProcess(self)
        self.process.readyRead.connect(self.terminalOutput)

        self.initMenu()
        self.algorithmParameters()
        self.thresholdsParameter()
        self.initInputField()
        self.initScriptButton()

        self.terminalResults = QTextEdit()
        self.terminalOutput()
        
        self.show()
        
    #NOTE: Uncomment code in this function to add a Settings Window in Menu Bar
    def initMenu(self):
        # NOTE: Uncomment to add a Settings Window to Menu Bar
        # self.w = settingWindow()
        # setParametersAct = QAction('&Set Parameters', self)
        # setParametersAct.setShortcut('Ctrl+P')
        # setParametersAct.triggered.connect(self.show_settingWindow)

        #Exit Action
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)

        #Menu Bar
        menuBar = self.menuBar()
        menuMediaGrapher = menuBar.addMenu("Media Grapher")

        # NOTE: Uncomment to add a Settings Window in Menu Bar
        #menuMediaGrapher.addAction(setParametersAct)

        menuMediaGrapher.addAction(exitAct)

    # NOTE:Uncomment to show a Settings Window
    # def show_settingWindow(self, checked):
    #     #Shows Setting Window
    #     self.w.show()     

    def algorithmParameters(self):
        self.algoComboBox = QComboBox()
        self.algoComboBox.addItems(["Canny", "Sobel"])
        algoLabel = QLabel("Algorithm: ")
        algoLabel.setBuddy(self.algoComboBox)
        algoLayout = QHBoxLayout()
        algoLayout.addWidget(algoLabel)
        algoLayout.addWidget(self.algoComboBox)
        self.layout.addLayout(algoLayout)

    def thresholdsParameter(self):
        thresholdLabel = QLabel("Set Algorithm Thresholds: ")  
        thresholdLayout = QHBoxLayout()
        self.thresholdSlider = QLabeledRangeSlider(Qt.Orientation.Horizontal)
        self.thresholdSlider.setRange(0,255)
        self.thresholdSlider.setSliderPosition((30,150))
        self.thresholdSlider.setTickInterval(10)
        thresholdLabel.setBuddy(self.thresholdSlider)
        thresholdLayout.addWidget(thresholdLabel)
        thresholdLayout.addWidget(self.thresholdSlider)

        #self.threshold = [str(self.thresholdSlider.value()[0]),str(self.thresholdSlider.value()[1])]
        self.threshold = [str(value) for value in self.thresholdSlider.value()]

        self.layout.addLayout(thresholdLayout)

    def initInputField(self):
        self.inputBox = QHBoxLayout()
        self.inputLabel = QLabel("Enter URL: ")
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter URL for Image/Video")
        self.inputLabel.setBuddy(self.inputField)
        self.inputBox.addWidget(self.inputLabel)
        self.inputBox.addWidget(self.inputField)
        self.layout.addLayout(self.inputBox)

        self.outputBox = QHBoxLayout()
        self.outputLabel = QLabel("Output File Name: ")
        self.outputFileName = QLineEdit()
        self.outputFileName.setPlaceholderText("Enter Output File Name")
        self.outputLabel.setBuddy(self.outputFileName)
        self.outputBox.addWidget(self.outputLabel)
        self.outputBox.addWidget(self.outputFileName)
        self.layout.addLayout(self.outputBox)

    def initScriptButton(self):
        #Button to run script
        self.runButton = QPushButton("Download and Graph Image/Video")
        self.runButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.runButton.clicked.connect(self.runScript)
        self.runButton.setShortcut("Return")
        self.layout.addWidget(self.runButton)
    
    def terminalOutput(self):
        self.terminalResults.setPlaceholderText("Terminal Results")
        cursor = self.terminalResults.textCursor()
        self.terminalResults.setReadOnly(True)
        cursor.insertText(self.process.readAll().data().decode())
        self.terminalResults.ensureCursorVisible()
        self.layout.addWidget(self.terminalResults)
        
    def runScript(self):
        try:
            output_flag = ["-o", self.outputFileName.text()] if self.outputFileName.text() else []
            algo_flag = ["-a", self.algoComboBox.currentText()] if self.algoComboBox.currentText() else []
            threshold_flag = ["-t", self.threshold[0], self.threshold[1] ] if self.threshold else []
    
            #subprocess.run(["python", "mediagrapher.py", self.inputField.text()]+ output_flag + algo_flag + threshold_flag)
            self.process.start("python", ["mediagrapher.py", self.inputField.text()]+ output_flag + algo_flag + threshold_flag)

            # Just to prevent accidentally running multiple times
            # Disable the button when process starts, and enable it when it finishes
            self.process.started.connect(lambda: self.runButton.setEnabled(False))
            self.process.finished.connect(lambda: self.runButton.setEnabled(True))

        except Exception as e:
            print(f"Error running script: {e}")

    def resizeEvent (self, event: QtGui.QResizeEvent) -> None:
        #Doesn't change cursor yet
        #QApplication.setOverrideCursor(Qt.CursorShape.BusyCursor)
        self.setCursor(Qt.CursorShape.SizeBDiagCursor) #changes cursor, but doesn't work here or when resetting

        #QMainWindow.resizeEvent(self, event)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        #Save Window Size when Program Closes
        self.setting_geometry = QSettings('MediaGrapher', 'Window Size').setValue('Window Size', self.saveGeometry())

    def setParameters(self):
        #https://www.pythonguis.com/tutorials/pyqt6-creating-multiple-windows/
        #self.w = settingWindow()
        pass

"""
Uncomment comment block below to add a Settings Window

TODO: Add Thresholds to Settings Window
TODO: Add Default Button to reset Settings to Default

"""
'''
class settingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(300,250)
        self.layout = QVBoxLayout()
        self.setWindowTitle("Parameters")

        self.algorithmParameters()

        self.setLayout(self.layout)

    def update(self):
        #gets radio button value
        rb = self.sender()
        #check if radio button is checked
        if rb.isChecked():
            print(f"{rb.text()} is selected")
    
    def algorithmParameters(self):
        algoComboBox = QComboBox()
        algoComboBox.addItems(["Canny", "Sobel"])
        algoLabel = QLabel("Algorithm")
        algoLabel.setBuddy(algoComboBox)
        topLayout = QHBoxLayout()
        topLayout.addWidget(algoLabel)
        topLayout.addWidget(algoComboBox)
        self.layout.addLayout(topLayout)
'''
    

# Create the app, the main window, and run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

