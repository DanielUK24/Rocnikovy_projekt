import psycopg2
import os
from dotenv import load_dotenv

class Loader:

    def __init__(self, config):

        active_measurement = config["active_measurement"]
        source_columns = config["measurements"][active_measurement]["target_facts"]["source_columns"]
        self._source_columns_names = []
        for column in source_columns:
            self._source_columns_names.append(column["name"])
        
        self._sensor_source_column = self._find_first(config["measurements"][active_measurement]["target_dimensions"], "accumulator", "yes")["source_column"]
        self._timestamp_source_column = self._find_first(config["measurements"][active_measurement]["target_dimensions"], "time_dimension", "yes")["source_column"]
        target_table = config["measurements"][active_measurement]["target_facts"]["target_table"]
        self._target_table_without_spaces = target_table.replace(" ", "_")

        self._sensor_source_column_without_spaces = self._sensor_source_column.replace(" ", "_")
        self.source_column_timestamp_without_spaces = self._timestamp_source_column.replace(" ", "_")
        
        self._measurement_columns_without_spaces = []
        for column in self._source_columns_names:
            self._measurement_columns_without_spaces.append(column.replace(" ", "_"))
        
        create_table_arg = "CREATE TABLE %s (%s varchar, %s timestamp" % (self._target_table_without_spaces, self._sensor_source_column_without_spaces, self.source_column_timestamp_without_spaces)
        for column in self._measurement_columns_without_spaces:
            create_table_arg += ", %s real" % column
        create_table_arg += ")"

        load_dotenv()
        self._my_host = os.getenv("DB_HOST")
        self._my_dbname = os.getenv("DB_NAME")
        self._my_user = os.getenv("DB_USER")
        self._my_password = os.getenv("DB_PASSWORD")
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

        insert_into_arg = "INSERT INTO %s (%s, %s" % (self._target_table_without_spaces, self._sensor_source_column_without_spaces, self.source_column_timestamp_without_spaces)
        for column in self._measurement_columns_without_spaces:
            insert_into_arg += ", " + column

        insert_into_arg += ") VALUES (%(" + self._sensor_source_column + ")s, %(" + self._timestamp_source_column + ")s"

        for column in self._source_columns_names:
            insert_into_arg += ", %(" + column + ")s"

        insert_into_arg += ");"

        for row in transformed_chunk:
            cur.execute(insert_into_arg, row)

        conn.commit()
        cur.close()
        conn.close()
