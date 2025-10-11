from db.conn_db import get_cursor
from db.copy_db import drop_db_if_exists


def create_db():
    drop_db_if_exists()

    create_db_weapons = """
        CREATE TABLE IF NOT EXISTS weapons (
            weapon TEXT PRIMARY KEY,
            reload_speed INTEGER,
            rotational_speed INTEGER,
            diameter INTEGER,
            power_volley INTEGER,
            count INTEGER
        );
        """
    create_db_hulls = """
        CREATE TABLE IF NOT EXISTS hulls (
            hull TEXT PRIMARY KEY,
            armor INTEGER,
            type INTEGER,
            capacity INTEGER
        );
        """

    create_db_engines = """
    CREATE TABLE IF NOT EXISTS engines (
        engine TEXT PRIMARY KEY,
        power INTEGER,
        type INTEGER
    );
    """
    create_db_ships = """
        CREATE TABLE IF NOT EXISTS ships (
            ship TEXT PRIMARY KEY,
            weapon TEXT,
            hull TEXT,
            engine TEXT,
            FOREIGN KEY (weapon) REFERENCES weapons(weapon),
            FOREIGN KEY (hull) REFERENCES hulls(hull),
            FOREIGN KEY (engine) REFERENCES engines(engine)
        );
        """

    with get_cursor() as cursor:
        cursor.execute(create_db_weapons)
        cursor.execute(create_db_hulls)
        cursor.execute(create_db_engines)
        cursor.execute(create_db_ships)

    # logging.info("Databases created successfully.")
