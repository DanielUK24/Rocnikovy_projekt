from psycopg import Connection
from psycopg import sql

class MetaDataReader:

    @staticmethod
    def get_fct_tables(conn: Connection):
        
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

        with conn.cursor() as cur:
            cur.execute(query, ("fct",))
            rows = cur.fetchall()

        return [row[0] for row in rows]

    @staticmethod
    def get_sensors(conn: Connection, fct_table):
        
        with conn.cursor() as cur:
            query = sql.SQL("""
                SELECT DISTINCT ds.{sensor}
                FROM {fct_table} fct
                JOIN {dim_sensors} ds ON fct.{sensor_id} = ds.{sensor_id}
            """).format(
                sensor = sql.Identifier(MetaDataReader.get_dim_sensors_name(conn)),
                fct_table = sql.Identifier(fct_table),
                dim_sensors = sql.Identifier(MetaDataReader.get_dim_sensors(conn)),
                sensor_id = sql.Identifier(MetaDataReader.get_dim_sensors_id(conn))
            )
            cur.execute(query)
            rows = cur.fetchall()

        return [row[0] for row in rows]

    @staticmethod
    def get_metrics(conn: Connection, fct_table):
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

                AND (d.description IS NULL OR d.description != 'timestamp');
        """

        with conn.cursor() as cur:
            cur.execute(query, (fct_table,))
            rows = cur.fetchall()

        return [row[0] for row in rows]

    @staticmethod
    def get_timestamp_column(conn: Connection, fct_table):
        return MetaDataReader._find_column_by_comments(conn, fct_table, "timestamp")

    @staticmethod
    def get_dim_sensors(conn: Connection):
        return MetaDataReader._find_table_by_comment(conn, "dim_sensors")

    @staticmethod
    def get_dim_sensors_id(conn: Connection):
        return MetaDataReader._find_column_by_comments(conn, MetaDataReader.get_dim_sensors(conn), "sensor_id")

    @staticmethod
    def get_dim_sensors_name(conn: Connection):
        return MetaDataReader._find_column_by_comments(conn, MetaDataReader.get_dim_sensors(conn), "name")

    @staticmethod
    def get_dim_dates(conn: Connection):
        return MetaDataReader._find_table_by_comment(conn, "dim_dates")

    @staticmethod
    def get_dim_dates_id(conn: Connection):
        return MetaDataReader._find_column_by_comments(conn, MetaDataReader.get_dim_dates(conn), "date_id")

    @staticmethod
    def get_dim_dates_date(conn: Connection):
        return MetaDataReader._find_column_by_comments(conn, MetaDataReader.get_dim_dates(conn), "date")

    @staticmethod
    def _find_table_by_comment(conn, comment):

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

        with conn.cursor() as cur:
            cur.execute(query, (comment,))
            rows = cur.fetchall()

        if len(rows) == 0:
            return None
        if len(rows) > 1:
            raise ValueError(
                f"Invariant violated: multiple tables found for comment '{comment}'"
            )

        return rows[0][0]

    @staticmethod
    def _find_column_by_comments(conn, table_name, column_comment):

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

        with conn.cursor() as cur:
            cur.execute(query, (table_name, column_comment))
            rows = cur.fetchall()

        if len(rows) == 0:
            return None
        if len(rows) > 1:
            raise ValueError("Invariant violated: multiple matching columns found")
 
        return rows[0][0]
