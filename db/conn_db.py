import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

from config import DB_NAME


@contextmanager
def conn_db(db_name: str = DB_NAME) -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(db_name)
    try:
        yield conn
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        # logging.exception(f"Database error in {db_name}")
        # logger.exception(...)   <-- Использован именованный логгер 'logger'
        raise
    finally:
        conn.close()


@contextmanager
def get_cursor(db_name: str = DB_NAME) -> Generator[sqlite3.Cursor, None, None]:
    with conn_db(db_name) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
