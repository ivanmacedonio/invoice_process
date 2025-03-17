from sqlalchemy import create_engine
from configs.environments import DATABASE_DRIVER, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME


class Database:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls._instance._db = None
        return cls._instance

    @staticmethod
    def create_connection_string():
        connection_string = f'{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
        return connection_string

    def get_or_create_db(self):
        if self._db is None:
            connection_string = self.create_connection_string()
            self._db = create_engine(connection_string)
        return self._db
