import sqlite3

from config import DB_NAME


def conn_db(db_name: str = DB_NAME):  # что на выходе получаем ???
    return sqlite3.connect(db_name)
