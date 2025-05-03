from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


def transactional(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session = self._session
        try:
            result = func(self, *args, **kwargs)
            session.commit()
            return result
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(
                f"Unexpected SQLAlchemy error, rollback executed: {str(e)}")
            raise
    return wrapper
