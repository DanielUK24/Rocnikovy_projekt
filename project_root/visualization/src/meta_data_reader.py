from psycopg import sql

from src.db_conn_manager import DBConnectionManager

class MetaDataReader:

    def __init__(self, shared_config):
        self._conn_manager = DBConnectionManager()
        self._dim_sensors_table_code = shared_config["dim_sensors_table_code"]
        self._dim_sensors_id_column = shared_config["dim_sensors_id_column"]
        self._dim_sensors_name_column = shared_config["dim_sensors_name_column"]
        self._dim_dates_table_code = shared_config["dim_dates_table_code"]
        self._dim_dates_id_column = shared_config["dim_dates_id_column"]
        self._dim_dates_date_column = shared_config["dim_dates_date_column"]
        self._fct_table_code = shared_config["fct_table_code"]
        self._timestamp_column = shared_config["timestamp_column"]

    def get_fct_tables(self):
        
        query = """
            SELECT c.relname AS table_name
            FROM pg_catalog.pg_description d
            JOIN pg_catalog.pg_class c 
                ON d.objoid = c.oid
            WHERE
                d.objsubid = 0
                AND c.relkind = 'r'
                AND d.description = %s
        """

        with self._conn_manager.get_connection().cursor() as cur:
            cur.execute(query, (self._fct_table_code,))
            rows = cur.fetchall()

        return [row[0] for row in rows]

    def get_sensors(self, fct_table):
        
        with self._conn_manager.get_connection().cursor() as cur:
            query = sql.SQL("""
                SELECT DISTINCT ds.{sensor}
                FROM {fct_table} fct
                JOIN {dim_sensors} ds ON fct.{sensor_id} = ds.{sensor_id}
            """).format(
                sensor = sql.Identifier(self.get_dim_sensors_name()),
                fct_table = sql.Identifier(fct_table),
                dim_sensors = sql.Identifier(self.get_dim_sensors()),
                sensor_id = sql.Identifier(self.get_dim_sensors_id())
            )
            cur.execute(query)
            rows = cur.fetchall()

        return [row[0] for row in rows]

    def get_metrics(self, fct_table):
        query = """
            SELECT a.attname
            FROM pg_catalog.pg_attribute a
            JOIN pg_catalog.pg_class c 
                ON a.attrelid = c.oid
            LEFT JOIN pg_catalog.pg_description d
                ON d.objoid = a.attrelid AND d.objsubid = a.attnum
            WHERE
                c.relname = %s
                AND c.relkind = 'r'
                AND a.attnum > 0
                AND NOT a.attisdropped

                AND a.attnum NOT IN (
                    SELECT unnest(con.conkey)
                    FROM pg_catalog.pg_constraint con
                    WHERE con.conrelid = c.oid
                    AND con.contype = 'p'
                )

                AND a.attnum NOT IN (
                    SELECT unnest(con.conkey)
                    FROM pg_catalog.pg_constraint con
                    WHERE con.conrelid = c.oid
                    AND con.contype = 'f'
                )

                AND (d.description IS NULL OR d.description != %s);
        """

        with self._conn_manager.get_connection().cursor() as cur:
            cur.execute(query, (fct_table, self._timestamp_column))
            rows = cur.fetchall()

        return [row[0] for row in rows]

    def get_timestamp_column(self, fct_table):
        return self._find_column_in_table_by_comment(fct_table, self._timestamp_column)

    def get_dim_sensors(self):
        return self._find_table_by_comment(self._dim_sensors_table_code)

    def get_dim_sensors_id(self):
        return self._find_column_in_table_by_comment(self.get_dim_sensors(), self._dim_sensors_id_column)

    def get_dim_sensors_name(self):
        return self._find_column_in_table_by_comment(self.get_dim_sensors(), self._dim_sensors_name_column)

    def get_dim_dates(self):
        return self._find_table_by_comment(self._dim_dates_table_code)

    def get_dim_dates_id(self):
        return self._find_column_in_table_by_comment(self.get_dim_dates(), self._dim_dates_id_column)

    def get_dim_dates_date(self):
        return self._find_column_in_table_by_comment(self.get_dim_dates(), self._dim_dates_date_column)

    def _find_table_by_comment(self, comment):

        query = """
            SELECT c.relname AS table_name
            FROM pg_catalog.pg_description d
            JOIN pg_catalog.pg_class c 
                ON d.objoid = c.oid
            WHERE 
                d.objsubid = 0
                AND c.relkind = 'r'
                AND d.description = %s
            LIMIT 2;
        """

        with self._conn_manager.get_connection().cursor() as cur:
            cur.execute(query, (comment,))
            rows = cur.fetchall()

        if len(rows) == 0:
            return None
        if len(rows) > 1:
            raise ValueError(
                f"Invariant violated: multiple tables found for comment '{comment}'"
            )

        return rows[0][0]

    def _find_column_in_table_by_comment(self, table_name, column_comment):

        query = """
            SELECT a.attname AS column_name
            FROM pg_catalog.pg_description d_col
            JOIN pg_catalog.pg_attribute a
                ON a.attrelid = d_col.objoid
                AND a.attnum = d_col.objsubid
            JOIN pg_catalog.pg_class c
                ON c.oid = d_col.objoid
            WHERE 
                c.relname = %s
                AND d_col.description = %s
                AND c.relkind = 'r'
            LIMIT 2;
        """

        with self._conn_manager.get_connection().cursor() as cur:
            cur.execute(query, (table_name, column_comment))
            rows = cur.fetchall()

        if len(rows) == 0:
            return None
        if len(rows) > 1:
            raise ValueError("Invariant violated: multiple matching columns found")
 
        return rows[0][0]
