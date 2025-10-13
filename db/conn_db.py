import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

from config import DB_NAME


@contextmanager
def conn_db(db_name: str = DB_NAME) -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(db_name)
    try:
        # logger.debug(f"Connecting to database: {db_path}")
        # conn = sqlite3.connect(str(db_path))
        # conn.row_factory = sqlite3.Row  # Enable column access by name
        yield conn
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        # logger.error(f"Database error in {db_path}, transaction rolled back: {e}")
        # raise DatabaseError(f"Database operation failed: {e}") from e
    except Exception:
        conn.rollback()
        # logger.error(f"Unexpected error in {db_path}: {e}")
        # raise DatabaseError(f"Unexpected database error: {e}") from e
        raise
    finally:
        conn.close()
        # logger.debug(f"Closed connection to {db_path}")


@contextmanager
def get_cursor(db_name: str = DB_NAME) -> Generator[sqlite3.Cursor, None, None]:
    with conn_db(db_name) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        # except sqlite3.Error as e:
        #     logger.error(f"Cursor error in {db_name}: {e}")
        #     raise DatabaseError(f"Cursor operation failed: {e}") from e
        finally:
            cursor.close()
