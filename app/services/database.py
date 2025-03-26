from app.configs.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.configs.environments import DATABASE_DRIVER, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from sqlalchemy.exc import OperationalError


class Database:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls._instance._db = None
        return cls._instance

    @staticmethod
    def create_connection_string():
        if not all([DATABASE_DRIVER, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME, DATABASE_PORT]):
            raise ValueError(
                "missing fields while trying to connect to the database")
        connection_string = f'{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
        return connection_string

    def get_or_create_db(self):
        if self._db is None:
            connection_string = self.create_connection_string()
            self._db = create_engine(connection_string)
            self._session_factory = sessionmaker(bind=self._db)
        return self._db

    def create_session(self):
        try:
            self.get_or_create_db()
            session = scoped_session(self._session_factory)
            return session
        except OperationalError as operr:
            logger.error(
                f'Unexpected error while trying to make the engine: {str(operr)}')
