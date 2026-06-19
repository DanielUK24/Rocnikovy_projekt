import psycopg

class DBConnectionManager:
    instance = None
    _connection = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def init(cls, host, port, database, username, password):
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=database,
            user=username,
            password=password,
            connect_timeout=3
        )
        cls.close_connection_if_exists()
        cls._connection = conn
    
    def get_connection(cls):
        return cls._connection
    
    def close_connection_if_exists(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None