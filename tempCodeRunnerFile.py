from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# Create the app's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello, World!")

        button = QPushButton("My simple app.")
        button.pressed.connect(self.close)

        self.setCentralWidget(button)
        self.show()

# Create the app, the main window, and run the app
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()