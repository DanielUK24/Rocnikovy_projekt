import sys

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.ui.connection_window import ConnectionWindow

app = QApplication(sys.argv)

conn_window = ConnectionWindow()
main_window = MainWindow()

conn_window.set_main_window(main_window)
main_window.set_conn_window(conn_window)

conn_window.show()

sys.exit(app.exec())
