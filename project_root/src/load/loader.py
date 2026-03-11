import psycopg
import os
from dotenv import load_dotenv
from psycopg import sql
from datetime import datetime

class Loader:

    def __init__(self, config, active_measurement):
        
        # initializing variables for table names (spaces are replaced by _)
        self._fct_table_name = config["measurements"][active_measurement]["target_facts"]["target_table"].replace(" ", "_")
        self._dim_sensors_table_name = config["target_dimensions"]["dim_sensors"]["target_table"].replace(" ", "_")
        self._dim_dates_table_name = config["target_dimensions"]["dim_dates"]["target_table"].replace(" ", "_")
        
        # initializing variables for column names in dim sensors table (spaces are replaced by _)
        self._dim_sensors_sensor_column = config["target_dimensions"]["dim_sensors"]["target_column"].replace(" ", "_")
        self._dim_sensors_id_column = config["target_dimensions"]["dim_sensors"]["id_column"].replace(" ", "_")
        
        # initializing variables for column names in dim dates table (spaces are replaced by _)
        self._dim_dates_date_column = config["target_dimensions"]["dim_dates"]["target_column"].replace(" ", "_")
        self._dim_dates_id_column = config["target_dimensions"]["dim_dates"]["id_column"].replace(" ", "_")

        # initializing list of column names in fct measurements table (spaces are replaced by _)
        source_columns = config["measurements"][active_measurement]["target_facts"]["source_columns"]
        source_columns_names = []
        for column in source_columns:
            source_columns_names.append(column["name"].replace(" ", "_"))

        self._fact_table_column_identifiers = []
        fct_table_timestamp_column = config["measurements"][active_measurement]["source_column_for_dim_dates"].replace(" ", "_")
        self._fact_table_column_identifiers.append(sql.Identifier(self._dim_sensors_id_column))
        self._fact_table_column_identifiers.append(sql.Identifier(self._dim_dates_id_column))
        self._fact_table_column_identifiers.append(sql.Identifier(fct_table_timestamp_column))
        for column in source_columns_names:
            self._fact_table_column_identifiers.append(sql.Identifier(column))

        # loading and setting variables for .env
        load_dotenv()
        self._my_host = os.getenv("DB_HOST")
        self._my_dbname = os.getenv("DB_NAME")
        self._my_user = os.getenv("DB_USER")
        self._my_password = os.getenv("DB_PASSWORD")
            
    def load_to_dim_sensors(self, all_sensors_from_codelist):
        
        with psycopg.connect(
            host=self._my_host, 
            dbname=self._my_dbname, 
            user=self._my_user, 
            password=self._my_password) as conn:
            
            with conn.cursor() as cur:
                
                query = sql.SQL("""
                    INSERT INTO {table} ({column})
                    VALUES (%s)
                    ON CONFLICT ({column}) DO NOTHING
                    """).format(
                        table=sql.Identifier(self._dim_sensors_table_name),
                        column=sql.Identifier(self._dim_sensors_sensor_column)
                        )

                values = [(sensor,) for sensor in all_sensors_from_codelist]
            
                cur.executemany(query, values)

                conn.commit()
    
    def load(self, measurements_to_load, dates_to_load: list[datetime], sensor_name):
        # measurements_to_load must contain just timestamp + all measured values

        assert len(measurements_to_load) == len(dates_to_load)

        dates_to_load_tuples = [(date,) for date in dates_to_load]

        with psycopg.connect(
            host=self._my_host, 
            dbname=self._my_dbname, 
            user=self._my_user, 
            password=self._my_password) as conn:
            
            with conn.cursor() as cur:

                # loading dates to dim_dates
                query_for_insert_date = sql.SQL("""
                                                INSERT INTO {table} ({column})
                                                VALUES (%s)
                                                ON CONFLICT ({column}) DO NOTHING
                                                """).format(
                                                    table=sql.Identifier(self._dim_dates_table_name),
                                                    column=sql.Identifier(self._dim_dates_date_column)
                                                )
                cur.executemany(query_for_insert_date, dates_to_load_tuples)

                # selecting current sensor id from dim_sensors
                query_for_select_sensor_id = sql.SQL("""
                                           SELECT {id_column}
                                           FROM {table}
                                           WHERE {sensor_column} = %s
                                           """).format(
                                               id_column = sql.Identifier(self._dim_sensors_id_column),
                                               table = sql.Identifier(self._dim_sensors_table_name),
                                               sensor_column = sql.Identifier(self._dim_sensors_sensor_column)
                                            )
                cur.execute(query_for_select_sensor_id, (sensor_name,))
                this_sensor_id = cur.fetchone()[0]

                for meas, date_tuple in zip(measurements_to_load, dates_to_load_tuples):

                    query_for_select_date_id = sql.SQL("""
                                                       SELECT {id_column}
                                                       FROM {table}
                                                       WHERE {date_column} = %s
                                                       """).format(
                                                           id_column=sql.Identifier(self._dim_dates_id_column),
                                                           table=sql.Identifier(self._dim_dates_table_name),
                                                           date_column=sql.Identifier(self._dim_dates_date_column)
                                                       )
                    cur.execute(query_for_select_date_id, date_tuple)
                    this_date_id = cur.fetchone()[0]

                    meas.insert(0, this_date_id)
                    meas.insert(0, this_sensor_id)

                    query_for_insert_of_row = sql.SQL("""
                        INSERT INTO {table} ({columns})
                        VALUES ({values})
                        """).format(
                            table=sql.Identifier(self._fct_table_name),
                            columns=sql.SQL(',').join(self._fact_table_column_identifiers),
                            values=sql.SQL(',').join(meas)
                        )
                    cur.execute(query_for_insert_of_row)

                conn.commit()
