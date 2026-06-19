import sys
import json

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from src.main_window import MainWindow
from src.connection_window import ConnectionWindow
    
shared_config_file = "shared/config/config.json"
with open(shared_config_file, 'r', encoding='utf-8') as f:
    shared_config = json.load(f)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("icons/app_icon.png"))

conn_window = ConnectionWindow()
main_window = MainWindow(shared_config)

conn_window.set_main_window(main_window)
main_window.set_conn_window(conn_window)

conn_window.show()

sys.exit(app.exec())
