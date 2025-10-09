import sqlite3

DB_NAME = "WoW.db"

connect = sqlite3.connect(DB_NAME)
cursor = connect.cursor()