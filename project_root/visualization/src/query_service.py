from psycopg import sql

from src.db_conn_manager import DBConnectionManager
from src.meta_data_reader import MetaDataReader

class QueryService:

    def __init__(self):
        self._conn_manager = DBConnectionManager()
        self._meta_data_reader = MetaDataReader()

    def get_data_one_sensor_many_metrics(self, fct_table, sensor, metrics, start, end):

        metrics_sql_identifiers = []
        for metric in metrics:
            metrics_sql_identifiers.append(sql.Identifier("f", metric))

        # loading timestamps and measurements from database
        query = sql.SQL("""
                        SELECT f.{timestamp_column}, {measurement_columns}
                        FROM {fct_measurements} f
                        JOIN {dim_dates} dd ON dd.{dim_date_id} = f.{fact_date_id}
                        JOIN {dim_sensors} ds ON ds.{dim_sensor_id} = f.{fact_sensor_id}
                        WHERE dd.{date} BETWEEN %s AND %s AND ds.{name} = %s
                        ORDER BY f.{timestamp_column}
                        """).format(
                            timestamp_column = sql.Identifier(self._meta_data_reader.get_timestamp_column(fct_table)),
                            measurement_columns = sql.SQL(',').join(metrics_sql_identifiers),
                            fct_measurements = sql.Identifier(fct_table),
                            dim_dates = sql.Identifier(self._meta_data_reader.get_dim_dates()),
                            dim_date_id = sql.Identifier(self._meta_data_reader.get_dim_dates_id()),
                            fact_date_id = sql.Identifier(self._meta_data_reader.get_dim_dates_id()),
                            dim_sensors = sql.Identifier(self._meta_data_reader.get_dim_sensors()),
                            dim_sensor_id = sql.Identifier(self._meta_data_reader.get_dim_sensors_id()),
                            fact_sensor_id = sql.Identifier(self._meta_data_reader.get_dim_sensors_id()),
                            date = sql.Identifier(self._meta_data_reader.get_dim_dates_date()),
                            name = sql.Identifier(self._meta_data_reader.get_dim_sensors_name()),
                        )

        with self._conn_manager.get_connection().cursor() as cur:
            cur.execute(query, (start, end, sensor))
            return cur.fetchall()
        
    def get_data_many_sensors_one_metric(self, fct_table, sensors, metric, start, end):

        metric_values_for_sensors = []

        with self._conn_manager.get_connection().cursor() as cur:

            for sensor in sensors:

                query = sql.SQL("""
                                SELECT f.{timestamp_column}, {metric_column}
                                FROM {fct_measurements} f
                                JOIN {dim_dates} dd ON dd.{dim_date_id} = f.{fact_date_id}
                                JOIN {dim_sensors} ds ON ds.{dim_sensor_id} = f.{fact_sensor_id}
                                WHERE dd.{date} BETWEEN %s AND %s AND ds.{name} = %s
                                ORDER BY f.{timestamp_column}
                                """).format(
                                    timestamp_column = sql.Identifier(self._meta_data_reader.get_timestamp_column(fct_table)),
                                    metric_column = sql.Identifier(metric),
                                    fct_measurements = sql.Identifier(fct_table),
                                    dim_dates = sql.Identifier(self._meta_data_reader.get_dim_dates()),
                                    dim_date_id = sql.Identifier(self._meta_data_reader.get_dim_dates_id()),
                                    fact_date_id = sql.Identifier(self._meta_data_reader.get_dim_dates_id()),
                                    dim_sensors = sql.Identifier(self._meta_data_reader.get_dim_sensors()),
                                    dim_sensor_id = sql.Identifier(self._meta_data_reader.get_dim_sensors_id()),
                                    fact_sensor_id = sql.Identifier(self._meta_data_reader.get_dim_sensors_id()),
                                    date = sql.Identifier(self._meta_data_reader.get_dim_dates_date()),
                                    name = sql.Identifier(self._meta_data_reader.get_dim_sensors_name()),
                                )
                cur.execute(query, (start, end, sensor))
                metric_values_for_sensors.append(cur.fetchall())

        return metric_values_for_sensors