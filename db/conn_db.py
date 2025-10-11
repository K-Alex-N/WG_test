import sqlite3
from contextlib import contextmanager

from config import DB_NAME


@contextmanager
def conn_db(db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        # logging.error(f"Database error: {e}")
    finally:
        conn.close()
