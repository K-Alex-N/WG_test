import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("WoW.db")
cursor = conn.cursor()

# Create tables
# weapons
cursor.execute("""
CREATE TABLE IF NOT EXISTS weapons (
    weapon TEXT PRIMARY KEY,
    reload_speed INTEGER,
    rotational_speed INTEGER,
    diameter INTEGER,
    power_volley INTEGER,
    count INTEGER
)
""")

# Create hulls table
cursor.execute("""
CREATE TABLE IF NOT EXISTS hulls (
    hull TEXT PRIMARY KEY,
    armor INTEGER,
    type INTEGER,
    capacity INTEGER
)
""")

# Create engines table
cursor.execute("""
CREATE TABLE IF NOT EXISTS engines (
    engine TEXT PRIMARY KEY,
    power INTEGER,
    type INTEGER
)
""")

# Create ships table
cursor.execute()

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created successfully.")
