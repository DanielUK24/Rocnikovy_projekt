import psycopg
import os
from dotenv import load_dotenv
from psycopg import sql

def create_tables(config):

    # initializing variables for table names (spaces are replaced by _)
    dim_sensor_table_name = config["target_dimensions"]["dim_sensors"]["target_table"].replace(" ", "_")
    dim_day_table_name = config["target_dimensions"]["dim_dates"]["target_table"].replace(" ", "_")
    
    # initializing variables for column names in dim sensors table (spaces are replaced by _)
    dim_sensors_sensor_column = config["target_dimensions"]["dim_sensors"]["target_column"].replace(" ", "_")
    dim_sensors_id_column = config["target_dimensions"]["dim_sensors"]["id_column"].replace(" ", "_")
    
    # initializing variables for column names in dim dates table (spaces are replaced by _)
    dim_dates_date_column = config["target_dimensions"]["dim_dates"]["target_column"].replace(" ", "_")
    dim_dates_id_column = config["target_dimensions"]["dim_dates"]["id_column"].replace(" ", "_")

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
        
        with conn.cursor() as cur:

            # creating tables for sensor and date dimensions
            query_dim_sensors = sql.SQL("""
                                        CREATE TABLE IF NOT EXISTS {table_name} (
                                        {sensor_id_column} INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                        {sensor_column} varchar UNIQUE
                                        )""").format(
                                            sensor_id_column = sql.Identifier(dim_sensors_id_column),
                                            sensor_column = sql.Identifier(dim_sensors_sensor_column),
                                            table_name = sql.Identifier(dim_sensor_table_name),
                                        )

            query_dim_day = sql.SQL("""
                                    CREATE TABLE IF NOT EXISTS {table_name} (
                                    {day_id_column} INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                    {day_column} timestamp UNIQUE
                                    )""").format(
                                        day_id_column = sql.Identifier(dim_dates_id_column),
                                        day_column = sql.Identifier(dim_dates_date_column),
                                        table_name = sql.Identifier(dim_day_table_name),
                                    )
            
            cur.execute(query_dim_sensors)
            cur.execute(query_dim_day)

            cur.execute(
                sql.SQL("TRUNCATE TABLE {}").format(
                    sql.Identifier(dim_sensor_table_name)
                    )
            )

            cur.execute(
                sql.SQL("TRUNCATE TABLE {}").format(
                    sql.Identifier(dim_day_table_name)
                    )
            )

            # creating fact tables
            measurements_from_config = config["measurements"]
            for meas in measurements_from_config:

                # variable for fct measurements table name
                fct_table_name = meas["target_facts"]["target_table"].replace(" ", "_")

                # variable for timestamp column in fct measurements table
                fct_table_timestamp_column = meas["source_column_for_dim_dates"].replace(" ", "_")

                # initializing list of column names in fct measurements table 
                # but just for measurements, not measurement_id, sensor_is, date_id, timestamp (spaces are replaced by _)
                source_columns = meas["target_facts"]["source_columns"]
                source_columns_names = []
                for column in source_columns:
                    source_columns_names.append(column["name"])

                measurement_columns_identifiers = []
                for column in source_columns:
                    measurement_columns_identifiers.append(
                        sql.SQL("{} {}").format(
                            sql.Identifier(column["name"].replace(" ", "_")),
                            sql.SQL("FLOAT")
                        )
                    )

                query_fct_measurements = sql.SQL("""
                                                CREATE TABLE IF NOT EXISTS {table_name} (
                                                measurement_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                                {sensor_id_column} INTEGER,
                                                {day_id_column} INTEGER,
                                                {timestamp_column} timestamp,
                                                {measurement_columns}
                                                )""").format(
                                                    table_name = sql.Identifier(fct_table_name),
                                                    sensor_id_column = sql.Identifier(dim_sensors_id_column),
                                                    day_id_column = sql.Identifier(dim_dates_id_column),
                                                    timestamp_column = sql.Identifier(fct_table_timestamp_column),
                                                    measurement_columns = sql.SQL(',').join(measurement_columns_identifiers)
                                                )


                cur.execute(query_fct_measurements)

                cur.execute(
                    sql.SQL("TRUNCATE TABLE {}").format(
                        sql.Identifier(fct_table_name)
                        )
                )


            conn.commit()