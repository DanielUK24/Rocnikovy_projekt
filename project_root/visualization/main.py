import sys
import psycopg
import os
from dotenv import load_dotenv

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.ui.connection_window import ConnectionWindow
from src.meta_data_reader import MetaDataReader

def on_succesful_connection(data):
    print("Pripojené:", data)

#app = QApplication(sys.argv)

#connection_window = ConnectionWindow()
#connection_window.succesful_connection.connect(on_succesful_connection)
#connection_window.show()

#sys.exit(app.exec())

# loading and setting variables for .env
load_dotenv()
my_host = os.getenv("DB_HOST")
my_dbname = os.getenv("DB_NAME")
my_user = os.getenv("DB_USER")
my_password = os.getenv("DB_PASSWORD")

with psycopg.connect(
    host=my_host,
    dbname=my_dbname,
    user=my_user, 
    password=my_password) as conn:

        meta_data_reader = MetaDataReader()

        print("get_fct_tables: ", meta_data_reader.get_fct_tables(conn),"\n")
        print("get_sensors fct_measurements_water_300_lines: ", meta_data_reader.get_sensors(conn,"fct_measurements_water_300_lines"),"\n")
        print("get_sensors fct_measurements_water: ", meta_data_reader.get_sensors(conn, "fct_measurements_water"),"\n")
        print("get_sensors fct_measurements_weather: ", meta_data_reader.get_sensors(conn, "fct_measurements_weather"),"\n")
        print("get_metrics fct_measurements_water_300_lines: ", meta_data_reader.get_metrics(conn, "fct_measurements_water_300_lines"),"\n")
        print("get_metrics fct_measurements_water: ", meta_data_reader.get_metrics(conn, "fct_measurements_water"),"\n")
        print("get_metrics fct_measurements_weather: ", meta_data_reader.get_metrics(conn, "fct_measurements_weather"),"\n")
        print("get_timestamp_column fct_measurements_water_300_lines: ", meta_data_reader.get_timestamp_column(conn, "fct_measurements_water_300_lines"),"\n")
        print("get_timestamp_column fct_measurements_water: ", meta_data_reader.get_timestamp_column(conn, "fct_measurements_water"),"\n")
        print("get_timestamp_column fct_measurements_weather: ", meta_data_reader.get_timestamp_column(conn, "fct_measurements_weather"),"\n")
        print("get_dim_sensors: ", meta_data_reader.get_dim_sensors(conn),"\n")
        print("get_dim_sensors_id: ", meta_data_reader.get_dim_sensors_id(conn),"\n")
        print("get_dim_sensors_name: ", meta_data_reader.get_dim_sensors_name(conn),"\n")
        print("get_dim_dates: ", meta_data_reader.get_dim_dates(conn),"\n")
        print("get_dim_dates_id: ", meta_data_reader.get_dim_dates_id(conn),"\n")
        print("get_dim_dates_date: ", meta_data_reader.get_dim_dates_date(conn),"\n")
