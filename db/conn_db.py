import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

from config import DB_NAME
from constants import (
    CLOSED_CONNECTION,
    CONNECTING_TO_DB,
    CURSOR_ERROR,
    DB_ERROR,
    UNEXPECTED_ERROR,
)
from db.logger import logger


@contextmanager
def conn_db(db_name: str = DB_NAME) -> Generator[sqlite3.Connection, None, None]:
    logger.debug(CONNECTING_TO_DB.format(db_name=db_name))
    conn = sqlite3.connect(db_name)
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(DB_ERROR.format(db_name=db_name, e=e))
        # raise DatabaseError(f"Database operation failed: {e}") from e
    except Exception as e:
        conn.rollback()
        logger.error(UNEXPECTED_ERROR.format(db_name=db_name, e=e))
        # raise DatabaseError(f"Unexpected database error: {e}") from e
        raise
    finally:
        conn.close()
        logger.debug(CLOSED_CONNECTION.format(db_name=db_name))


@contextmanager
def get_cursor(db_name: str = DB_NAME) -> Generator[sqlite3.Cursor, None, None]:
    with conn_db(db_name) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        except sqlite3.Error as e:
            logger.error(CURSOR_ERROR.format(db_name=db_name, e=e))
            # raise DatabaseError(f"Cursor operation failed: {e}") from e
        finally:
            cursor.close()
