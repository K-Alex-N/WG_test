import logging
import sqlite3
from contextlib import contextmanager
from typing import Generator

from config import DB_NAME


@contextmanager
def conn_db(db_name: str = DB_NAME) -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(db_name)
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        logging.exception(f"Database error in {db_name}: {e}")
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
