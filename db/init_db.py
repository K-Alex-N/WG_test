import sqlite3

conn = None
cursor = None

DB_NAME = "WoW.db"


def init_db(db_name=DB_NAME):
    global conn
    global cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    yield
    conn.close()