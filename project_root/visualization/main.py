import sys
import os

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.ui.connection_window import ConnectionWindow
from src.db_conn_manager import DBConnectionManager

from dotenv import load_dotenv

app = QApplication(sys.argv)

# loading and setting variables for .env
load_dotenv()
my_host = os.getenv("DB_HOST")
my_dbname = os.getenv("DB_NAME")
my_user = os.getenv("DB_USER")
my_password = os.getenv("DB_PASSWORD")

conn_manager = DBConnectionManager()
conn_manager.init(my_host, 5432, my_dbname, my_user, my_password)

main_window = MainWindow()
main_window.show()
print("asdf")

sys.exit(app.exec())
