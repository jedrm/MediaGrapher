"""
GUI for MediaGrapher
"""


import sys
import os
# import subprocess

# NOTE: Some imports are for commented out code (Settings Window)
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QProcess, QSettings
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import (QHBoxLayout, QComboBox, QLineEdit, QTextEdit, QApplication, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)
from superqt import QLabeledRangeSlider

# Setting Window (Additional Imports)
# from PyQt6 import QtWidgets
# from PyQt6.QtGui import QResizeEvent
# from PyQt6.QtWidgets import (QMenu, QDialog, QRadioButton, QDialogButtonBox, QGroupBox)

ALLOWED_ALGORITHMS = ["Canny", "Sobel"]
MAX_THREADS = os.cpu_count()

class MainWindow(QMainWindow):
    """
    The main window of the MediaGrapher application.

    This class represents the main window of the MediaGrapher application. It inherits from the QMainWindow class
    and provides the user interface for the application. The main window contains various UI elements such as
    menus, input fields, buttons, and a terminal output area.

    Attributes:
        setting_geometry (QSettings): The QSettings object for storing and retrieving window size settings.

    Methods:
        __init__(): Initializes the MainWindow object.
        get_setting_values(): Retrieves the saved settings for the application window.
        init_ui(): Initializes the user interface of the main window.
        init_menu(): Initializes the menu bar of the main window.
        algorithm_parameters(): Initializes the algorithm parameters UI element.
        thresholds_parameter(): Initializes the thresholds parameter UI element.
        init_input_field(): Initializes the input field UI elements.
        init_script_button(): Initializes the script execution button.
        terminal_output(): Displays the terminal output in the UI.
        run_script(): Executes the script with the provided input and parameters.
        resize_event(): Handles the resize event of the main window.
        close_event(): Handles the close event of the main window.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.get_setting_values()

    def get_setting_values(self):
        """
        This method retrieves the saved settings for the application window.

        It fetches the window size from the QSettings object and restores the window geometry
        to the saved state. The settings are stored with the organization name 'MediaGrapher'
        and the application name 'Window Size'.

        Note: Currently, the method only handles window size. In the future, it may be extended
        to handle additional parameters.
        """
        self.setting_geometry = QSettings('MediaGrapher', 'Window Size')
        self.restoreGeometry(self.setting_geometry.value('Window Size'))

        # self.setting_parameters = QSettings('MediaGrapher', 'Parameters')

    def init_ui(self):
        """
        Initializes the user interface for the MediaGrapher application.
        Sets the window title, creates the central widget, and sets up the layout.
        Connects the QProcess readyRead signal to the terminal_output slot.
        Initializes the menu, algorithm parameters, thresholds parameter, input field, and script button.
        Creates a QTextEdit widget for terminal results and displays the window.
        """
        self.setWindowTitle("MediaGrapher")
        # self.resize(500,350) #width, height

        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)

        self.process = QProcess(self)
        self.process.readyRead.connect(self.terminal_output)

        self.init_menu()
        self.algorithm_parameters()
        self.thresholds_parameter()
        self.threads_parameter()
        self.init_input_field()
        self.init_script_button()

        self.terminal_results = QTextEdit()
        self.terminal_output()

        self.show()

    # NOTE: Uncomment code in this function to add a Settings Window in Menu Bar
    def init_menu(self):
        """
        Initializes the menu bar of the GUI window.
        """

        # NOTE: Uncomment to add a Settings Window to Menu Bar
        # self.w = settingWindow()
        # setParametersAct = QAction('&Set Parameters', self)
        # setParametersAct.setShortcut('Ctrl+P')
        # setParametersAct.triggered.connect(self.show_settingWindow)

        # Exit Action
        exit_act = QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        # Menu Bar
        menu_bar = self.menuBar()
        menu_mediagrapher = menu_bar.addMenu("Media Grapher")

        # NOTE: Uncomment to add a Settings Window in Menu Bar
        # menu_mediagrapher.addAction(setParametersAct)

        menu_mediagrapher.addAction(exit_act)

    # NOTE:Uncomment to show a Settings Window
    # def show_settingWindow(self, checked):
    #     #Shows Setting Window
    #     self.w.show()

    def algorithm_parameters(self):
        """
        Sets up the algorithm parameters in the GUI.

        This method creates a combo box to select the algorithm type (Canny or Sobel)
        and adds it to the layout.

        Parameters:
            None

        Returns:
            None
        """
        self.algo_combo_box = QComboBox()
        self.algo_combo_box.addItems(ALLOWED_ALGORITHMS)
        algo_label = QLabel("Algorithm: ")
        algo_label.setBuddy(self.algo_combo_box)
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algo_combo_box)
        self.layout.addLayout(algo_layout)

    def thresholds_parameter(self):
        """
        Sets up the GUI elements for adjusting algorithm thresholds.

        This method creates a QLabel and a QLabeledRangeSlider to allow the user to set the algorithm thresholds.
        The range of the slider is set from 0 to 255, with the initial slider position set to (30, 150).
        The tick interval of the slider is set to 10.
        The method also adds the threshold_layout to the main layout of the GUI.

        Returns:
            None
        """
        threshold_label = QLabel("Set Algorithm Thresholds: ")
        threshold_layout = QHBoxLayout()
        self.threshold_slider = QLabeledRangeSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setSliderPosition((30, 150))
        self.threshold_slider.setTickInterval(10)
        threshold_label.setBuddy(self.threshold_slider)
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.threshold_slider)

        self.threshold = [str(value)
                          for value in self.threshold_slider.value()]

        self.layout.addLayout(threshold_layout)

    def threads_parameter(self):
        """
        Creates a parameter for selecting the number of CPU threads to be used.

        This method creates a QComboBox widget that allows the user to select the number of CPU threads to be used.
        The available options range from 1 to MAX_THREADS.
        The default choice is set to MAX_THREADS.
        The widget is added to the layout of the GUI.

        Parameters:
            None

        Returns:
            None
        """
        self.threads_combo_box = QComboBox()
        self.threads_combo_box.addItems([str(i) for i in range(1, MAX_THREADS+1)])
        self.threads_combo_box.setCurrentIndex(MAX_THREADS-1)  # Set default choice to MAX_THREADS
        self.threads_combo_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        threads_label = QLabel("Number of CPU Threads: ")
        threads_label.setBuddy(self.threads_combo_box)
        threads_layout = QHBoxLayout()
        threads_layout.addWidget(threads_label)
        threads_layout.addWidget(self.threads_combo_box)
        self.layout.addLayout(threads_layout)


    def init_input_field(self):
        """
        Initializes the input field by creating the input box and output box layouts,
        adding labels and input fields to them, and adding the layouts to the main layout.
        """
        self.input_box = QHBoxLayout()
        self.input_label = QLabel("Enter URL: ")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter URL for Image/Video")
        self.input_label.setBuddy(self.input_field)
        self.input_box.addWidget(self.input_label)
        self.input_box.addWidget(self.input_field)
        self.layout.addLayout(self.input_box)

        self.output_box = QHBoxLayout()
        self.output_label = QLabel("Output File Name: ")
        self.output_file_name = QLineEdit()
        self.output_file_name.setPlaceholderText("Enter Output File Name")
        self.output_label.setBuddy(self.output_file_name)
        self.output_box.addWidget(self.output_label)
        self.output_box.addWidget(self.output_file_name)
        self.layout.addLayout(self.output_box)

    def init_script_button(self):
        """
        Initializes the script button.

        This function creates a QPushButton widget to run the script. It sets the button's text, cursor shape, click event handler, and shortcut. The button is then added to the layout.

        Parameters:
            None

        Returns:
            None
        """
        self.run_script_button = QPushButton("Download and Graph Image/Video")
        self.run_script_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.run_script_button.clicked.connect(self.run_script)
        self.run_script_button.setShortcut("Return")
        self.layout.addWidget(self.run_script_button)

    def terminal_output(self):
        """
        Display the output of the terminal process in the GUI.
        """
        self.terminal_results.setPlaceholderText("Terminal Results")
        self.terminal_results.setReadOnly(True)
        self.terminal_results.insertPlainText(
            self.process.readAll().data().decode())
        self.terminal_results.ensureCursorVisible()
        self.layout.addWidget(self.terminal_results)

    def run_script(self):
        """
        Executes the script by starting a subprocess to run the 'mediagrapher.py' script with the specified arguments.
        Disables the 'run_script_button' while the process is running and enables it when the process finishes.
        """
        try:
            output_flag = ["-o", self.output_file_name.text()
                           ] if self.output_file_name.text() else []
            algo_flag = ["-a", self.algo_combo_box.currentText()
                         ] if self.algo_combo_box.currentText() else []
            threshold_flag = ["-t", self.threshold[0],
                              self.threshold[1]] if self.threshold else []
            threads_flag = ["-p", self.threads_combo_box.currentText()] if self.threads_combo_box.currentText() else []

            # subprocess.run(["python", "mediagrapher.py", self.input_field.text()]+ output_flag + algo_flag + threshold_flag + threads_flag)
            self.process.start("python", ["mediagrapher.py", self.input_field.text(
            )] + output_flag + algo_flag + threshold_flag + threads_flag)

            # Just to prevent accidentally running multiple times
            # Disable the button when process starts, and enable it when it finishes
            self.process.started.connect(
                lambda: self.run_script_button.setEnabled(False))
            self.process.finished.connect(
                lambda: self.run_script_button.setEnabled(True))

        except ValueError as e:
            print(f"Error running script: {e}")

    # NOTE: Function not in use, and not working
    # pylint: disable=unused-argument
    def resize_event(self, event: QtGui.QResizeEvent) -> None:
        """
        Event handler for resizing the window.

        Args:
            event (QtGui.QResizeEvent): The resize event object.

        Returns:
            None
        """
        # Doesn't change cursor yet
        # QApplication.setOverrideCursor(Qt.CursorShape.BusyCursor)
        # changes cursor, but doesn't work here or when resetting
        self.setCursor(Qt.CursorShape.SizeBDiagCursor)

        # QMainWindow.resizeEvent(self, event)

    # pylint: disable=unused-argument
    def close_event(self, _event: QtGui.QCloseEvent) -> None:
        """
        Event handler for the close event of the window.

        Saves the window size when the program is closed.

        Args:
            event (QtGui.QCloseEvent): The close event object.

        Returns:
            None
        """
        self.setting_geometry = QSettings('MediaGrapher', 'Window Size').setValue(
            'Window Size', self.saveGeometry())


# NOTE: Uncomment below to add a Settings Window
# class settingWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.resize(300,250)
#         self.layout = QVBoxLayout()
#         self.setWindowTitle("Parameters")

#         self.algorithmParameters()

#         self.setLayout(self.layout)

#     def update(self):
#         #gets radio button value
#         rb = self.sender()
#         #check if radio button is checked
#         if rb.isChecked():
#             print(f"{rb.text()} is selected")

#     def algorithmParameters(self):
#         algo_combo_box = QComboBox()
#         algo_combo_box.addItems(["Canny", "Sobel"])
#         algo_label = QLabel("Algorithm")
#         algo_label.setBuddy(algo_combo_box)
#         topLayout = QHBoxLayout()
#         topLayout.addWidget(algo_label)
#         topLayout.addWidget(algo_combo_box)
#         self.layout.addLayout(topLayout)

# Create the app, the main window, and run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
