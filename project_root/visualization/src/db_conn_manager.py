import psycopg

class DBConnectionManager:
    instance = None
    _connection = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def init(cls, host, port, database, username, password):
        cls._connection = cls._create_connection(host, port, database, username, password)
        
    def get_connection(cls):
        if cls._connection is None:
            raise Exception("Connection not initialized")
        return cls._connection
    
    def _create_connection(host, port, database, username, password):
        try:
            conn = psycopg.connect(
                host=host,
                port=port,
                dbname=database,
                user=username,
                password=password,
                connect_timeout=5
            )
            return conn
        except psycopg.Error as e:
            # dtd tato vynimka tu je zatial iba tak
            # dtd bude sa este riesit poriadnejsie pri rieseni vynimiek
            raise RuntimeError(f"Failed to connect to database: {e}")
        