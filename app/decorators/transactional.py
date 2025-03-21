from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


def transactional(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            with self._session.begin():
                return func(self, *args, **kwargs)
        except SQLAlchemyError as e:
            self._session.rollback()
            logger.error(
                f"Unexpected SQLAlchemy error, rollback executed: {str(e)}")
            raise
    return wrapper
