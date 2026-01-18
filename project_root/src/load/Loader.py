import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv, dotenv_values

class Loader:

    def __init__(self, config):
        # check which variables do not have to be instance variables

        active_measurement = config["active_measurement"]
        source_columns_dict = config["measurements"][active_measurement]["target_facts"]["source_columns"]
        self._source_columns = []
        for column in source_columns_dict:
            self._source_columns.append(column["name"])
        
        self._source_column_sensor = self._find_first(config["measurements"][active_measurement]["target_dimensions"], "accumulator", "yes")["source_column"]
        self._source_column_timestamp = self._find_first(config["measurements"][active_measurement]["target_dimensions"], "time_dimension", "yes")["source_column"]
        self._target_table = config["measurements"][active_measurement]["target_facts"]["target_table"]

        self._source_column_sensor_without_white = self._source_column_sensor.replace(" ", "_")
        self.source_column_timestamp_without_white = self._source_column_timestamp.replace(" ", "_")
        
        self._measurement_columns_without_white = []
        for column in self._source_columns:
            self._measurement_columns_without_white.append(column.replace(" ", "_"))

        create_table_arg = "CREATE TABLE %s (%s varchar, %s timestamp" % (self._target_table, self._source_column_sensor_without_white, self.source_column_timestamp_without_white)
        for column in self._measurement_columns_without_white:
            create_table_arg += ", %s real" % column
        create_table_arg += ")"

        load_dotenv()
        self._my_host = os.getenv("HOST")
        self._my_dbname = os.getenv("DB_NAME")
        self._my_user = os.getenv("USER")
        self._my_password = os.getenv("PASSWORD")
        print(self._my_host, self._my_dbname, self._my_user, self._my_password)
        conn = psycopg2.connect(host=self._my_host, dbname=self._my_dbname, user=self._my_user, password=self._my_password)
        cur = conn.cursor()

        cur.execute(create_table_arg)

        conn.commit()
        cur.close()
        conn.close()

    def _find_first(self, dicts, key, value):
        for dict in dicts:
            if key in dict.keys() and dict[key] == value:
                return dict

    def load(self, transformed_chunk):

        conn = psycopg2.connect(host=self._my_host, dbname=self._my_dbname, user=self._my_user, password=self._my_password)

        cur = conn.cursor()

        insert_into_arg = "INSERT INTO %s (%s, %s" % (self._target_table, self._source_column_sensor_without_white, self.source_column_timestamp_without_white)
        for column in self._measurement_columns_without_white:
            insert_into_arg += ", " + column

        insert_into_arg += ") VALUES (%(" + self._source_column_sensor + ")s, %(" + self._source_column_timestamp + ")s"

        for column in self._source_columns:
            insert_into_arg += ", %(" + column + ")s"

        insert_into_arg += ");"

        for row in transformed_chunk:
            cur.execute(insert_into_arg, row)

        conn.commit()
        cur.close()
        conn.close()
