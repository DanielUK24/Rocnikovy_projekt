from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QToolButton
from PySide6.QtCore import Qt, Signal

from src.models.connection_data import ConnectionData

class ConnectionWindow(QMainWindow):
    succesful_connection = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Visualizator')

        self._build_ui()

    def _build_ui(self):

        container = QWidget()
        self.setCentralWidget(container)
        container_layout = QVBoxLayout(container)

        connection_info = QWidget()
        connection_layout = QGridLayout(connection_info)
        container_layout.addWidget(connection_info)

        host_label = QLabel('Host:')
        connection_layout.addWidget(host_label,5,0)
        self._host_line = QLineEdit()
        connection_layout.addWidget(self._host_line,5,1)

        port_label = QLabel('Port:')
        connection_layout.addWidget(port_label,8,0)
        self._port_line = QLineEdit()
        connection_layout.addWidget(self._port_line,8,1)

        database_label = QLabel('Database:')
        connection_layout.addWidget(database_label,10,0)
        self._database_line = QLineEdit()
        connection_layout.addWidget(self._database_line,10,1)

        username_label = QLabel('Username:')
        connection_layout.addWidget(username_label,15,0)
        self._username_line = QLineEdit()
        connection_layout.addWidget(self._username_line,15,1)

        password_label = QLabel('Password:')
        connection_layout.addWidget(password_label,20,0)
        self._password_line = QLineEdit()
        self._password_line.setEchoMode(QLineEdit.Password)
        connection_layout.addWidget(self._password_line,20,1)

        toggle_button = QToolButton()
        toggle_button.setText("👁")
        toggle_button.clicked.connect(self._toggle_password)
        connection_layout.addWidget(toggle_button,20,2)


        connect_button = QPushButton('Connect')
        connect_button.clicked.connect(self._on_connect_clicked)
        connection_layout.addWidget(connect_button,30,0)

    def set_inputs(self, connection_data):
        self._host_line.setText(connection_data.host)
        self._port_line.setText(connection_data.port)
        self._database_line.setText(connection_data.database)
        self._username_line.setText(connection_data.username)

    def _on_connect_clicked(self):

        # verifikacia

        # tieto data pojdu z UI
        connection_data = ConnectionData('localhost','5432','admin','my_db')

        self.succesful_connection.emit(connection_data)

    def _toggle_password(self):
        if (self._password_line.echoMode() == QLineEdit.Password):
            self._password_line.setEchoMode(QLineEdit.Normal)
        else:
            self._password_line.setEchoMode(QLineEdit.Password)

        