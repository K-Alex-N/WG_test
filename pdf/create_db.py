import sqlite3

def create_database(db_name="ships.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE weapons (
            weapon TEXT PRIMARY KEY,
            reload_speed INTEGER,
            rotational_speed INTEGER,
            diameter INTEGER,
            power_volley INTEGER,
            count INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE hulls (
            hull TEXT PRIMARY KEY,
            armor INTEGER,
            type INTEGER,
            capacity INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE engines (
            engine TEXT PRIMARY KEY,
            power INTEGER,
            type INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE ships (
            ship TEXT PRIMARY KEY,
            weapon TEXT,
            hull TEXT,
            engine TEXT,
            FOREIGN KEY (weapon) REFERENCES weapons(weapon),
            FOREIGN KEY (hull) REFERENCES hulls(hull),
            FOREIGN KEY (engine) REFERENCES engines(engine)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
