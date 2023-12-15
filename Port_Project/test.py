import sys
import signal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QSettings, QTimer, QCoreApplication
import atexit

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle('Power-Outage-Proof App')
        self.setGeometry(100, 100, 400, 300)

        # Example widgets
        self.label = QLabel('Enter some text:')
        self.line_edit = QLineEdit()
        self.button = QPushButton('Save State')
        self.button.clicked.connect(self.save_state)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Register the save_state function to be called at exit
        atexit.register(self.save_state)

    def save_state(self):
        settings = QSettings('MyCompany', 'MyApp')
        settings.setValue('text', self.line_edit.text())
        settings.setValue('geometry', self.saveGeometry())

    def load_settings(self):
        settings = QSettings('MyCompany', 'MyApp')
        text = settings.value('text', '')
        geometry = settings.value('geometry')

        if geometry:
            self.restoreGeometry(geometry)

        self.line_edit.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyApp()

    window.show()
    sys.exit(app.exec_())
