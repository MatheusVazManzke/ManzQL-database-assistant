from sqlalchemy import create_engine
from llama_index.core import SQLDatabase

class DatabaseConnector:
    def __init__(self):
        self.engine = None
        self.connection = None
        self.sql_database = None

    def create_engine(self, db_type, user, password, host, port, db_name):
        """
        Creates a SQLAlchemy engine based on the user's input.
        
        :param db_type: The type of database (e.g., 'mysql', 'postgresql', etc.)
        :param user: Username for the database
        :param password: Password for the database
        :param host: Host where the database is located
        :param port: Port number to connect to
        :param db_name: The name of the database
        :return: None
        """
        # Mapping db_type to the correct connector string
        db_connector = {
            'mysql': 'mysql+mysqlconnector',
            'postgresql': 'postgresql+psycopg2',
            'sqlite': 'sqlite'  # SQLite doesn't need user, password, host, or port
        }

        if db_type not in db_connector:
            raise ValueError(f"Unsupported database type: {db_type}")

        if db_type == 'sqlite':
            connection_string = f"{db_connector[db_type]}:///{db_name}.db"
        else:
            connection_string = f"{db_connector[db_type]}://{user}:{password}@{host}:{port}/{db_name}"

        self.engine = create_engine(connection_string)

    def connect_to_db(self, include_tables=None):
        """
        Establishes a connection to the database and sets up the SQLDatabase object.
        
        :param include_tables: List of table names to include in the SQLDatabase object.
        :return: None
        """
        if not self.engine:
            raise RuntimeError("Engine has not been created. Please call create_engine() first.")

        self.connection = self.engine.connect()

        # Creating the SQLDatabase object using the connected engine
        self.sql_database = SQLDatabase(self.engine, include_tables=include_tables)

    def close_connection(self):
        """
        Closes the connection to the database.
        :return: None
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_sql_database(self):
        """
        Returns the SQLDatabase object.
        :return: SQLDatabase object
        """
        return self.sql_database
