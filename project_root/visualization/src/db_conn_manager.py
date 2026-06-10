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
    
    def _create_connection(self, host, port, database, username, password):
        # tu by asi ani nemalo byt try a except, staci ak to odchyti conn window
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=database,
            user=username,
            password=password
        )
        return conn
        