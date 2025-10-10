import sqlite3
from contextlib import contextmanager

from config import DB_NAME


# def conn_db(db_name: str = DB_NAME):  # что на выходе получаем ???
#     return sqlite3.connect(db_name)


@contextmanager
def conn_db(db_name: str = DB_NAME):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()
